# OPML Format Reference

<overview>
OPML (Outline Processor Markup Language) is an XML format for outlines, commonly used for feed subscription lists. Understanding OPML structure is essential for parsing, organizing, and generating feed lists.
</overview>

<structure>
## Basic OPML Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head>
    <title>Feed List Title</title>
    <dateCreated>Mon, 02 Feb 2025 14:30:00 GMT</dateCreated>
    <dateModified>Mon, 02 Feb 2025 14:30:00 GMT</dateModified>
  </head>
  <body>
    <outline text="Category Name">
      <outline text="Subcategory">
        <outline type="rss" text="Feed Title" xmlUrl="https://example.com/feed.xml" htmlUrl="https://example.com/"/>
      </outline>
    </outline>
  </body>
</opml>
```

**Key elements**:
- `<head>` - Metadata about the OPML file
- `<body>` - Contains the outline hierarchy
- `<outline>` - Represents a node (category or feed)

**Outline attributes**:
- `text` - Display name (category name or feed title)
- `type` - Feed type ("rss", "atom", or omitted for categories)
- `xmlUrl` - Feed URL (required for feed entries)
- `htmlUrl` - Website URL (optional but recommended)
</overview>

<parsing_notes>
## Parsing Considerations

**Hierarchical structure**:
- Outlines can nest arbitrarily deep
- Categories = outline without `type` attribute
- Feeds = outline with `type="rss"` or `type="atom"`

**Common patterns**:
```
Technology (category)
  └─ Security (subcategory)
      ├─ Feed 1
      ├─ Feed 2
      └─ Feed 3
```

**Flat vs hierarchical**:
Some OPML files use flat structure (all feeds at root level), others use deep categorization.
</parsing_notes>

<validation>
## OPML Validation

Valid OPML must have:
- XML declaration
- Root `<opml>` element with version attribute
- `<head>` and `<body>` elements
- Feed outlines with `xmlUrl` attribute
- Valid XML escaping for special characters

**Common errors**:
- Missing `xmlUrl` for feed entries
- Invalid XML characters in URLs or titles
- Broken nesting (unclosed outline tags)
- Missing version attribute on `<opml>` tag
</validation>

<generation>
## Generating Clean OPML

Best practices:
- Use OPML version 2.0
- Include creation/modification dates
- Properly escape special characters (&, <, >, ", ')
- Indent for readability (2 spaces per level)
- Include both `xmlUrl` and `htmlUrl` for feeds
- Use descriptive category names
- Sort feeds alphabetically within categories
</generation>
