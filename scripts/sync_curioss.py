#!/usr/bin/env python3
"""Fetch member and funding data from curioss.org before building the map.

curioss.org is the source of truth for two lists the map shows:

- data/members.yml: CURIOSS member institutions and their logos. A member
  with a `mapPage` gets its logo shown on that page of the map.
- data/funding-opportunities.yml: funding calls. A call with `mapPages`
  is listed on those pages of the map while it is open.

This script downloads both files and the member logos into _curioss/
(git-ignored), where the curioss_data Sphinx extension (_ext/) reads them
during the build. Nothing is copied into the repository by hand, so the map
can't drift from curioss.org: every build uses the current lists.

It also reports where the two sites disagree, as warnings (not errors, so a
change on curioss.org can't block a deploy here):

- a mapPage or mapPages entry that doesn't match a page in the map;
- a member whose map page doesn't list CURIOSS under "Member of";
- a map page that lists CURIOSS under "Member of" but isn't in members.yml.

Usage:
    python scripts/sync_curioss.py

Environment variables:
    CURIOSS_REF       Branch, tag, or commit of CURIOSSorg/curioss.org to read
                      (default: main).
    CURIOSS_DATA_DIR  Read members.yml, funding-opportunities.yml, and logos
                      from a local curioss.org checkout instead of GitHub.
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_curioss"
REF = os.environ.get("CURIOSS_REF", "main")
LOCAL = os.environ.get("CURIOSS_DATA_DIR")
RAW = f"https://raw.githubusercontent.com/CURIOSSorg/curioss.org/{REF}/"
SECTIONS = ("universities", "research-institutions", "organizations", "service-providers")
IN_CI = os.environ.get("GITHUB_ACTIONS") == "true"


def warn(message, file=None):
    if IN_CI:
        location = f" file={file}" if file else ""
        print(f"::warning{location}::{message}")
    else:
        print(f"warning: {message}", file=sys.stderr)


def fetch(path):
    """Return the bytes of a file in the curioss.org repository."""
    if LOCAL:
        return (Path(LOCAL) / path).read_bytes()
    url = RAW + urllib.parse.quote(path)
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


def member_of_curioss(page):
    """True if a map page lists CURIOSS on its "Member of" line."""
    text = (ROOT / f"{page}.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        if re.search(r"\*Member\*? ?of\*?:", line):
            return "CURIOSS" in line
    return False


def pages_claiming_curioss():
    pages = set()
    for section in SECTIONS:
        for path in sorted((ROOT / section).glob("*.md")):
            page = f"{section}/{path.stem}"
            if path.stem != "index" and member_of_curioss(page):
                pages.add(page)
    return pages


def sync_members():
    data = yaml.safe_load(fetch("data/members.yml"))
    logos = OUT / "logos"
    logos.mkdir(parents=True, exist_ok=True)

    members = []
    for member in data["members"]:
        logo = member["logo"]
        filename = Path(logo).name
        (logos / filename).write_bytes(fetch("static" + logo))
        page = member.get("mapPage")
        if page and not (ROOT / f"{page}.md").exists():
            warn(f"curioss.org members.yml: mapPage '{page}' for {member['name']} "
                 "is not a page in the map", "_curioss/members.json")
            page = None
        members.append({
            "name": member["name"],
            "url": member["url"],
            "logo": f"_curioss/logos/{filename}",
            "mapPage": page,
        })

    linked = {m["mapPage"] for m in members if m["mapPage"]}
    for member in members:
        page = member["mapPage"]
        if page and not member_of_curioss(page):
            warn(f"{page}.md is a CURIOSS member on curioss.org, but its "
                 "'Member of' line doesn't list CURIOSS", f"{page}.md")
    for page in sorted(pages_claiming_curioss() - linked):
        warn(f"{page}.md lists CURIOSS under 'Member of', but no member in "
             "curioss.org's data/members.yml has that mapPage", f"{page}.md")

    (OUT / "members.json").write_text(json.dumps(members, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8")
    with_page = sum(1 for m in members if m["mapPage"])
    print(f"Synced {len(members)} CURIOSS members ({with_page} with map pages).")


def sync_funding():
    data = yaml.safe_load(fetch("data/funding-opportunities.yml"))
    calls = []
    for call in data["opportunities"]:
        if str(call.get("status") or "").strip().lower() == "closed":
            continue
        pages = []
        for page in call.get("mapPages") or []:
            if (ROOT / f"{page}.md").exists():
                pages.append(page)
            else:
                warn(f"curioss.org funding-opportunities.yml: mapPages entry '{page}' "
                     f"for '{call['title']}' is not a page in the map", "_curioss/funding.json")
        calls.append({
            "title": call["title"],
            "funder": call["funder"],
            "url": call["url"],
            "amount": call.get("amount") or "",
            "deadline": call.get("deadline") or "",
            "deadlineSort": str(call.get("deadlineSort") or ""),
            "mapPages": pages,
        })
    calls.sort(key=lambda c: (c["deadlineSort"] or "9999", c["title"].lower()))
    (OUT / "funding.json").write_text(json.dumps(calls, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8")
    with_page = sum(1 for c in calls if c["mapPages"])
    print(f"Synced {len(calls)} open funding calls ({with_page} shown on funder pages).")


def main():
    OUT.mkdir(exist_ok=True)
    source = LOCAL or f"CURIOSSorg/curioss.org@{REF}"
    print(f"Reading CURIOSS data from {source}")
    sync_members()
    sync_funding()


if __name__ == "__main__":
    main()
