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
