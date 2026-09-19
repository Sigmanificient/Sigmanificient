import re
from datetime import datetime
from pathlib import Path

import requests

DATE_OF_BIRTH = datetime(year=2001, month=12, day=11)
METRICS_URL = "https://commit-history.com/embed/Sigmanificient"
METRIC_MATCH = r">([\d,]+)\s[^<]+<"
METRICS = {
    "commits": "",
    "pr": "prs",
    "issues": "issues",
    "reviews": "reviews",
}

ICON_URL = (
    "https://raw.githubusercontent.com/mallowigi/iconGenerator/master/assets"
    "/icons/files/"
)
ICON_MATCH = r"&:([\w_]+)"


def compute_age():
    today = datetime.now()
    return int((today - DATE_OF_BIRTH).days / 365)


def fetch_metrics_data() -> dict[str, str]:
    data = {}

    for key, metric in METRICS.items():
        response = requests.get(
            METRICS_URL,
            params={"metric": metric},
            timeout=30,
        )
        response.raise_for_status()

        match = re.search(METRIC_MATCH, response.text)
        if match is None:
            raise RuntimeError(f"Could not extract {metric!r} metric")

        data[key] = match.group(1).replace(",", "")

    return data


def generate_icons(text: str) -> str:
    return re.sub(
        ICON_MATCH,
        rf'<img src="{ICON_URL}\1.svg" width="24px" height="24px"/>',
        text,
    )


def generate_readme(data: dict[str, str]) -> None:
    base = Path("base.md").read_text()
    data["age"] = str(compute_age())

    print('\n'.join(f'- {k}: {v}' for k, v in data.items()))
    Path("README.md").write_text(generate_icons(base).format(**data))


def main():
    generate_readme(fetch_metrics_data())


if __name__ == "__main__":
    main()
