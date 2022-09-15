import re
from datetime import datetime

import requests

DATE_OF_BIRTH = datetime(year=2001, month=12, day=11)
HTML_FILTER = r'(<.*>)|(\s{2,})|(\{[\s\S]+})'

FIELDS_PATTERNS = {
    'commits': r'\D(\d+)\s?Commits',
    'pr': r'\D(\d+)\s?Pull\D*\sopened',
    'issues': r'\D(\d+)\sIssues\D*\sopened',
    'streak': r'\DBest\sstreak\s(\d+)'
}

URL = (
    "https://metrics.lecoq.io/Sigmanificient"
    "?template=classic&isocalendar=1&isocalendar.duration=half-year"
    "&config.timezone=Europe%2FParis"
)


def compute_age():
    today = datetime.now()
    return int((today - DATE_OF_BIRTH).days / 365)


def main():
    response = requests.get(URL)
    filtered_response = re.sub(HTML_FILTER, '', response.text)

    data = {
        key: re.search(pattern, filtered_response)[1]
        for key, pattern in FIELDS_PATTERNS.items()
    }

    data['age'] = compute_age()

    with open('base.md', 'r') as f:
        base = f.read()

    with open('README.md', 'w') as f:
        f.write(base.format(**data))


if __name__ == '__main__':
    main()
