"""productive-box gist 내용을 GitHub Stats 카드와 같은 모양의 SVG로 그린다."""
import re
import time
import urllib.request
from html import escape

# raw 주소는 API 토큰 없이 읽을 수 있다 (Actions 기본 토큰은 gist API에서 403)
GIST_RAW_URL = "https://gist.githubusercontent.com/shinyena00/fdca64413c459d510028634a3289883a/raw"
OUTPUT = "productive-box.svg"
LINE_PATTERN = re.compile(r"^(\S+)\s+(\w+)\s+(\d+) commits.*?([\d.]+)%\s*$")

# github-readme-stats 카드와 크기·색을 맞춘다 (README에서 같은 크기로 띄움)
WIDTH, HEIGHT = 304, 145
BAR_X, BAR_WIDTH = 120, 110


def fetch_gist_content():
    # raw 주소는 몇 분간 캐시되므로 매번 다른 주소로 요청한다
    with urllib.request.urlopen(f"{GIST_RAW_URL}?t={int(time.time())}") as response:
        return response.read().decode("utf-8")


def parse_rows(content):
    """줄 순서는 Morning, Daytime, Evening, Night (productive-box 고정 순서)"""
    rows = []
    for line in content.splitlines():
        match = LINE_PATTERN.match(line.strip())
        if match:
            emoji, label, commits, percent = match.groups()
            rows.append((emoji, label, int(commits), float(percent)))
    return rows


def build_title(rows):
    # productive-box가 gist 제목을 정하는 규칙과 같다
    morning, daytime, evening, night = (row[3] for row in rows)
    return "I'm an early 🐤" if morning + daytime > evening + night else "I'm a night 🦉"


def build_row(index, row):
    emoji, label, commits, percent = row
    y = 62 + index * 21
    fill_width = BAR_WIDTH * percent / 100
    return (
        f'<text x="25" y="{y}" class="label">{escape(emoji)} {escape(label)}</text>'
        f'<rect x="{BAR_X}" y="{y - 8}" width="{BAR_WIDTH}" height="8" fill="#e5e7eb"/>'
        f'<rect x="{BAR_X}" y="{y - 8}" width="{fill_width:.1f}" height="8" fill="#22C55E"/>'
        f'<text x="279" y="{y}" class="value" text-anchor="end">{percent:.1f}%</text>'
    )


def build_svg(rows):
    body = "".join(build_row(index, row) for index, row in enumerate(rows))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<style>
.title {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #111827; }}
.label {{ font: 600 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #4b5563; }}
.value {{ font: 600 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #4b5563; }}
</style>
<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" fill="#ffffff" stroke="#e5e7eb"/>
<text x="25" y="35" class="title">{escape(build_title(rows))}</text>
{body}
</svg>
"""


def main():
    rows = parse_rows(fetch_gist_content())
    # 아직 productive-box가 한 번도 안 돌았으면 그림을 건드리지 않는다
    if len(rows) != 4:
        print("gist가 아직 채워지지 않음")
        return
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as file:
        file.write(build_svg(rows))


main()
