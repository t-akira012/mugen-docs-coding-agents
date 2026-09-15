#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from markdownify import markdownify as to_markdown

ROOT = Path(__file__).resolve().parents[1]
SOURCES_FILE = ROOT / "sources.json"
GENERATED = ROOT / "generated"
USER_AGENT = "mugen-docs-coding-agents/0.1 (+https://github.com/t-akira012/mugen-docs-coding-agents)"
HEADING_RE = re.compile(r"^h([1-6])$")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9._+-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "section"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def clean_soup(html: bytes) -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["script", "style", "noscript"]):
        tag.decompose()
    return soup


def md(fragment: str) -> str:
    text = to_markdown(fragment, heading_style="ATX", bullets="-")
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + "\n"


def heading_level(tag: Tag) -> int | None:
    match = HEADING_RE.match(tag.name or "")
    return int(match.group(1)) if match else None


def section_nodes(heading: Tag) -> list[Tag | NavigableString]:
    level = heading_level(heading)
    assert level is not None
    nodes: list[Tag | NavigableString] = [heading]
    for sibling in heading.next_siblings:
        if isinstance(sibling, Tag):
            sibling_level = heading_level(sibling)
            if sibling_level is not None and sibling_level <= level:
                break
        nodes.append(sibling)
    return nodes


def fragment_html(nodes: list[Tag | NavigableString]) -> str:
    return "".join(str(node) for node in nodes)


def source_fragment(heading: Tag) -> str | None:
    if heading.get("id"):
        return str(heading["id"])
    anchor = heading.find("a")
    if anchor and anchor.get("name"):
        return str(anchor["name"])
    previous = heading.find_previous("a")
    if previous and previous.get("name"):
        return str(previous["name"])
    return None


def build_source(source: dict[str, str], output: Path) -> list[dict[str, object]]:
    source_id = source["id"]
    url = source["url"]
    html = fetch(url)
    soup = clean_soup(html)
    body = soup.body or soup

    full_dir = output / "full"
    section_dir = output / "sections" / source_id
    full_dir.mkdir(parents=True, exist_ok=True)
    section_dir.mkdir(parents=True, exist_ok=True)

    full_path = full_dir / f"{source_id}.md"
    full_path.write_text(md(str(body)), encoding="utf-8")

    entries: list[dict[str, object]] = []
    headings = [tag for tag in body.find_all(["h2", "h3", "h4"]) if tag.get_text(" ", strip=True)]

    for ordinal, heading in enumerate(headings, start=1):
        title = heading.get_text(" ", strip=True)
        level = heading_level(heading)
        section_markdown = md(fragment_html(section_nodes(heading)))
        path = section_dir / f"{ordinal:03d}-{slugify(title)}.md"

        fragment = source_fragment(heading)
        source_url = f"{url}#{fragment}" if fragment else url
        frontmatter = (
            "---\n"
            f"source_id: {source_id}\n"
            f"source_url: {source_url}\n"
            f"heading_level: {level}\n"
            f"title: {json.dumps(title, ensure_ascii=False)}\n"
            "generated: true\n"
            "---\n\n"
        )
        path.write_text(frontmatter + section_markdown, encoding="utf-8")

        entries.append(
            {
                "source_id": source_id,
                "title": title,
                "heading_level": level,
                "path": str(path.relative_to(ROOT)),
                "source_url": source_url,
            }
        )

    return [
        {
            "source_id": source_id,
            "title": source["title"],
            "url": url,
            "sha256": hashlib.sha256(html).hexdigest(),
            "full_markdown": str(full_path.relative_to(ROOT)),
            "sections": entries,
        }
    ]


def load_sources() -> list[dict[str, str]]:
    data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    return data["sources"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an agent-readable local corpus from official Elecbyte docs.")
    parser.add_argument(
        "--only",
        help="Comma-separated source ids, e.g. cns,sctrls,trigger",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete generated output before rebuilding",
    )
    args = parser.parse_args()

    selected = set(args.only.split(",")) if args.only else None
    sources = [source for source in load_sources() if selected is None or source["id"] in selected]

    if selected:
        known = {source["id"] for source in load_sources()}
        unknown = selected - known
        if unknown:
            raise SystemExit(f"Unknown source id(s): {', '.join(sorted(unknown))}")

    if args.clean and GENERATED.exists():
        shutil.rmtree(GENERATED)

    GENERATED.mkdir(parents=True, exist_ok=True)
    built: list[dict[str, object]] = []
    for source in sources:
        print(f"fetching {source['id']}: {source['url']}")
        built.extend(build_source(source, GENERATED))

    index = {
        "schema_version": 1,
        "generated_from": "sources.json",
        "sources": built,
    }
    (GENERATED / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    count = sum(len(item["sections"]) for item in built)
    print(f"built {len(built)} source document(s), {count} section file(s)")
    print(f"index: {GENERATED / 'index.json'}")


if __name__ == "__main__":
    main()
