# Setup Usenet Stack

Complete Usenet configuration from scratch: provider selection, indexer subscription, and SABnzbd/NZBGet installation.

## Required Reading

- [`references/usenet-protocol.md`](../references/usenet-protocol.md) - How Usenet works
- [`references/usenet-providers.md`](../references/usenet-providers.md) - Backbone vs resellers, provider selection
- [`references/trackers-indexers.md`](../references/trackers-indexers.md) - Indexer types and selection
- [`references/sabnzbd-optimization.md`](../references/sabnzbd-optimization.md) - SABnzbd configuration
- [`references/nzbget-optimization.md`](../references/nzbget-optimization.md) - NZBGet configuration

## Process

### Step 1: Understand the Components

You need **both** a provider AND an indexer:

**Usenet Provider** (the "library"):
- Stores the actual binary files on servers
- Measured by retention (days), speed (Mbps), completion (%)
- Examples: Newshosting, UsenetServer, Eweka
- Cost: $5-15/month unlimited or $5-10 per block (pay as you go)

**Usenet Indexer** (the "search engine"):
- Catalogs content and generates NZB files
- NZB = roadmap telling downloader where to find file parts
- Examples: NZBGeek, DOGnzb, NZB.su
- Cost: Free tier limited, $10-20/year VIP

### Step 2: Choose Providers

**Primary provider** (choose one):
- **Newshosting**: UNS Holdings backbone, 5300+ days retention, $8.33/month
- **UsenetServer**: UNS Holdings backbone, 5000+ days retention, good completion
- **Eweka**: Eweka backbone (European), 5000+ days, excellent for EU content

**Backup provider** (different backbone, optional but recommended):
- **Tweaknews**: Tweaknews backbone, block account, fills gaps from primary
- **Vipernews**: Vipernews backbone, block account

**Why different backbones?** Each backbone may be missing different articles due to DMCA takedowns or propagation issues. Combining backbones = higher completion rate.

### Step 3: Choose Indexers

**Start with 2-3 indexers** (redundancy if one goes down):

**Open registration** (check current status, changes frequently):
- **NZBGeek**: Reliable, good API, $12/year VIP
- **NZBFinder**: Premium tier, $10€/year
- **NZB.su**: Free tier available, good for testing

**Invite-only / waitlist**:
- **DOGnzb**: Excellent curation, invite required
- **DrunkenSlug**: Quality indexing, donations for invite

### Step 4: Choose Download Client

**SABnzbd** - Recommended for:
- Ease of use, web UI, extensive plugins
- Better integration with *arr stack
- More active development

**NZBGet** - Recommended for:
- Lower resource usage (C++ vs Python)
- Embedded devices (NAS, Raspberry Pi)
- Faster post-processing

For your Dockge LXC setup, **SABnzbd** recommended (better automation integration).

### Step 5: Install SABnzbd

**Docker compose** (add to your Dockge LXC):

```yaml
version: "3.8"
services:
  sabnzbd:
    image: linuxserver/sabnzbd:latest
    container_name: sabnzbd
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    volumes:
      - /path/to/sabnzbd/config:/config
      - /mnt/mpool/media/data/usenet:/downloads
      - /mnt/mpool/media/data/usenet/incomplete:/incomplete-downloads
    ports:
      - 8080:8080
    restart: unless-stopped
```

**Access**: `http://localhost:8080` after container starts

### Step 6: Configure SABnzbd - Providers

**Add primary provider** (General → Servers):
1. Click `+` to add server
2. Server details (example for Newshosting):
   - Server: `news.newshosting.com`
   - Port: `563` (SSL) **Always use SSL for privacy**
   - Username: Your Newshosting username
   - Password: Your Newshosting password
   - Connections: 30 (adjust based on speed - more connections = faster, but respect provider limits)
   - SSL: Enabled
   - Priority: 0 (highest)

3. Test server (should show green checkmark)

**Add backup provider** (if using):
- Same process, but set Priority: 1 (lower priority, used when primary fails)
- Set connections lower (10-15) since it's backup

**Connections tuning**:
- Start with 10 connections per 10 Mbps of internet speed
- 100 Mbps connection → 30 connections
- Too many connections = provider throttling/banning

### Step 7: Configure SABnzbd - General Settings

**General → Folders**:
- Temporary Download Folder: `/downloads/incomplete`
- Completed Download Folder: `/downloads/complete`
- Minimum Free Space: 10 GB

**General → Switches**:
- Enable HTTPS: Yes (generate self-signed cert or use reverse proxy)
- Ignore Samples: Yes (removes sample files from downloads)
- Unwanted Extensions: `exe, com, bat, cmd` (Windows malware)

### Step 8: Configure SABnzbd - Categories

**Categories** tab:
```
Category: tv
- Folder: /downloads/complete/tv
- Post-processing: +Delete
- Priority: Normal

Category: movies
- Folder: /downloads/complete/movies
- Post-processing: +Delete
- Priority: Normal

Category: books
- Folder: /downloads/complete/books
- Post-processing: +Delete
- Priority: Low
```

**Post-processing options**:
- `+Delete`: Delete source files after extraction (recommended)
- `+Repair`: Use PAR2 files to repair corrupted downloads
- `+Unpack`: Extract archives automatically

### Step 9: Add Indexers to SABnzbd

**General → Indexer** (for API integration):
1. Get API key from your indexer's website (Profile → API)
2. Add indexer (example for NZBGeek):
   - Name: `NZBGeek`
   - URL: `https://api.nzbgeek.info/api`
   - API Key: `your_api_key_here`

Repeat for each indexer.

**Note**: Most indexers will be configured in Prowlarr/Sonarr/Radarr, not directly in SABnzbd. This section is optional if using *arr stack automation.

### Step 10: Test Download

**Manual NZB test**:
1. Visit indexer website (e.g., nzbgeek.info)
2. Search for known good content
3. Download NZB file
4. Upload to SABnzbd via web UI (Upload NZB button)
5. Monitor download progress

**Expected behavior**:
- Download starts immediately
- Multiple parts downloading simultaneously
- PAR2 verification after download completes
- Automatic extraction if archive
- Move to complete folder

### Step 11: Configure Post-Processing

**Config → Switches**:
- Enable PAR2: Yes (automatic repair of corrupted files)
- Enable UnRAR: Yes (automatic extraction)
- Delete RAR files: Yes (save space after extraction)
- Abort jobs that cannot be completed: Yes (don't waste time on hopeless downloads)

**Config → Sorting**:
- Enable TV Sorting: Optional (better handled by Sonarr)
- Enable Movie Sorting: Optional (better handled by Radarr)

Leave sorting disabled if using *arr stack - they handle renaming/organizing better.

## Verification

**Provider connectivity:**
- Test server connection in SABnzbd (should show green checkmark)
- No error messages in SABnzbd logs

**Download functionality:**
- Manual NZB test downloads successfully
- Files extract automatically
- Move to correct category folder

**Performance baseline:**
- Download speed reaches 70-90% of internet max
- Multiple connections working simultaneously
- PAR2 repair working (test with intentionally corrupted download)

## Success Criteria

- [ ] Primary Usenet provider configured and tested
- [ ] Backup provider configured (optional but recommended)
- [ ] At least 2 indexers registered (accounts created)
- [ ] SABnzbd installed and accessible
- [ ] Categories configured for media types
- [ ] Test NZB downloads successfully
- [ ] Post-processing extracts files automatically
- [ ] Download speeds reach expected levels (70-90% of connection max)

## Next Steps

- **Automation**: See [`integrate-arr-stack.md`](integrate-arr-stack.md) to connect Sonarr/Radarr to SABnzbd
- **Optimization**: See [`optimize-client-performance.md`](optimize-client-performance.md) for advanced tuning
- **Troubleshooting**: See [`troubleshoot-usenet-failures.md`](troubleshoot-usenet-failures.md) if downloads fail

## Troubleshooting

**"Failed to connect" errors:**
- Verify SSL port 563 (not 119 unencrypted)
- Check username/password correct
- Firewall blocking outbound connections
- Provider temporarily down (check status page)

**Downloads fail with "Not enough repair blocks":**
- Incomplete upload or DMCA takedown
- Try backup provider on different backbone
- Search newer upload or different release group

**Slow download speeds:**
- Increase connections (test in increments of 10)
- Provider throttling (check account status)
- Disk I/O bottleneck (use `iotop` to monitor)

**PAR2 verification hanging:**
- Corrupted PAR2 files
- Insufficient disk space
- High CPU usage (check `top`)
