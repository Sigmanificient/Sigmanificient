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
	n = ''.join(ch for ch in string if ch.isdigit() or ch == '.')
	return int(n) if n.isdigit() else float(n)


data = {
	k: extract_number(fields[i])
	for (k, i) in {
		'contributed': 3,
		'commits': 4,
		'pr_opened': 6,
		'issues': 7,
		'streak_best': 23,
		'highest': 24,
		'average': 25
	}.items()
}

today = datetime.now()
DATE_OF_BIRTH = datetime(year=2001, month=12, day=11)

current_age = int((today - DATE_OF_BIRTH).days / 365)
data['age'] = current_age

with open('base.md', 'r') as f:
	base = f.read()

with open('readme.md', 'w') as f:
	f.write(base.format(**data))
