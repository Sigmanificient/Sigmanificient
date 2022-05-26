from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = (
	"https://metrics.lecoq.io/Sigmanificient"
	"?template=classic&isocalendar=1&isocalendar.duration=half-year"
	"&config.timezone=Europe%2FParis"
)

r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')

fields = [div.text.strip() for div in soup.find_all('div', class_='field')]


def extract_number(string):
	return int(''.join(ch for ch in string if ch.isdigit()))


DATE_OF_BIRTH = datetime(year=2001, month=12, day=11)
today = datetime.now()

current_age = int((today - DATE_OF_BIRTH).days / 365)

data = {
	k: extract_number(fields[i])
	for (k, i) in {
		'age': current_age,
		'contributed': 4,
		'commits': 5,
		'pr_opened': 7,
		'issues': 8,
		'streak_best': 23,
		'highest': 24,
		'average': 25
	}.items()
}

with open('base.md', 'r') as f:
	base = f.read()

with open('readme.md', 'w') as f:
	f.write(base.format(**data))
