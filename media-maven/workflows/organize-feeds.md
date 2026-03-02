# Workflow: Organize Feeds

<required_reading>
**Read these reference files NOW:**
1. references/redundancy-detection.md
2. references/curated-sources.md (for category definitions)
</required_reading>

<process>
## Step 1: Load Feed List

Parse existing OPML with categories:
```python
python scripts/parse_opml.py input.opml --output feeds.json
```

## Step 2: Detect Redundancy

Run redundancy detection:
```python
python scripts/detect_redundancy.py feeds.json --output duplicates.json
```

Methods:
- **Exact URL match** - Same URL in different categories
- **Canonical resolution** - example.com/feed = example.com/rss
- **Content fingerprinting** - Compare recent post titles/dates

Mark duplicates, keep canonical version (usually first occurrence).

## Step 3: Categorize Feeds

Apply consistent categorization from curated-sources.md:

**Technology**:
- Security (InfoSec, privacy, cryptography)
- AI/ML (machine learning, LLMs, AI research)
- Web Dev (frontend, backend, frameworks)
- Systems (infrastructure, DevOps, databases)

**News**: General, tech news, science, politics
**Business**: Startups, finance, SaaS, marketing
**Culture**: Art, music, film, literature, design
**Science**: Research, academia, specific disciplines
**Personal**: Individual bloggers, independent creators

Analyze feed content to determine best fit category.

## Step 4: Generate Organized OPML

Write structured OPML with categories:
```python
python scripts/write_opml.py --input feeds.json --output organized.opml
```

Structure:
```xml
<opml version="2.0">
  <body>
    <outline text="Technology">
      <outline text="Security">
        <outline type="rss" text="Feed Name" xmlUrl="..." htmlUrl="..."/>
      </outline>
      <outline text="AI/ML">
        <outline type="rss" text="Feed Name" xmlUrl="..." htmlUrl="..."/>
      </outline>
    </outline>
  </body>
</opml>
```

## Step 5: Document Changes

Create summary report:
```markdown
# Organization Report

## Duplicates Removed: X
- [Feed Name](url) → Duplicate of [Canonical](url)

## Recategorized: X
- [Feed Name] moved from "Old Category" to "New Category"

## Categories
### Technology > Security (X feeds)
### Technology > AI/ML (X feeds)
### News > Tech (X feeds)
...
```
</process>

<success_criteria>
Organization is complete when:
- [ ] All duplicates detected and removed
- [ ] Feeds categorized logically
- [ ] OPML has clean hierarchical structure
- [ ] Changes documented in report
- [ ] Output OPML is valid and importable
</success_criteria>
