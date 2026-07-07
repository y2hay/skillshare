---

name: p2p-expertise
description: |
  Use when building or optimizing P2P file sharing infrastructure; triggers include "set up qBittorrent", "Usenet stack", "SABnzbd", "arr stack", and "seedbox optimization". Covers BitTorrent, Usenet, aria2, media automation, and performance troubleshooting.
version: 1
metadata:
  migrated_from: build-p2p-infrastructure
  completeness: skeleton
triggers:
  - P2P
  - BitTorrent
  - Usenet
  - seedbox
  - media automation
  - arr stack
when_to_use: crack,firgirl,torrent

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
</intake_routing>

<resources>
<workflows_index>
- **workflows/setup-bittorrent-client.md**: Optimal qBittorrent/Deluge setup
- **workflows/setup-usenet-stack.md**: SABnzbd/NZBGet and provider config
</workflows_index>
</resources>

<usage_notes>
- **Direct Invocation**: Follow workflow step-by-step.
- **Planning**: Load relevant references BEFORE creating an implementation plan.
- **Infrastructure**: Consider Docker/LXC context (e.g., Dockge LXC managing stacks).
</usage_notes>
</skill>
