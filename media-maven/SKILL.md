---
name: media-maven
description: Curate RSS/OPML feeds by parsing files, validating feed health, detecting stale/redundant sources, organizing into categories, and recommending quality niche sources. Use when managing RSS subscriptions, cleaning feed lists, or discovering new sources.
---

<skill>
<objective>
Curate RSS/OPML feeds by parsing files, validating feed health, detecting stale/redundant sources, organizing into categories, and recommending quality niche sources.
</objective>

<quick_start>
Provide an OPML file or RSS URL to audit, organize, or clean. Media Maven will validate health, deduplicate, and suggest quality niche sources.
</quick_start>

<essential_principles>
<how_media_maven_works>
<feed_health_detection>
Media maven fetches live feeds to check:
- **HTTP status** (404, 410, timeout = dead feed)
- **Last modified date** (>6 months = potentially stale)
- **Recent entries** (no posts in 3+ months = inactive)
- **Redirect chains** (updated feed URL)
</feed_health_detection>

<redundancy_detection>
Identifies duplicate feeds by:
- **Exact URL match** (same feed, different category)
- **Canonical URL resolution** (example.com/feed vs example.com/rss)
- **Content fingerprinting** (same posts, different URLs - scrapers/aggregators)
</redundancy_detection>

<category_organization>
Applies consistent categorization:
- Technology (security, AI/ML, web dev, systems)
- News (general, tech, science, politics)
- Business (startups, finance, marketing)
- Culture (art, music, film, literature)
- Science (research, academia, specific fields)
- Personal (individual bloggers, creators)
</category_organization>

<source_discovery>
Curated library of quality niche sources organized by category. Updated recommendations based on reputation, consistency, and signal-to-noise ratio.
</source_discovery>
</how_media_maven_works>
</essential_principles>

<intake>
What would you like to do?

1. **Audit existing feeds** - Check health, find stale/dead feeds
2. **Organize feeds** - Categorize and deduplicate
3. **Discover new sources** - Get recommendations for categories
4. **Clean OPML** - Full audit + organization + discovery
5. Something else

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "audit", "check", "health", "stale" | workflows/audit-feeds.md |
| 2, "organize", "categorize", "dedupe" | workflows/organize-feeds.md |
| 3, "discover", "recommend", "find", "new" | workflows/discover-sources.md |
| 4, "clean", "full", "everything", "complete" | workflows/clean-opml.md |
| 5, other | Clarify intent, then route |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
All domain knowledge in `references/`:

**Formats**: opml-format.md, rss-atom-formats.md
**Detection**: feed-health-detection.md, redundancy-detection.md
**Sources**: curated-sources.md (quality niche feeds by category)
**Patterns**: common-issues.md
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| audit-feeds.md | Validate feed health, identify stale/dead feeds |
| organize-feeds.md | Categorize and deduplicate feed list |
| discover-sources.md | Recommend quality niche sources by category |
| clean-opml.md | Full pipeline: audit → organize → discover → output |
</workflows_index>

<scripts_index>
Utility scripts in `scripts/`:

- **fetch_feed.py** - HTTP fetching with timeout, redirect handling
- **parse_opml.py** - OPML parsing and structure validation
- **validate_feed.py** - Feed health checks (status, recency, content)
- **write_opml.py** - Generate clean OPML with proper structure
</scripts_index>

<success_criteria>
Media maven is working when:
- Live feed validation completes with accurate health status
- Stale feeds (>3 months inactive) are identified correctly
- Redundant feeds are detected and consolidated
- Categories are logically organized and consistent
- Curated source recommendations are relevant and high-quality
- Output OPML is valid, well-structured, and importable
</success_criteria>
</skill>
