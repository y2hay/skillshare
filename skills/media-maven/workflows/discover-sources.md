# Workflow: Discover Sources

<required_reading>
**Read these reference files NOW:**
1. references/curated-sources.md
</required_reading>

<process>
## Step 1: Identify Existing Categories

Parse current feed list to see what categories exist:
```python
python scripts/parse_opml.py input.opml --categories-only
```

## Step 2: Load Curated Recommendations

From curated-sources.md, load quality niche sources organized by category.

**Selection criteria**:
- Consistent posting (1+ posts/month)
- High signal-to-noise ratio (original analysis, not aggregation)
- Established reputation (2+ years active)
- Niche expertise (focused domain, not generalist)
- Lesser known (avoid mainstream sources already widely known)

## Step 3: Compare Against Existing Feeds

For each category in the user's feed list, filter curated sources:
- Exclude URLs already in user's feed list
- Exclude domains already represented
- Prioritize complementary perspectives

## Step 4: Generate Recommendations

Present 3-5 recommendations per category:

```markdown
# Recommended Feed Additions

## Technology > Security
### Krebs on Security
- **URL**: https://krebsonsecurity.com/feed/
- **Why**: In-depth investigative journalism on cybercrime, data breaches
- **Frequency**: 2-3 posts/week
- **Active since**: 2009

### Schneier on Security
- **URL**: https://www.schneier.com/feed/
- **Why**: Expert analysis of security, cryptography, privacy policy
- **Frequency**: Daily
- **Active since**: 2004

## Culture > Design
### It's Nice That
- **URL**: https://www.itsnicethat.com/feed
- **Why**: Emerging creative talent across disciplines
- **Frequency**: Daily
- **Active since**: 2007
```

## Step 5: Optional OPML Export

Offer to create OPML file with just recommendations:
```python
python scripts/write_opml.py --recommendations recommendations.json --output recommended-feeds.opml
```

User can selectively import recommended feeds.
</process>

<success_criteria>
Discovery is complete when:
- [ ] Existing categories identified
- [ ] Curated sources loaded and filtered
- [ ] 3-5 quality recommendations per category
- [ ] Recommendations exclude existing feeds
- [ ] Each recommendation includes URL, description, rationale
- [ ] Optional OPML export available for easy import
</success_criteria>
