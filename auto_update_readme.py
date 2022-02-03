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


data = {
	k: extract_number(fields[i])
	for (k, i) in {
		'contributed': 4,
		'commits': 5,
		'pr_opened': 7,
		'issues': 8,
		'streak': 23,
		'streak_best': 24,
		'highest': 25,
		'average': 26
	}.items()
}

with open('base.md', 'r') as f:
	base = f.read()

with open('readme.md', 'w') as f:
	f.write(base.format(**data))
