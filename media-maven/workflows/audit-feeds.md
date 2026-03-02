# Workflow: Audit Feeds

<required_reading>
**Read these reference files NOW:**
1. references/feed-health-detection.md
2. references/opml-format.md
</required_reading>

<process>
## Step 1: Parse Feed List

Extract feeds from OPML/XML:
```python
python scripts/parse_opml.py input.opml --output feeds.json
```

## Step 2: Validate Each Feed

Run parallel validation:
```python
python scripts/validate_feed.py --input feeds.json --output audit-report.json
```

For each feed URL, check:
- HTTP status code
- Response time
- Last-Modified header
- Feed parse success
- Recent entry count
- Last entry date

## Step 3: Categorize Health Status

**Healthy**:
- HTTP 200
- Recent posts (<1 month)
- Parse success

**Stale**:
- HTTP 200
- No posts in 3+ months
- Parse success

**Dead**:
- HTTP 404, 410, or timeout
- Parse failure

**Redirected**:
- HTTP 301/302
- Extract new URL

**Slow**:
- Response time >5s
- May be unreliable

## Step 4: Generate Report

Create audit summary:
```markdown
# Feed Audit Report

## Statistics
- Total: X feeds
- Healthy: X (Y%)
- Stale: X (Y%)
- Dead: X (Y%)
- Redirected: X
- Slow: X

## Dead Feeds (Remove)
- [Feed Name](url) - 404 Not Found
- [Feed Name](url) - Connection timeout

## Stale Feeds (Review)
- [Feed Name](url) - Last post: 2024-08-15
- [Feed Name](url) - Last post: 2024-09-22

## Redirected Feeds (Update)
- [Feed Name](old-url) → [new-url]

## Slow Feeds (Monitor)
- [Feed Name](url) - Response time: 8.2s
```

Present report to user for review.
</process>

<success_criteria>
Audit is complete when:
- [ ] All feed URLs validated
- [ ] Health status accurately determined
- [ ] Dead feeds identified for removal
- [ ] Stale feeds flagged for review
- [ ] Redirected feeds show new URLs
- [ ] Report generated with clear statistics
</success_criteria>
