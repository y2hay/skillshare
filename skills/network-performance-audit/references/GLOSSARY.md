# Glossary — Network Performance Audit

Disclosed reference. Load this when the agent needs deeper definitions for any of the bolded terms in `SKILL.md`.

---

## bottleneck

The single constraint that caps performance in a networked system. Every network path has exactly one bottleneck at any moment — the slowest link in the chain. Finding it means every slower link downstream is explained, and every faster link upstream is irrelevant until the bottleneck moves.

**Practical test:** If you fix X and throughput improves, X was the bottleneck. If you fix X and throughput stays the same, X was not the bottleneck.

**How to find it:** The audit phases are ordered to find the bottleneck in descending likelihood. Phase 2 (link cage) catches 80% of homelab slowdowns. Only go deeper if the physical link is already healthy.

---

## link cage

The physical-layer negotiation between a NIC and the switch port it's plugged into. The link cage is the hardest constraint because it's invisible to software — the OS thinks the link is fine at 100Mbps, and every higher-layer measurement agrees. Only `ethtool` reveals the cage.

**Why it matters:** 1000baseT Gigabit can move roughly 10× the data per second as 100baseT. No amount of TCP tuning, DNS optimization, or buffer tweaking will push past the cage limit.

**Common failure modes:**

| Symptom | Likely cause |
|---------|--------------|
| Link at 100Mbps, both sides support 1000baseT | Damaged cable or marginal termination |
| Link at 100Mbps, switch doesn't advertise 1000baseT | Switch port configured for 100Mbps, or cable too long (>100m) |
| Link flaps (drops and renegotiates) | Intermittent cable fault or EMI |
| Link at 10Mbps when expected higher | Very bad cable, or forced speed on switch |

**Fix order:** Replace cable first (cheapest), then check switch port config, then try a different port on the switch.

---

## PMTU blackhole

Path MTU (Maximum Transmission Unit) discovery failure. Normally, when a router receives a packet larger than the next hop's MTU, it sends back an ICMP "Fragmentation Needed" message so the sender shrinks. A **PMTU blackhole** is a router that silently drops the oversized packet without sending the ICMP message.

**Why exit nodes make this worse:** Tailscale encapsulate inside WireGuard, adding ~60 bytes of overhead. A server sends a 1500-byte TCP segment; Tailscale wraps it in a 1560-byte WireGuard packet. If any router on the path has an MTU of 1500, the expanded packet is silently dropped with no ICMP response. The TCP connection stalls until a retransmit happens with a smaller segment (if `tcp_mtu_probing` is enabled).

**Detection:**
```bash
# If this fails but a smaller size works, you have a PMTU blackhole:
ping -c 1 -M do -s 1472 8.8.8.8  # standard 1500 MTU
ping -c 1 -M do -s 1340 8.8.8.8  # exit-node-safe MTU (1280 + 60 overhead?)
```

**Fix:** `sysctl -w net.ipv4.tcp_mtu_probing=2` — enables always-on PMTU discovery at the kernel level. The kernel will actively probe MTU rather than waiting for ICMP messages.

---

## bridge squeeze

When a Linux bridge (like `vmbr0` on Proxmox) drops received packets because the bridge can't deliver them fast enough through the egress interface.

**How it happens:** The physical NIC receives packets at wire speed and places them on the bridge. The bridge needs to forward them to the destination (a veth interface for a container, or the host's network stack). If the CPU or the destination interface can't keep up, the bridge's backlog grows and starts dropping.

**Why it's a downstream symptom:** When the physical link is 100Mbps, the bridge will accumulate drops because the veth interfaces feeding into it have a different speed profile. Fix the link speed, and the bridge drops almost always resolve.

**Isolation:**
- `ip -s link show vmbr0` — check the `dropped` column
- Compare with `ethtool -S nic0` — if the physical NIC has 0 errors and 0 drops, the bridge itself is the chokepoint, not the wire

**Worth flagging independently only if** the physical link is already Gigabit and drops persist — that suggests a CPU/IRQ imbalance or a driver issue.

---

## Tailscale table 52

The Linux routing table that Tailscale uses for its internal peer routing. Table 52 is a subsidiary routing table, separate from the main table (table 254), and is activated by policy rule `5270: from all lookup 52`.

**Normal contents:** Only Tailscale IPs (100.x.x.x/32) and IPv6 ULAs (fd7a:.../128). These are the routes that tell the kernel "to reach this Tailscale peer, send via `tailscale0`."

**Abnormal contents:** Any `10.10.0.0/24` or other local subnet route in table 52. This happens when Tailscale's internal subnet routing logic adds the local LAN to its table — usually as a side effect of exit node configuration or subnet routing advertisement. When present, it can cause traffic to the local LAN to be routed through `tailscale0` instead of `vmbr0`, breaking direct LAN access.

**Check:**
```bash
ip route show table 52
```

**Fix:** Usually resolves when the exit node is cleared (`tailscale set --exit-node=`) or when LAN access is re-enabled (`--exit-node-allow-lan-access`).

---

## WireGuard encapsulation overhead

Tailscale uses WireGuard for encryption. WireGuard adds headers to each packet:

| Component | Approximate overhead |
|-----------|---------------------|
| UDP header | 8 bytes |
| WireGuard type+reserved | 4 bytes |
| WireGuard counter | 8 bytes |
| Encryption metadata | ~16 bytes |
| Auth tag (Poly1305) | 16 bytes |
| **Total overhead** | **~52-60 bytes** |

This means a 1500-byte TCP segment becomes a ~1556-byte WireGuard packet. On a network with 1500-byte MTU, this forces fragmentation or triggers a PMTU blackhole if `tcp_mtu_probing` is off.

**Effective MTU for exit node traffic:** If the LAN MTU is 1500 and WireGuard adds 60 bytes, the effective MTU for the inner (encrypted) traffic is approximately 1440 (1500 - 60). Tailscale defaults to 1280 internally to leave room for IPv6 and avoid fragmentation.

---

## conntrack exhaustion

The Linux connection tracking (`conntrack`) table tracks every active network connection. When the table fills up, the kernel starts evicting the oldest established connections to make room for new ones — causing random TCP resets and application timeouts.

**Why it happens in homelabs:** Docker containers, LXC containers, and Tailscale all create large numbers of connections. A system with many containers can easily exhaust the default 262144 conntrack entries.

**Monitoring:**
```bash
# Current usage
conntrack -C

# Utilization percentage
echo "$(conntrack -C) * 100 / $(cat /proc/sys/net/netfilter/nf_conntrack_max)" | bc

# Table size
cat /proc/sys/net/netfilter/nf_conntrack_max

# Early drop detection (if >0, connections are being dropped)
cat /proc/sys/net/netfilter/nf_conntrack_acct 2>/dev/null
```

**Fix:** Increase the table:
```bash
sysctl -w net.netfilter.nf_conntrack_max=524288
```

---

## BBR

Bottleneck Bandwidth and Round-trip propagation time — Google's congestion control algorithm. Unlike CUBIC (the Linux default), BBR does not rely on packet loss as a congestion signal. It models the available bandwidth and RTT directly, which makes it excellent for:

- Networks with bufferbloat
- Wireless links with variable latency
- Exit node paths where extra hops add latency but not congestion
- High-latency links where CUBIC would unnecessarily slow down

**Pairing:** BBR must be paired with the `fq` (fair queue) qdisc on the egress interface. Without `fq`, BBR's pacing doesn't work correctly:
```bash
sysctl -w net.core.default_qdisc=fq
```

---

## tcp_mtu_probing values

| Value | Behavior |
|-------|----------|
| 0 | **Disabled.** Kernel trusts ICMP Fragmentation Needed messages. If a router is a PMTU blackhole, TCP stalls silently until retransmit timeout. |
| 1 | **Probe on blackhole detection.** Kernel only probes MTU after noticing a pattern of blackhole behavior (lost packets without ICMP). |
| 2 | **Always probe.** Every TCP connection probes for the optimal MTU. Best practice for networks with exit nodes, VPNs, or tunnels. Zero downside in modern networks. |

---

## tcp_slow_start_after_idle

When set to 1 (default), the kernel resets the congestion window to its initial value (`initcwnd`) after a TCP connection has been idle for one RTO (retransmission timeout). This means every bursty API call or web request starts from a cold congestion window, taking several round trips to ramp up.

Setting to 0 preserves the congestion window across idle periods, which significantly improves performance for bursty application traffic (HTTP APIs, dashboards, monitoring, web interfaces).

**Safe to change:** Yes, on any modern network. Preserving the congestion window across idle periods cannot cause congestion collapse because the window still responds to actual loss events.

---

## fq qdisc

Fair Queueing packet scheduler. Queues packets per-flow and paces BBR's probe packets at the calculated rate. Without `fq`, BBR sends bursts that can overwhelm a shallow buffer, causing self-inflicted packet loss.

**Verify:**
```bash
tc qdisc show dev vmbr0
# Should show 'fq' not 'noqueue' or 'pfifo_fast'
```
