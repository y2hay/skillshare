#!/usr/bin/env python3
"""
Parse OPML files and extract feed information.
"""
import xml.etree.ElementTree as ET
import json
import sys
from typing import List, Dict, Optional


def parse_opml(file_path: str) -> List[Dict]:
    """
    Parse OPML file and extract feeds with categories.

    Returns list of feed dicts with:
    - title: Feed title
    - xmlUrl: Feed URL
    - htmlUrl: Website URL (optional)
    - category: Category path (e.g., "Technology > Security")
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    feeds = []

    def traverse_outline(element, category_path=""):
        """Recursively traverse outline elements."""
        for outline in element.findall('outline'):
            # Check if this is a feed or category
            feed_type = outline.get('type', '').lower()
            text = outline.get('text', '')
            xml_url = outline.get('xmlUrl')

            if xml_url:  # This is a feed
                feeds.append({
                    'title': text,
                    'xmlUrl': xml_url,
                    'htmlUrl': outline.get('htmlUrl', ''),
                    'category': category_path.strip(' > ')
                })
            elif text:  # This is a category
                new_path = f"{category_path} > {text}" if category_path else text
                traverse_outline(outline, new_path)

    body = root.find('body')
    if body is not None:
        traverse_outline(body)

    return feeds


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_opml.py <input.opml> [--output feeds.json]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--output' else None

    feeds = parse_opml(input_file)

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(feeds, f, indent=2)
        print(f"Parsed {len(feeds)} feeds to {output_file}")
    else:
        print(json.dumps(feeds, indent=2))


if __name__ == '__main__':
    main()
