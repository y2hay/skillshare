# Workflow: Clean OPML

<required_reading>
**Read these reference files NOW:**
1. references/opml-format.md
2. references/feed-health-detection.md
3. references/redundancy-detection.md
4. references/curated-sources.md
</required_reading>

<process>
## Step 1: Parse Input

Read the OPML/XML file:
```python
python scripts/parse_opml.py input.opml
```

Extract:
- All feed URLs
- Existing categories
- Feed titles and metadata
- OPML structure version

## Step 2: Audit Feed Health

For each feed, run validation:
```python
python scripts/validate_feed.py feed_url
```

Checks:
- HTTP status (200 = healthy, 404/410 = dead, 301/302 = redirected)
- Last-Modified header (>6 months = stale warning)
- Recent entries (parse feed, check last post date)
- Response time (>5s = slow, may be unreliable)

Categorize results:
- **Healthy**: Active, recent content, good response
- **Stale**: No posts in 3+ months
- **Dead**: 404, 410, or timeout
- **Redirected**: 301/302 with new URL
- **Slow**: High latency (>5s response)

## Step 3: Detect Redundancy

Run redundancy detection:
```python
python scripts/detect_redundancy.py feeds.json
```

Checks:
- Exact URL duplicates (keep first occurrence)
- Canonical URL resolution (example.com/feed = example.com/rss)
- Content fingerprinting (compare recent post titles/dates)

Mark duplicates for removal, keep canonical version.

## Step 4: Organize Categories

Apply consistent categorization from references/curated-sources.md:

**Technology**:
- Security → InfoSec, privacy, cryptography
- AI/ML → Machine learning, AI research, LLMs
- Web Dev → Frontend, backend, frameworks
- Systems → Infrastructure, DevOps, databases

**News**: General, tech news, science, politics
**Business**: Startups, finance, SaaS, marketing
**Culture**: Art, music, film, literature, design
**Science**: Research, academia, specific disciplines
**Personal**: Individual bloggers, independent creators

Recategorize misplaced feeds based on content analysis.

## Step 5: Discover Recommendations

For each category, check curated-sources.md for quality niche sources:

**Selection criteria**:
- Consistent posting (1+ posts/month)
- High signal-to-noise ratio (original analysis, not aggregation)
- Established reputation (2+ years active)
- Niche expertise (focused domain, not generalist)

Present 3-5 recommendations per category that aren't already in the feed list.

## Step 6: Generate Clean OPML

Write organized OPML:
```python
python scripts/write_opml.py --input feeds.json --output clean.opml
```

Structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head>
    <title>Curated Feed List</title>
    <dateCreated>2025-02-02T14:30:00Z</dateCreated>
  </head>
  <body>
    <outline text="Technology">
      <outline text="Security">
        <outline type="rss" text="Krebs on Security" xmlUrl="https://krebsonsecurity.com/feed/" htmlUrl="https://krebsonsecurity.com/"/>
      </outline>
    </outline>
  </body>
</opml>
```

Include only:
- Healthy feeds
- Redirected feeds (use new URL)
- Deduplicated canonical versions
- Properly categorized

## Step 7: Generate Report

Create summary markdown:

```markdown
# Feed Curation Report

## Summary
- Total feeds analyzed: X
- Healthy feeds: X
- Stale feeds: X (removed)
- Dead feeds: X (removed)
- Redirected feeds: X (URLs updated)
- Duplicates removed: X

## Removed Feeds
### Dead (404/410)
- [Feed Name](url)

### Stale (>3 months inactive)
- [Feed Name](url) - Last post: YYYY-MM-DD

### Duplicates
- [Feed Name](url) - Duplicate of [Canonical](url)

## Recommended Additions
### Technology > Security
- [Feed Name](url) - Why it's recommended

### Culture > Design
- [Feed Name](url) - Why it's recommended
```

Present report to user with clean OPML for review before importing.
</process>

<success_criteria>
This workflow is complete when:
- [ ] All feeds validated with accurate health status
- [ ] Dead feeds removed, redirected feeds updated
- [ ] Stale feeds (>3 months) identified and removed/flagged
- [ ] All duplicates detected and consolidated
- [ ] Feeds organized into logical categories
- [ ] 3-5 quality recommendations provided per category
- [ ] Clean OPML generated with valid XML structure
- [ ] Summary report shows before/after statistics
- [ ] User can import clean OPML into their feed reader
</success_criteria>
