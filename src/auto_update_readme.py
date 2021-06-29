from datetime import datetime

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://github-readme-stats.vercel.app"
GH_STAT_LINK = f"{BASE_URL}/api?username=Sigmanificient"
GH_TOP_LANGUAGES_LINK = f"{BASE_URL}/api/top-langs/?username=Sigmanificient&layout=compact&langs_count=10"
GH_COMMIT_STAT_URL = 'https://metrics.lecoq.io/Sigmanificient?template=classic&isocalendar=1&isocalendar.duration' \
                     '=half-year&config.timezone=Europe%2FParis '

# Github stats
github_stat = requests.get(GH_STAT_LINK)
soup = BeautifulSoup(github_stat.content, "html.parser")

svg_vars = {t.attrs["data-testid"]: t.text for t in soup.find_all('text', class_="stat") if t.has_attr("data-testid")}
svg_vars['L'] = soup.find('g', class_="rank-text").text.replace(' ', '').strip()
svg_vars['year'] = str(datetime.now().year)

# top languages
top_languages = requests.get(GH_TOP_LANGUAGES_LINK)
soup = BeautifulSoup(top_languages.content, "html.parser")

languages = []
for g in soup.find_all('g'):
    children = [child for child in g.children if not (isinstance(child, str))]
    if len(children) != 2:
        continue

    languages.append(children)

last = len(languages) - 1
for c, lang in enumerate(languages):
    circle, text = lang
    name, percent = text.text.strip().split()

    svg_vars[f'l{c}-col'] = circle.attrs['fill']
    svg_vars[f'lang_{c}'] = name
    svg_vars[f'l{c}-w'] = percent

while c <= 9:
    svg_vars[f'lang_{c}'] = 'empty'
    c += 1

# commits stats
commits_stats = requests.get(GH_COMMIT_STAT_URL)
soup = BeautifulSoup(commits_stats.content, "html.parser")


stats = [x.text.strip() for x in soup.find_all('div', class_='field')]
streak, commit_avg = stats[-3], stats[-1]

streak = ''.join(c for c in streak if c.isdigit() or c == '.')
commit_avg = ''.join(c for c in commit_avg if c.isdigit() or c == '.')

svg_vars['streak'] = streak
svg_vars['cmt_avg'] = commit_avg

with open("../src/web/base.svg") as f:
    svg = f.read()

for k, v in svg_vars.items():
    svg = svg.replace(f'#{k}', v)

svg = svg.replace('<p>empty</p>', '')

with open("../readme.svg", "w") as f:
    f.write(svg)
