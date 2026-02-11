import urllib.request
import re

url = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')

    # Find the start of History section and end at Philosophy
    start_marker = 'id="History"'
    end_marker = 'id="Philosophy"'

    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        history_section = html[start_idx:end_idx]
        # Remove HTML tags to get plain text
        clean_text = re.sub('<[^<]+?>', '', history_section)
        # Count 'intelligence' case-insensitively
        count = clean_text.lower().count('intelligence')
        print(count)
    else:
        print('Error: Markers not found')
except Exception as e:
    print(f'Error: {e}')
