"""productive-box gist 내용을 README의 표시 구간에 옮겨 적는다."""
import re
import urllib.request

# raw 주소는 API 토큰 없이 읽을 수 있다 (Actions 기본 토큰은 gist API에서 403)
GIST_RAW_URL = "https://gist.githubusercontent.com/shinyena00/fdca64413c459d510028634a3289883a/raw"
README = "README.md"
START = "<!-- productive-box:start -->"
END = "<!-- productive-box:end -->"


def fetch_gist_content():
    with urllib.request.urlopen(GIST_RAW_URL) as response:
        return response.read().decode("utf-8").rstrip()


def find_percentages(content):
    """줄 순서는 Morning, Daytime, Evening, Night (productive-box 고정 순서)"""
    return [float(value) for value in re.findall(r"([\d.]+)%", content)]


def build_title(percentages):
    # productive-box가 gist 제목을 정하는 규칙과 같다
    morning, daytime, evening, night = percentages
    return "I'm an early 🐤" if morning + daytime > evening + night else "I'm a night 🦉"


def build_section(title, content):
    return f"{START}\n**{title}**\n\n```text\n{content}\n```\n{END}"


def main():
    content = fetch_gist_content()
    percentages = find_percentages(content)
    # 아직 productive-box가 한 번도 안 돌았으면 README를 건드리지 않는다
    if len(percentages) != 4:
        print("gist가 아직 채워지지 않음")
        return
    with open(README, encoding="utf-8") as file:
        readme = file.read()
    pattern = re.compile(re.escape(START) + ".*?" + re.escape(END), re.S)
    section = build_section(build_title(percentages), content)
    updated = pattern.sub(lambda _: section, readme)
    with open(README, "w", encoding="utf-8", newline="\n") as file:
        file.write(updated)


main()
