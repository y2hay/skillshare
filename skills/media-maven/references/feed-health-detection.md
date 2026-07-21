# Feed Health Detection

<overview>
Feed health detection identifies dead, stale, and problematic feeds through HTTP checks, content analysis, and metadata inspection.
</overview>

<health_categories>
## Health Status Categories

**Healthy**:
- HTTP 200 status
- Recent posts (within last 30 days)
- Valid RSS/Atom XML structure
- Fast response time (<3s)

**Stale**:
- HTTP 200 status
- No posts in 90+ days
- Valid XML structure
- May indicate abandoned feed

**Dead**:
- HTTP 404 (Not Found)
- HTTP 410 (Gone)
- Connection timeout (>10s)
- DNS resolution failure
- Invalid XML (parse error)

**Redirected**:
- HTTP 301 (Permanent Redirect)
- HTTP 302 (Temporary Redirect)
- HTTP 308 (Permanent Redirect)
- Extract new URL from Location header

**Slow**:
- HTTP 200 status
- Response time >5 seconds
- May timeout intermittently
- Consider unreliable
</health_categories>

<detection_methods>
## Detection Methods

### 1. HTTP Status Check

```python
import requests

def check_feed_status(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=False)
        return {
            'status': response.status_code,
            'redirect_url': response.headers.get('Location'),
            'last_modified': response.headers.get('Last-Modified'),
            'response_time': response.elapsed.total_seconds()
        }
    except requests.Timeout:
        return {'status': 'timeout'}
    except requests.ConnectionError:
        return {'status': 'connection_error'}
```

### 2. Content Recency Check

Parse feed and check last entry date:

```python
import feedparser
from datetime import datetime, timedelta

def check_content_recency(url):
    feed = feedparser.parse(url)

    if not feed.entries:
        return None

    # Get most recent entry
    latest = feed.entries[0]
    if hasattr(latest, 'published_parsed'):
        pub_date = datetime(*latest.published_parsed[:6])
    elif hasattr(latest, 'updated_parsed'):
        pub_date = datetime(*latest.updated_parsed[:6])
    else:
        return None

    days_ago = (datetime.now() - pub_date).days
    return days_ago
```

### 3. Parse Validation

```python
def validate_feed_structure(url):
    feed = feedparser.parse(url)

    # Check for bozo (malformed feed)
    if feed.bozo:
        return False, feed.bozo_exception

    # Check for required elements
    if not feed.entries:
        return False, "No entries found"

    return True, None
```
</detection_methods>

<thresholds>
## Health Thresholds

**Staleness threshold**: 90 days (3 months)
- Rationale: Most blogs post at least quarterly
- Adjust for specific niches (academic feeds may post less frequently)

**Timeout threshold**: 10 seconds
- Rationale: Feeds should respond quickly
- Slow feeds impact reader startup time

**Response time warning**: 5 seconds
- Flag as "slow" but not dead
- May indicate hosting issues

**HTTP status codes**:
- 200-299: Success (check content recency)
- 300-399: Redirect (follow and update URL)
- 400-499: Client error (dead, except 429 rate limit)
- 500-599: Server error (retry before marking dead)
</thresholds>

<edge_cases>
## Edge Cases

**Seasonal feeds**:
- Some feeds post seasonally (e.g., tax advice blogs)
- Check publication pattern before marking stale

**Podcast feeds**:
- May have longer intervals between episodes
- Use 6-month threshold instead of 3 months

**HTTP 429 (Rate Limit)**:
- Temporary block, not dead
- Retry with exponential backoff

**Cloudflare/Bot Protection**:
- Some feeds block automated requests
- Use proper User-Agent header
- Add delay between requests

**Paywalled content**:
- HTTP 200 but no/limited entries
- Not necessarily dead, may require authentication
</edge_cases>
