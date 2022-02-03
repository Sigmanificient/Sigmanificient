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

data = {
	'contributed': fields[4],
	'commits': fields[5],
	'pr_opened': fields[7],
	'issues': fields[8],
	'streak': fields[23],
	'streak_best': fields[24],
	'highest': fields[25],
	'average': fields[26]
}

with open('base.md', 'r') as f:
	base = f.read()

with open('readme.md', 'w') as f:
	f.write(base.format(**data))
