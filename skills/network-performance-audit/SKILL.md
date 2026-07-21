---
name: network-performance-audit
description: "Comprehensive Linux network stack audit for the xcx homelab — NIC link negotiation, TCP sysctl tuning, routing table analysis, bridge drops, MTU/PMTU testing, DNS health, conntrack, exit node path analysis, and bandwidth throughput. Use when diagnosing slow connections, optimizing network throughput, tuning TCP performance, investigating packet drops, configuring Tailscale exit nodes, or troubleshooting connectivity degradation. Also triggers on: \"slow network\", \"performance audit\", \"network tune-up\", \"diagnose connectivity\", \"check network speed\", \"MTU issue\", \"packet loss\", \"high latency\"."
disable-model-invocation: false
---

# Skill: Network Performance Audit

Hunt the **bottleneck** — the single constraint in the network path. A full audit is 11 phases run sequentially. Each phase ends with a clear finding: **pass**, **warn**, or **fail**. Report the full chain at the end so the user sees exactly which phase caps performance.

## Before you start

You need **root** on the target machine. All commands require root privileges unless noted. If a command isn't available (`ethtool`, `conntrack`, `bc`), the phase notes an alternative and the missing tool itself becomes a minor finding.

## Phases

### 1. Quick connectivity smoke test

Establish a baseline — is the machine reachable and responding?

```bash
hostname -f
ping -c 3 -W 2 8.8.8.8     # internet reachable + baseline latency
ping -c 3 -W 2 10.10.0.1     # gateway reachable
ping -c 3 -W 2 10.10.0.53    # DNS reachable (Pi-hole)
# Exit if DNS is unreachable: check with 1.1.1.1 or 8.8.8.8
```

**Completion criterion:** All three ping targets respond with <5% loss. If any fails, flag it and continue — the deeper phases will tell you why.

---

### 2. Physical layer audit — the **link cage**

The physical link negotiation sets the hard ceiling on every measurement that follows. If the NIC negotiated to 100Mbps when it should be Gigabit, every other finding is downstream of that.

```bash
# NIC identification
ethtool -i <iface>            # driver, firmware, bus
ip link show <iface>          # MTU, state, qlen

# Link negotiation
ethtool <iface>               # Speed, Duplex, Auto-negotiation
ethtool <iface> | grep -i 'Link partner'  # What the switch/router advertised

# Cable/path check
ethtool <iface> | grep -iE 'Supported|Advertised'  # What this NIC can do
```

**Analysis:**

| Advertised capabilities | Negotiated speed | Likely cause |
|------------------------|-----------------|--------------|
| 1000baseT/Full | 1000Mb/s | ✅ Healthy Gigabit link |
| 1000baseT/Full | 100Mb/s | **Bad cable or switch port fault** — 🔴 **top fix** |
| 1000baseT/Full | 10Mb/s | **Severe cable fault or misconfiguration** |
| Link partner doesn't advertise your speed | Mismatch | Switch port may be hard-set, or cable problem prevents link from reaching full negotiation |

**Combined failure indicator:** If the physical NIC (not the bridge) shows `Speed: 100Mb/s` and the NIC supports Gigabit, that single finding is the **bottleneck** and everything downstream is derivative.

**Completion criterion:** Record the negotiated speed and the NIC's advertised capabilities. Flag a mismatch as 🔴.

---

### 3. TCP sysctl audit

The kernel's TCP stack settings directly control throughput, latency under load, and resilience to path MTU issues.

```bash
sysctl net.ipv4.tcp_congestion_control    # Should be 'bbr' (gold standard)
sysctl net.ipv4.tcp_mtu_probing           # Should be '2' (enabled, always probe)
sysctl net.ipv4.tcp_slow_start_after_idle # Should be '0' (no reset on idle)
sysctl net.ipv4.tcp_rmem                  # Read buffer: 4096 87380 16777216
sysctl net.ipv4.tcp_wmem                  # Write buffer: 4096 65536 16777216
sysctl net.core.default_qdisc             # Should be 'fq' (BBR pairing)
```

**Thresholds:**

| Setting | Pass | Warn | Fail |
|---------|------|------|------|
| tcp_congestion_control | bbr | — | anything else |
| tcp_mtu_probing | 2 | 1 | 0 |
| tcp_slow_start_after_idle | 0 | — | 1 |
| tcp_rmem default | ≥87380 | 65536-87379 | <65536 |
| tcp_wmem default | ≥65536 | 40960-65535 | <40960 |
| default_qdisc | fq | — | anything else |

**Completion criterion:** Every TCP setting recorded and classified pass/warn/fail. The user sees the table.

---

### 4. Routing table audit

Misrouted traffic is invisible to the application — packets disappear into the wrong interface.

```bash
ip route show table main       # Default route + local subnet
ip rule show                    # Policy routing rules
ip route show table 52          # Tailscale routing table (if Tailscale installed)
```

**Checks:**
- **Main table:** Default route should go through `vmbr0` (or the correct bridge), not `tailscale0`.
- **Policy rules:** Tailscale's rules (fwmark 0x80000, table 52) are normal. If a `10.10.0.0/24` route appears in table 52, it may interfere with direct LAN access when an exit node is active — flag as a **warn**.
- **Multiple default routes:** Only one default route should exist. Two means asymmetric routing or a split-tunnel gone wrong.
- **Tailscale table 52:** Should contain only 100.x.x.x/32 and fd7a:.../128 peer routes. If it contains 10.10.0.0/24, flag as described above.

**Completion criterion:** All three tables inspected. If table 52 contains local subnet routes, flag as ⚠️.

---

### 5. Bridge and interface audit — **bridge squeeze**

When the bridge drops packets, it's usually because a fast interface feeds a slow one, or a container veth could be overwhelmed.

```bash
# Bridge drops
ip -s link show vmbr0          # Check 'dropped' column in RX
echo "Drop rate: $(echo "DROPS * 100 / PACKETS" | bc)%"  # Calculate percentage

# Physical interface health
ethtool -S <phys_iface>        # rx_errors, tx_errors, rx_missed_errors, rx_no_buffer_count

# Per-container veth drops
for iface in $(ip link show | grep -o 'veth[0-9a-z]*i[0-9]*'); do
    ip -s link show "$iface" | grep -A1 RX | tail -1 | awk '{print $3, "drops"}'
done

# Ring buffer (may not be available in LXC)
ethtool -g <phys_iface> 2>/dev/null || echo "Ring buffer info unavailable"
```

**Thresholds:**

| Metric | Pass | Warn | Fail |
|--------|------|------|------|
| vmbr0 RX drops | <0.5% of RX packets | 0.5-2% | >2% |
| Physical NIC errors | 0 | >0, no pattern | >0, growing |
| veth drops | 0 | — | >0 |
| rx_no_buffer_count | 0 | >0 | >100 |

**If drops are high (>2%):** Check whether the physical link speed (Phase 2) is the bottleneck. If the NIC is 100Mbps, that's the root cause.

**Completion criterion:** Drop rates calculated and classified. If >2%, link it to the Phase 2 finding.

---

### 6. MTU / PMTU audit — **PMTU blackhole**

Path MTU discovery silently breaks when a router drops oversized packets without sending ICMP Fragmentation Needed. The exit node path is especially vulnerable because of the WireGuard encapsulation overhead.

```bash
# Test across the MTU range
for mtu in 1500 1440 1400 1280 1200; do
    ping -c 1 -M do -s $((mtu - 28)) -W 2 8.8.8.8 2>&1 | tail -1
done

# Interface MTUs
ip link show | grep -E 'mtu|UP'

# TCP MTU probing setting
sysctl net.ipv4.tcp_mtu_probing
```

**Analysis:**
- **MTU 1500** should pass (allowing for the 28-byte header, that's `-s 1472`). If it fails but 1440 succeeds, there may be a PMTU blackhole on the path.
- **MTU 1280** is Tailscale's standard MTU and is the minimum IPv6-safe MTU. It should always pass.
- If `tcp_mtu_probing=0` AND any MTU test fails, flag 🔴 — this is a **PMTU blackhole** and will cause intermittent TCP stalls.

**Exit node specific:** When an exit node is active, the effective path MTU is:
- Tailscale's internal MTU (1280) + WireGuard encapsulation overhead (~60 bytes) = effective 1340 or less.
- Test: `ping -c 1 -M do -s 1312 -W 2 8.8.8.8` — if this passes, the path can handle the exit node overhead.

**Completion criterion:** All MTU tests pass. If any fail with `tcp_mtu_probing=0`, flag as 🔴.

---

### 7. DNS audit

Slow DNS makes everything feel sluggish. A misconfigured resolver also masks other issues.

```bash
cat /etc/resolv.conf
resolvectl status 2>/dev/null || echo "No systemd-resolved"
tailscale dns status 2>/dev/null || echo "No tailscale DNS status"
```

**Checks:**
- **Nameservers should be local:** 10.10.0.53 (Pi-hole) and 10.10.0.253 (Technitium). A 1.1.1.1 fallback is fine.
- **Tailscale DNS status:** Record whether it's enabled. In the homelab, local DNS is preferred — if Tailscale DNS is on, note it.
- **Search domains:** Should include `lan` for the homelab.
- **Timeouts:** `dig +time=2 +tries=1 google.com @10.10.0.53` to verify sub-second resolution.

**Completion criterion:** All nameservers are reachable and respond in <1s.

---

### 8. Conntrack audit

A full conntrack table causes random connection drops — the kernel starts evicting established connections.

```bash
echo "Max: $(cat /proc/sys/net/netfilter/nf_conntrack_max)"
echo "Current: $(conntrack -C 2>/dev/null || echo 'N/A')"
```

**Thresholds:**

| Utilization | Status |
|-------------|--------|
| <50% full | ✅ Healthy |
| 50-80% full | ⚠️ Watch |
| >80% full | 🔴 Near exhaustion — increase `nf_conntrack_max` |
| >95% full | 🔴 Critical — connections being actively dropped |

**Completion criterion:** Utilization percentage recorded and classified. If >80%, flag as 🔴.

---

### 9. Exit node path analysis (if Tailscale exit node in use)

When the machine is using a Tailscale exit node, the effective path is:
```
machine → tailscale0 → vmbr0 → LAN → exit node → internet
```

Each hop adds latency. Measure the breakdown:

```bash
# Who's the exit node?
tailscale status | grep 'exit node'
tailscale exit-node list 2>/dev/null

# Path latency: LAN to exit node
ping -c 3 -W 2 <exit-node-LAN-IP>    # 10.10.0.xxx

# Path latency: Tailscale to exit node
ping -c 3 -W 2 <exit-node-Tailscale-IP>  # 100.xxx

# Internet through exit node vs direct
echo "Direct to internet:"
ping -c 1 -W 3 1.1.1.1 | tail -1

echo "Through exit node:"
# (SSH to exit node and ping from there, or check with exit node active)
ssh -o ConnectTimeout=3 root@<exit-node-IP> 'ping -c 1 -W 3 1.1.1.1 | tail -1'

# Exit node allow-lan-access flag
tailscale status --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('ExitNode active:', d.get('Self',{}).get('ExitNode'))" 2>/dev/null
```

**Analysis:**
- **LAN latency** should be <1ms to any homelab machine.
- **Tailscale overhead** is the difference between LAN ping and Tailscale ping to the same machine. ~3-5ms is normal for userspace WireGuard. >10ms suggests CPU contention.
- **Internet via exit node** should be lower than direct (that's why you use it). If it's the same or worse, the exit node isn't helping.
- **lan=false** prevents LAN access during exit node use — this caused the SSH failure the user experienced.

**Completion criterion:** Complete latency breakdown recorded. If exit node latency > direct, flag as ⚠️.

---

### 10. Bandwidth throughput test

Latency tests miss bandwidth constraints. A quick SSH-pipe test reveals the real-world throughput ceiling.

```bash
# Throughput to another homelab machine over LAN
dd if=/dev/zero bs=1M count=100 2>/dev/null | \
  ssh -o ConnectTimeout=5 root@10.10.0.111 'dd of=/dev/null' 2>&1

# Result: "104857600 bytes (105 MB, 100 MiB) copied, X.XX s, YY.Y MB/s"
# YY.Y MB/s * 8 = ZZZ Mbps
```

**Thresholds (for homelab LAN):**

| Link speed | Expected SSH throughput (~80% of wire) |
|------------|----------------------------------------|
| 1000Mbps (Gigabit) | ~90-110 MB/s |
| 100Mbps | ~9-12 MB/s |
| 10Mbps | ~0.9-1.2 MB/s |

If throughput is below 80% of wire speed AND all prior phases passed, the bottleneck is elsewhere — check disk I/O on the target or CPU load during the transfer.

**Completion criterion:** Throughput measured and compared to expected wire speed. If <80%, cross-reference with Phase 2 (link speed).

---

### 11. Firewall rules audit

iptables/nftables can silently rate-limit or drop traffic.

```bash
iptables-save 2>/dev/null | grep -v '^#' | grep -v '^:' | head -50
nft list ruleset 2>/dev/null | head -50 || echo "No nftables"
```

**Focus checks:**
- **Tailscale rules:** Look for `-A ts-forward -s 100.64.0.0/10 -o tailscale0 -j DROP` — this is normal, prevents routing loops.
- **Rate limiting:** Any `limit` or `connlimit` rules that might throttle SSH or DNS.
- **Default policies:** Should be ACCEPT for INPUT/OUTPUT on the bridge.

**Completion criterion:** Firewall rules reviewed. No unexpected rate limits or overly restrictive defaults.

---

## Synthesis — finding the **bottleneck**

After all 11 phases, identify the single most constraining finding:

| Priority | Finding | Action |
|----------|---------|--------|
| 🔴 | NIC at 100Mbps when capable of Gigabit | Diagnose cable/switch port |
| 🔴 | tcp_mtu_probing=0 with PMTU failure | Set to 2 |
| 🔴 | Conntrack >80% full | Increase `nf_conntrack_max` |
| ⚠️ | vmbr0 drops >2% | Usually downstream of 100Mbps link — fix that first |
| ⚠️ | tcp_slow_start_after_idle=1 | Set to 0 |
| ⚠️ | tcp_congestion_control not BBR | Switch to BBR + fq qdisc |
| ℹ️ | DNS slow or misordered | Fix in `/etc/resolv.conf` |
| ℹ️ | Tailscale exit node overhead >10ms | Check CPU load on exit node |

**The rule:** Identify ONE bottleneck. If the NIC is 100Mbps, everything else is downstream of that. Don't recommend five fixes — recommend the one that matters.

**Completion criterion:** A single bottleneck identified and clearly stated to the user, with a concrete fix. All other findings reported as secondary or derivative.

## Relevant files

- `HOSTS/<hostname>.md` — update if NIC speed/duplex is newly recorded
- `references/GLOSSARY.md` — detailed definitions of every term used above
- `/etc/sysctl.d/99-network-tweaks.conf` — persistent sysctl overrides (create if applying fixes)
