"""productive-box gist 내용을 README의 표시 구간에 옮겨 적는다."""
import json
import os
import re
import urllib.request

GIST_ID = "fdca64413c459d510028634a3289883a"
README = "README.md"
START = "<!-- productive-box:start -->"
END = "<!-- productive-box:end -->"


def fetch_gist_file():
    request = urllib.request.Request(
        f"https://api.github.com/gists/{GIST_ID}",
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"},
    )
    with urllib.request.urlopen(request) as response:
        files = json.load(response)["files"]
    first = next(iter(files.values()))
    return first["filename"], first["content"].rstrip()


def build_section(title, content):
    return f"{START}\n**{title}**\n\n```text\n{content}\n```\n{END}"


def main():
    title, content = fetch_gist_file()
    # 아직 productive-box가 한 번도 안 돌았으면 README를 건드리지 않는다
    if title == "productive.md":
        print("gist가 아직 채워지지 않음")
        return
    with open(README, encoding="utf-8") as file:
        readme = file.read()
    pattern = re.compile(re.escape(START) + ".*?" + re.escape(END), re.S)
    updated = pattern.sub(lambda _: build_section(title, content), readme)
    with open(README, "w", encoding="utf-8", newline="\n") as file:
        file.write(updated)


main()
