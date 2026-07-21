#!/usr/bin/env python3
"""
Generate clean OPML from feed list.
"""
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from typing import List, Dict
import sys
import json


def create_opml(feeds: List[Dict], title: str = "Curated Feed List") -> str:
    """
    Create OPML XML from feed list.

    Feeds should be list of dicts with:
    - title: Feed title
    - xmlUrl: Feed URL
    - htmlUrl: Website URL (optional)
    - category: Category path (e.g., "Technology > Security")
    """
    # Create root element
    opml = ET.Element('opml', version='2.0')

    # Add head
    head = ET.SubElement(opml, 'head')
    ET.SubElement(head, 'title').text = title
    ET.SubElement(head, 'dateCreated').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    # Add body
    body = ET.SubElement(opml, 'body')

    # Organize feeds by category
    categories = {}
    for feed in feeds:
        category_path = feed.get('category', 'Uncategorized')
        if category_path not in categories:
            categories[category_path] = []
        categories[category_path].append(feed)

    # Build category hierarchy
    for category_path in sorted(categories.keys()):
        parts = [p.strip() for p in category_path.split('>')]
        current = body

        # Navigate/create category hierarchy
        for part in parts:
            # Find or create category outline
            found = None
            for child in current.findall('outline'):
                if child.get('text') == part and not child.get('xmlUrl'):
                    found = child
                    break

            if found is None:
                found = ET.SubElement(current, 'outline', text=part)

            current = found

        # Add feeds to this category
        for feed in sorted(categories[category_path], key=lambda f: f['title']):
            attrs = {
                'type': 'rss',
                'text': feed['title'],
                'xmlUrl': feed['xmlUrl']
            }
            if feed.get('htmlUrl'):
                attrs['htmlUrl'] = feed['htmlUrl']

            ET.SubElement(current, 'outline', **attrs)

    # Pretty print
    xml_string = ET.tostring(opml, encoding='utf-8')
    dom = minidom.parseString(xml_string)
    return dom.toprettyxml(indent='  ', encoding='UTF-8').decode('utf-8')


def main():
    if len(sys.argv) < 3:
        print("Usage: write_opml.py --input feeds.json --output clean.opml")
        sys.exit(1)

    input_file = None
    output_file = None

    for i, arg in enumerate(sys.argv):
        if arg == '--input' and i + 1 < len(sys.argv):
            input_file = sys.argv[i + 1]
        elif arg == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]

    if not input_file or not output_file:
        print("Error: Both --input and --output required")
        sys.exit(1)

    with open(input_file) as f:
        feeds = json.load(f)

    opml_content = create_opml(feeds)

    with open(output_file, 'w') as f:
        f.write(opml_content)

    print(f"Wrote {len(feeds)} feeds to {output_file}")


if __name__ == '__main__':
    main()
