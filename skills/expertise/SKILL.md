---
name: build-p2p-infrastructure
description: Build and optimize P2P file sharing infrastructure from scratch through production. Covers BitTorrent (qBittorrent, Deluge), Usenet (SABnzbd, NZBGet), aria2, media automation (*arr stack), seedbox optimization, and performance troubleshooting.
---

<skill>
<objective>
Provide comprehensive domain expertise for building, optimizing, and troubleshooting P2P file sharing infrastructure, including BitTorrent, Usenet, aria2, and the *arr stack.
</objective>

<quick_start>
Identify the protocol (BitTorrent for swarms, Usenet for retention, aria2 for direct). Follow the relevant workflow in `workflows/`. Optimize for privacy (VPN binding) and throughput (port forwarding, connection tuning).
</quick_start>

<success_criteria>
- P2P clients are optimally configured for performance and privacy
- *arr stack automation (Sonarr/Radarr) correctly imports and hardlinks files
- Usenet completion is high and BitTorrent ratios are maintained
- Troubleshooting identifies root causes (ISP throttling, NAT issues, I/O bottlenecks)
</success_criteria>

<essential_principles>
- **Protocol Selection**: Use BitTorrent for popular content, Usenet for obscure/reliable retention, and aria2 for multi-protocol mirror coordination.
- **Privacy &amp; Security**: Mandatory VPN/Proxy binding for public torrents. Use SSL/TLS for Usenet. Disable DHT/PEX on private trackers.
- **Performance**: Tune connection limits, enable port forwarding (49160-65534), and use SSDs for incomplete downloads.
- **Automation**: Use Prowlarr for indexer management and hardlinks to maintain seeding while organizing media.
</essential_principles>

<intake_routing>
- **Setup**: `workflows/setup-bittorrent-client.md`, `workflows/setup-usenet-stack.md`
- **Optimization**: `workflows/optimize-client-performance.md`, `workflows/setup-privacy-stack.md`
- **Troubleshooting**: `workflows/troubleshoot-slow-speeds.md`, `workflows/troubleshoot-usenet-failures.md`
- **Knowledge**: `references/bittorrent-protocol.md`, `references/usenet-protocol.md`
</intake_routing>

<resources>
<workflows_index>
- **workflows/setup-bittorrent-client.md**: Optimal qBittorrent/Deluge setup
- **workflows/setup-usenet-stack.md**: SABnzbd/NZBGet and provider config
- **workflows/integrate-arr-stack.md**: Connecting Sonarr/Radarr/Lidarr
- **workflows/setup-privacy-stack.md**: VPN binding and leak prevention
</workflows_index>

<reference_index>
- **references/bittorrent-protocol.md**: DHT, PEX, and tracker mechanics
- **references/usenet-protocol.md**: NNTP, retention, and completion
- **references/network-optimization.md**: Port forwarding and bandwidth tuning
- **references/storage-optimization.md**: Disk I/O and filesystem choices
</reference_index>
</resources>

<usage_notes>
- **Direct Invocation**: Follow workflow step-by-step.
- **Planning**: Load relevant references BEFORE creating an implementation plan.
- **Infrastructure**: Consider Docker/LXC context (e.g., Dockge LXC managing stacks).
</usage_notes>
</skill>


---
# Additional Documentation from Legacy Version

| `setup-bittorrent-client.md` | Install and configure qBittorrent/Deluge optimally | Setup |
| `setup-usenet-stack.md` | Providers, indexers, SABnzbd/NZBGet configuration | Setup |
| `setup-aria2.md` | Multi-protocol download manager configuration | Setup |
| `integrate-arr-stack.md` | Connect Sonarr/Radarr/Lidarr to download clients | Setup |
| `optimize-client-performance.md` | Tune for maximum throughput | Optimization |
| `troubleshoot-slow-speeds.md` | Diagnose and fix performance issues | Troubleshooting |
| `troubleshoot-stalled-torrents.md` | Fix stuck/stopped downloads | Troubleshooting |
| `troubleshoot-usenet-failures.md` | Handle incomplete/failed Usenet downloads | Troubleshooting |
| `manage-private-trackers.md` | Ratio management, tracker rules, freeleech | Advanced |
| `migrate-between-clients.md` | Move torrents between clients without data loss | Advanced |
| `setup-privacy-stack.md` | VPN/proxy configuration, IP binding, leak prevention | Security |
| `automate-categories.md` | Category-based automation and organization | Automation |

## Reference Index

All references use pure XML structure for maximum parsability by planning tools.

| Reference | Content |
|-----------|---------|
| **Protocol Knowledge** |
| `bittorrent-protocol.md` | How BitTorrent works (DHT, PEX, trackers) |
| `usenet-protocol.md` | How Usenet works (NNTP, retention, completion) |
| `aria2-capabilities.md` | HTTP/FTP/BitTorrent/Metalink protocols |
| **Client Comparison** |
| `bittorrent-clients.md` | qBittorrent vs Deluge vs Transmission vs rTorrent |
| `usenet-clients.md` | SABnzbd vs NZBGet feature comparison |
| `download-managers.md` | aria2 vs wget vs curl vs yt-dlp |
| **Configuration** |
| `qbittorrent-optimization.md` | Performance tuning, categories, automation |
| `deluge-optimization.md` | Plugin ecosystem, thin client mode, performance |
| `sabnzbd-optimization.md` | Servers, categories, scripts, post-processing |
| `nzbget-optimization.md` | Performance tuning, scripting, extensions |
| `aria2-optimization.md` | Configuration file, RPC, advanced features |
| **Integration** |
| `arr-stack-integration.md` | Sonarr/Radarr/Lidarr/Prowlarr workflows |
| `download-client-api.md` | API integration patterns |
| `category-automation.md` | Category-based workflows and scripts |
| `post-processing.md` | Extract, rename, move, notify patterns |
| **Infrastructure** |
| `network-optimization.md` | Port forwarding, connection limits, bandwidth |
| `storage-optimization.md` | Disk I/O, filesystem choices, cache tuning |
| `privacy-security.md` | VPN/proxy, IP binding, encryption, leak prevention |
| `seedbox-setup.md` | Dedicated server optimization patterns |
| **Troubleshooting** |
| `troubleshooting-bittorrent.md` | Slow speeds, stalls, tracker errors |
| `troubleshooting-usenet.md` | Failed downloads, PAR2 repair, server errors |
| `troubleshooting-network.md` | ISP throttling, NAT issues, firewall |
| `troubleshooting-arr-stack.md` | Import failures, matching issues |
| **Ecosystem** |
| `trackers-indexers.md` | Public vs private trackers, Usenet indexers |
| `usenet-providers.md` | Backbone vs resellers, retention, completion |
| `private-tracker-economy.md` | Ratio management, freeleech, bonus points |
| `anti-patterns.md` | Common mistakes, what NOT to do |

## Usage Notes

**For direct invocation**: Follow workflow step-by-step

**For planning tools**: Load relevant references before creating implementation plan

**Platform context**: Workflows include considerations for Docker, LXC, bare metal, and your specific balthazar infrastructure (Dockge LXC managing Docker stacks)
