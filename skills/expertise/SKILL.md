---
name: build-p2p-infrastructure
description: Build and optimize P2P file sharing infrastructure from scratch through production. Covers BitTorrent (qBittorrent, Deluge), Usenet (SABnzbd, NZBGet), aria2, media automation (*arr stack), seedbox optimization, and performance troubleshooting.
---

# P2P File Sharing & Optimization Expertise

Comprehensive domain expertise for peer-to-peer file sharing covering BitTorrent clients (qBittorrent, Deluge), Usenet (SABnzbd, NZBGet), aria2 multi-protocol downloads, *arr stack automation (Sonarr, Radarr, Lidarr, Prowlarr), seedbox optimization, and troubleshooting.

## Essential Principles

### 1. Protocol Understanding - Choose the Right Tool

**BitTorrent**: Decentralized P2P protocol excelling at popular content with many seeders. Best for public trackers, community-driven sharing, and content with long-term availability. Trade-off: dependent on swarm health (seeders).

**Usenet**: Centralized NNTP-based binary distribution with provider-hosted retention. Best for obscure content, guaranteed speeds (server-based), and automation workflows. Trade-off: requires paid provider + indexer subscription.

**aria2**: Multi-protocol download manager supporting HTTP/HTTPS, FTP, BitTorrent, and Metalink. Best for direct downloads, mirror coordination, and mixed protocol workflows. Trade-off: more manual configuration required.

**Decision tree**: Popular content with healthy swarms → BitTorrent | Obscure/older content or automation priority → Usenet | Direct downloads or multi-mirror coordination → aria2

### 2. Privacy & Security - Protect Your Identity

**VPN/Proxy binding**: Mandatory for public torrent trackers. Route traffic through encrypted tunnel, bind client to VPN interface to prevent leaks if VPN drops. Private trackers often forbid VPN use (ban risk).

**Encryption**: Enable protocol encryption in BitTorrent clients (prefer encryption, not enforce - allows encrypted + unencrypted peers). Usenet: always use SSL/TLS (port 563 vs 119).

**IP leak prevention**: Bind qBittorrent/Deluge network interface to VPN adapter (tun0/wg0). Test with torrent IP checkers. Kill-switch recommended.

**Private vs Public trackers**: Private trackers forbid DHT/PEX (disable in client). Public trackers benefit from DHT/PEX (enable for peer discovery).

### 3. Performance Optimization - Maximum Throughput

**Connection tuning**: Increase global max connections (500-1000), connections per torrent (100-200), upload slots (14-20). Balance: too many connections overwhelm router/disk I/O.

**Bandwidth allocation**: Don't limit upload on home connections (BitTorrent tit-for-tat algorithm penalizes). On seedboxes, set 70-80% of max speed to prevent saturation.

**Port forwarding**: Essential for BitTorrent. Use ports 49160-65534 (avoid default 6881-6889 = ISP throttling target). Verify open with portchecker tools.

**Disk I/O**: Use SSD for incomplete downloads, HDD for long-term seeding. Reduce disk cache if memory-constrained. Sequential download disabled (worse for swarm).

### 4. Automation Integration - *arr Stack Workflows

**Prowlarr**: Centralized indexer manager syncing to Sonarr/Radarr/Lidarr. Configure once, applies to all. Supports both torrent trackers and Usenet indexers.

**Download client patterns**: Sonarr/Radarr send downloads → qBittorrent/SABnzbd → completion triggers import to media library. Use categories for automatic routing.

**Hardlinks**: Enable in *arr apps ("Use Hardlinks instead of Copy"). Seeding continues from download directory, organized copy in media library shares same disk blocks (no duplication).

**Remote path mapping**: Required when download client runs on different machine/Docker container than *arr apps. Maps /downloads on client to /data/downloads on arr.

### 5. Ratio Management - Private Tracker Survival

**Ratio economy**: Upload / Download. Target minimum 1.0. Below tracker requirements = account warning/ban. Freeleech torrents don't count downloads, uploads count = ratio boost.

**Early seeding strategy**: Grab new uploads immediately (few seeders, many leechers = high upload opportunity). Seed popular long-term content for bonus points.

**Seedbox advantage**: 1-10 Gbps dedicated connection + 24/7 uptime = massive ratio gains. Single seedbox month can build 50+ TB upload credit.

**Ratio groups**: Advanced ruTorrent feature - automatically manage seeding rules by ratio threshold. Stop at 2.0 to free disk, continue forever on freeleech, etc.

## Intake Routing

**What is the user trying to do?**

### Setup & Installation

**"Set up qBittorrent optimally"** → [`workflows/setup-bittorrent-client.md`](workflows/setup-bittorrent-client.md)

**"Configure Usenet from scratch"** → [`workflows/setup-usenet-stack.md`](workflows/setup-usenet-stack.md)

**"Install and configure aria2"** → [`workflows/setup-aria2.md`](workflows/setup-aria2.md)

**"Connect Sonarr/Radarr to qBittorrent"** → [`workflows/integrate-arr-stack.md`](workflows/integrate-arr-stack.md)

### Optimization

**"Speed up my torrent client"** → [`workflows/optimize-client-performance.md`](workflows/optimize-client-performance.md)

**"Configure privacy/VPN binding"** → [`workflows/setup-privacy-stack.md`](workflows/setup-privacy-stack.md)

**"Automate with categories"** → [`workflows/automate-categories.md`](workflows/automate-categories.md)

### Troubleshooting

**"Torrents are slow"** → [`workflows/troubleshoot-slow-speeds.md`](workflows/troubleshoot-slow-speeds.md)

**"Torrents stuck at stalled"** → [`workflows/troubleshoot-stalled-torrents.md`](workflows/troubleshoot-stalled-torrents.md)

**"Usenet downloads failing"** → [`workflows/troubleshoot-usenet-failures.md`](workflows/troubleshoot-usenet-failures.md)

### Advanced Operations

**"Manage private tracker ratios"** → [`workflows/manage-private-trackers.md`](workflows/manage-private-trackers.md)

**"Migrate torrents between clients"** → [`workflows/migrate-between-clients.md`](workflows/migrate-between-clients.md)

### Knowledge Questions

**"How does BitTorrent work?"** → [`references/bittorrent-protocol.md`](references/bittorrent-protocol.md)

**"qBittorrent vs Deluge comparison"** → [`references/bittorrent-clients.md`](references/bittorrent-clients.md)

**"What's a Usenet backbone?"** → [`references/usenet-protocol.md`](references/usenet-protocol.md)

**"How do I combine multiple providers?"** → [`references/usenet-providers.md`](references/usenet-providers.md)

## Workflow Index

All workflows follow this pattern:
1. **Required Reading**: Load prerequisite reference files
2. **Process**: Step-by-step implementation
3. **Verification**: How to confirm success
4. **Success Criteria**: Done when...

| Workflow | Purpose | Category |
|----------|---------|----------|
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
