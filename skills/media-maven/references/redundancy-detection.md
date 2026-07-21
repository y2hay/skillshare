# Redundancy Detection

<overview>
Redundancy detection identifies duplicate feeds through URL normalization, canonical resolution, and content fingerprinting.
</overview>

<detection_methods>
## Detection Methods

### 1. Exact URL Match

Simplest case: identical URLs in different categories.

```python
from collections import defaultdict

def find_exact_duplicates(feeds):
    url_locations = defaultdict(list)

    for feed in feeds:
        url_locations[feed['xmlUrl']].append(feed)

    duplicates = {url: locs for url, locs in url_locations.items() if len(locs) > 1}
    return duplicates
```

**Resolution**: Keep first occurrence, remove others.

### 2. URL Normalization

Different URLs that point to same feed:

**Common variations**:
- `http://` vs `https://`
- `www.` vs no `www.`
- Trailing slash: `/feed/` vs `/feed`
- Query parameters: `?format=rss` vs empty
- `index.xml` vs directory URL

```python
from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    parsed = urlparse(url)

    # Normalize scheme to https
    scheme = 'https'

    # Remove www. prefix
    netloc = parsed.netloc.lower()
    if netloc.startswith('www.'):
        netloc = netloc[4:]

    # Remove trailing slash
    path = parsed.path.rstrip('/')

    # Remove common query parameters
    query = ''

    # Reconstruct
    normalized = urlunparse((scheme, netloc, path, '', query, ''))
    return normalized
```

### 3. Canonical URL Resolution

Some sites provide multiple feed URLs that serve identical content:

**Common patterns**:
- `example.com/feed` = `example.com/rss` = `example.com/atom`
- `example.com/feed/` = `example.com/index.xml`
- `feeds.example.com/posts` = `example.com/feed`

**Detection method**:
```python
def get_canonical_url(feed_url):
    """
    Fetch feed and check for <link rel="self"> or <atom:link rel="self">
    This is the feed's canonical URL.
    """
    import feedparser

    feed = feedparser.parse(feed_url)

    # Check for self link
    for link in feed.feed.get('links', []):
        if link.get('rel') == 'self':
            return link.get('href')

    # No canonical found, use original URL
    return feed_url
```

### 4. Content Fingerprinting

Compare recent post titles and dates to identify syndicated/aggregated content:

```python
def get_feed_fingerprint(url):
    """
    Create fingerprint from recent post titles and dates.
    """
    import feedparser
    import hashlib

    feed = feedparser.parse(url)

    # Get last 5 entry titles and dates
    entries = feed.entries[:5]
    fingerprint_data = []

    for entry in entries:
        title = entry.get('title', '').lower().strip()
        # Normalize date to day precision
        if hasattr(entry, 'published_parsed'):
            date = entry.published_parsed[:3]  # Year, month, day
        else:
            date = (0, 0, 0)

        fingerprint_data.append((title, date))

    # Hash the fingerprint
    fp_str = str(fingerprint_data)
    return hashlib.md5(fp_str.encode()).hexdigest()


def find_content_duplicates(feeds):
    """
    Find feeds with identical content fingerprints.
    """
    fingerprints = {}
    duplicates = []

    for feed in feeds:
        fp = get_feed_fingerprint(feed['xmlUrl'])
        if fp in fingerprints:
            duplicates.append((feed, fingerprints[fp]))
        else:
            fingerprints[fp] = feed

    return duplicates
```

**Use cases**:
- Aggregator sites that republish content
- Content scrapers
- Syndication networks (same content, different domains)
</detection_methods>

<resolution_strategy>
## Resolution Strategy

When duplicates detected, choose which to keep:

**Priority order**:
1. **Official domain** over aggregators
   - `example.com/feed` > `aggregator.com/example-feed`

2. **HTTPS** over HTTP
   - `https://example.com/feed` > `http://example.com/feed`

3. **Canonical URL** over alternates
   - Feed's self-declared canonical

4. **First occurrence** if no clear winner
   - Keep feed as it appears first in OPML

5. **More complete URL** (with htmlUrl)
   - Prefer feeds with both xmlUrl and htmlUrl
</resolution_strategy>

<output_format>
## Duplicate Report Format

```markdown
## Duplicates Detected: X

### Exact Match
- [Feed Title](url) appears in:
  - Category A
  - Category B
  **Resolution**: Kept in Category A (first occurrence)

### URL Normalization
- [Feed Title](http://example.com/feed/)
- [Feed Title](https://www.example.com/feed)
  **Resolution**: Consolidated to https://example.com/feed

### Content Fingerprint
- [Feed Title A](url-a)
- [Feed Title B](url-b)
  **Same content - aggregator detected**
  **Resolution**: Kept Feed A (official domain)
```
</output_format>
