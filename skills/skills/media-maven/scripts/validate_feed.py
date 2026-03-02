#!/usr/bin/env python3
"""
Validate RSS/Atom feeds for health status.
"""
import requests
import feedparser
from datetime import datetime, timedelta
from typing import Dict, Optional
import sys
import json


def validate_feed(url: str, timeout: int = 10) -> Dict:
    """
    Check feed health status.

    Returns dict with:
    - status: 'healthy', 'stale', 'dead', 'redirected', 'slow'
    - http_status: HTTP status code
    - response_time: Response time in seconds
    - last_post_date: Date of most recent entry (if available)
    - redirect_url: New URL if redirected
    - error: Error message if failed
    """
    result = {
        'url': url,
        'timestamp': datetime.now().isoformat()
    }

    # HTTP check
    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=False,
            headers={'User-Agent': 'MediaMaven/1.0 (Feed Health Check)'}
        )

        result['http_status'] = response.status_code
        result['response_time'] = response.elapsed.total_seconds()

        # Check for redirect
        if response.status_code in (301, 302, 307, 308):
            result['status'] = 'redirected'
            result['redirect_url'] = response.headers.get('Location', '')
            return result

        # Check for error status
        if response.status_code >= 400:
            result['status'] = 'dead'
            result['error'] = f"HTTP {response.status_code}"
            return result

        # Check response time
        if result['response_time'] > 5.0:
            result['status'] = 'slow'

    except requests.Timeout:
        result['status'] = 'dead'
        result['error'] = 'Connection timeout'
        return result
    except requests.ConnectionError as e:
        result['status'] = 'dead'
        result['error'] = f"Connection error: {str(e)}"
        return result

    # Parse feed content
    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            result['status'] = 'dead'
            result['error'] = f"Parse error: {feed.bozo_exception}"
            return result

        if not feed.entries:
            result['status'] = 'stale'
            result['error'] = 'No entries found'
            return result

        # Check most recent entry
        latest = feed.entries[0]
        pub_date = None

        if hasattr(latest, 'published_parsed') and latest.published_parsed:
            pub_date = datetime(*latest.published_parsed[:6])
        elif hasattr(latest, 'updated_parsed') and latest.updated_parsed:
            pub_date = datetime(*latest.updated_parsed[:6])

        if pub_date:
            result['last_post_date'] = pub_date.isoformat()
            days_ago = (datetime.now() - pub_date).days
            result['days_since_last_post'] = days_ago

            # Determine staleness
            if days_ago > 90:
                result['status'] = 'stale'
            elif result.get('status') != 'slow':
                result['status'] = 'healthy'
        else:
            result['status'] = 'healthy' if result.get('status') != 'slow' else 'slow'

    except Exception as e:
        result['status'] = 'dead'
        result['error'] = f"Feed parse error: {str(e)}"

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_feed.py <feed-url> [--output result.json]")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--output' else None

    print(f"Validating {url}...")
    result = validate_feed(url)

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
