# Setup BitTorrent Client (qBittorrent/Deluge)

Install and configure qBittorrent or Deluge with optimal settings for performance, privacy, and automation.

## Required Reading

Before starting, load these references for context:

- [`references/bittorrent-clients.md`](../references/bittorrent-clients.md) - Client comparison and selection criteria
- [`references/qbittorrent-optimization.md`](../references/qbittorrent-optimization.md) - qBittorrent specific tuning
- [`references/deluge-optimization.md`](../references/deluge-optimization.md) - Deluge specific tuning
- [`references/network-optimization.md`](../references/network-optimization.md) - Port forwarding and connection tuning

## Process

### Step 1: Choose Client

**qBittorrent** - Recommended for:
- General use, home servers, Docker environments
- Built-in search engine, RSS automation
- Active development, frequent updates
- Lower resource usage than Deluge with many plugins

**Deluge** - Recommended for:
- Advanced users needing extensive customization
- Thin client / headless server setups
- Plugin-based workflows (Labels, AutoAdd, etc.)
- Early seeding performance critical

### Step 2: Installation

**Docker (recommended for your Dockge LXC setup):**

```yaml
# docker-compose.yml
version: "3.8"
services:
  qbittorrent:
    image: linuxserver/qbittorrent:latest
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - WEBUI_PORT=8080
    volumes:
      - /path/to/qbittorrent/config:/config
      - /mnt/mpool/media/data/torrents:/downloads
    ports:
      - 8080:8080
      - 6881:6881
      - 6881:6881/udp
    restart: unless-stopped
```

**Bare metal (Arch Linux):**

```bash
# qBittorrent
sudo pacman -S qbittorrent-nox  # Headless version
systemctl --user enable --now qbittorrent-nox

# Deluge
sudo pacman -S deluge deluged deluge-web
systemctl --user enable --now deluged
systemctl --user enable --now deluge-web
```

### Step 3: Initial Configuration

**Access web UI:**
- qBittorrent: `http://localhost:8080` (default: admin / adminadmin)
- Deluge: `http://localhost:8112` (default: deluge)

**Change default password immediately** (Tools → Options → Web UI → Authentication)

### Step 4: Core Settings (qBittorrent)

**Connection Settings** (Tools → Options → Connection):
- Port: Random port 49160-65534 (avoid default 6881-6889)
- Enable UPnP / NAT-PMP: Check (auto port forwarding if router supports)
- Connections: Global max 500, per torrent 100
- Upload slots: 14

**BitTorrent Settings** (Tools → Options → BitTorrent):
- Enable DHT: Yes (disable for private trackers only)
- Enable PEX: Yes (disable for private trackers only)
- Enable LPD: Yes
- Encryption mode: Prefer encryption (allows encrypted + unencrypted)

**Downloads Settings** (Tools → Options → Downloads):
- Save files to: `/downloads/incomplete` (or your download path)
- Keep incomplete torrents in: `/downloads/incomplete`
- Default Torrent Management Mode: **Automatic** (required for category paths)
- When adding torrent: Do not start download automatically (optional, gives review time)

**Speed Settings** (Tools → Options → Speed):
- Global rate limits: 0 (unlimited) for home connections
- Alternative rate limits: Set if needed for peak hours
- Schedule: Configure if limiting during certain hours

**Advanced Settings** (Tools → Options → Advanced):
- Disk cache: -1 (auto) or manual 512 MB for stability
- Disk cache expiry: 60 seconds
- Enable OS cache: Yes
- Asynchronous I/O threads: 8

### Step 4alt: Core Settings (Deluge)

**Network Settings** (Preferences → Network):
- Incoming Port: Random port 49160-65534
- Outgoing Ports: Random
- Enable UPnP: Yes
- Enable NAT-PMP: Yes
- Connections: Global max 500, per torrent 100

**Plugins** (Preferences → Plugins):
- Enable: Label (for organization), AutoAdd (for watch folders)
- Disable unnecessary plugins (performance impact)

**Queue Settings** (Preferences → Queue):
- Total active: 8
- Total active downloading: 5
- Total active seeding: -1 (unlimited)

### Step 5: Port Forwarding

**Router configuration:**
1. Access router admin (typically 192.168.1.1 or 10.10.0.1)
2. Navigate to Port Forwarding / Virtual Servers
3. Add rule: External port 6881 (or your chosen port) → Internal IP:port
4. Protocol: Both TCP and UDP

**Verify port is open:**
```bash
# Use port checker
curl https://portchecker.co/check?port=6881

# Or use qBittorrent built-in checker
# Tools → Options → Connection → Test port
```

### Step 6: Category Setup (for automation)

**qBittorrent** (Options → Downloads → Category):
```
Category: tv → Save path: /downloads/tv
Category: movies → Save path: /downloads/movies
Category: music → Save path: /downloads/music
Category: books → Save path: /downloads/books
```

**Enable Automatic Torrent Management** for categories to work

### Step 7: RSS Automation (optional)

**qBittorrent** (View → RSS Reader):
1. Add RSS feeds from torrent sites
2. RSS Downloader → Add rule
3. Filter by title regex: `S\d{2}E\d{2}` (matches TV episodes)
4. Assign category, apply to specific feeds
5. Enable automatic downloading

## Verification

**Connection health:**
- Port forwarding working: Green network icon in status bar
- DHT nodes: Should show 100+ nodes after 10 minutes
- Peer exchange working: Torrents should find peers beyond tracker

**Performance baseline:**
- Download a well-seeded public torrent (e.g., Linux ISO)
- Speed should reach 70-90% of your internet connection max
- Upload should be actively sending to peers

**Category automation:**
- Add torrent with specific category
- Verify file saves to category path
- Moving category should move files on disk

## Success Criteria

- [ ] Client installed and accessible via web UI
- [ ] Port forwarding confirmed working (green icon or portchecker)
- [ ] Default password changed
- [ ] Automatic Torrent Management enabled
- [ ] Categories configured for media types
- [ ] Test torrent downloads at expected speeds
- [ ] DHT showing 100+ nodes (if public tracker usage)
- [ ] Upload actively working (not 0 KB/s on all torrents)

## Next Steps

- **Privacy**: See [`setup-privacy-stack.md`](setup-privacy-stack.md) for VPN binding
- **Automation**: See [`integrate-arr-stack.md`](integrate-arr-stack.md) to connect Sonarr/Radarr
- **Optimization**: See [`optimize-client-performance.md`](optimize-client-performance.md) for advanced tuning

## Troubleshooting

**Port shows as closed:**
- Verify router port forwarding rule
- Check firewall isn't blocking (ufw, iptables, Docker network)
- Ensure port matches between client config and router forward

**No DHT nodes:**
- DHT disabled → enable in BitTorrent settings
- Fresh install → wait 10-15 minutes for bootstrap
- Firewall blocking UDP traffic

**Slow speeds on well-seeded torrent:**
- See [`troubleshoot-slow-speeds.md`](troubleshoot-slow-speeds.md)

**Torrents stuck at "Stalled":**
- See [`troubleshoot-stalled-torrents.md`](troubleshoot-stalled-torrents.md)
