"""Show CURIOSS member logos and open funding calls on map pages.

Reads the files scripts/sync_curioss.py writes to _curioss/ and adds, while
each page is read (so the Markdown files themselves never change):

- on each CURIOSS member's page: the member's logo, under the title;
- on each funder page named in a call's mapPages: an "Open funding calls"
  section, before the page's first second-level heading;
- on funders/index: an "Open funding calls" section listing every open call.

If _curioss/ is missing (scripts/sync_curioss.py hasn't been run), the build
still works, without logos or calls, and prints one warning.
"""

import json
import re
from pathlib import Path

from sphinx.util import logging

logger = logging.getLogger(__name__)

FUNDING_LIST = "https://curioss.org/resources/funding-opportunities/"
FUNDERS_INDEX = "funders/index"


def load(app):
    folder = Path(app.srcdir) / "_curioss"
    members_file = folder / "members.json"
    funding_file = folder / "funding.json"
    if not members_file.exists() or not funding_file.exists():
        logger.warning("CURIOSS data not found in _curioss/; building without member "
                       "logos and funding calls. Run scripts/sync_curioss.py first.")
        app.curioss_members, app.curioss_calls = {}, {}
        app.curioss_all_calls = []
        return

    members = json.loads(members_file.read_text(encoding="utf-8"))
    app.curioss_members = {m["mapPage"]: m for m in members if m["mapPage"]}

    calls = json.loads(funding_file.read_text(encoding="utf-8"))
    app.curioss_all_calls = calls
    app.curioss_calls = {}
    for call in calls:
        for page in call["mapPages"]:
            app.curioss_calls.setdefault(page, []).append(call)


def escape(text):
    # $ too: this book enables MyST's dollarmath, so "$300 ... $500" would become math.
    return re.sub(r"([\[\]*_`$])", r"\\\1", text)


def call_line(call, with_funder=False, docname=None):
    line = f"- **[{escape(call['title'])}]({call['url']})**"
    if with_funder:
        funder = escape(call["funder"])
        if call["mapPages"] and docname:
            depth = docname.count("/")
            funder = f"[{funder}]({'../' * depth}{call['mapPages'][-1]}.md)"
        line += f", {funder}"
    details = []
    if call["amount"]:
        details.append(escape(call["amount"]))
    if call["deadline"]:
        details.append(f"Deadline: {escape(call['deadline'])}")
    if details:
        line += ". " + ". ".join(details)
    return line + "\n"


def page_title(text):
    """The page's own title, as plain text, or None."""
    match = re.search(r"^# (.*)$", text, flags=re.M)
    if not match:
        return None
    title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", match.group(1))
    return re.sub(r"[*_`]", "", title).strip() or None


def logo_block(member, title):
    # Use the map's title for the alt text, so it matches the page.
    return (
        f"```{{image}} /{member['logo']}\n"
        f":alt: {title or member['name']} logo\n"
        f":class: curioss-member-logo\n"
        f"```\n"
    )


def calls_block(calls, intro, with_funder=False, docname=None):
    lines = ["## Open funding calls\n", "\n", intro, "\n"]
    lines += [call_line(c, with_funder, docname) for c in calls]
    return "".join(lines) + "\n"


def insert_after_title(text, block):
    match = re.search(r"^# .*\n", text, flags=re.M)
    if not match:
        return block + "\n" + text
    return text[:match.end()] + "\n" + block + "\n" + text[match.end():]


def insert_before_first_section(text, block):
    match = re.search(r"^## ", text, flags=re.M)
    if not match:
        return text.rstrip("\n") + "\n\n" + block
    return text[:match.start()] + block + "\n" + text[match.start():]


def source_read(app, docname, source):
    text = source[0]
    member = app.curioss_members.get(docname)
    if member:
        text = insert_after_title(text, logo_block(member, page_title(text)))

    calls = app.curioss_calls.get(docname)
    if calls:
        intro = (f"These calls are open now, from CURIOSS's "
                 f"[list of funding opportunities]({FUNDING_LIST}).\n")
        text = insert_before_first_section(text, calls_block(calls, intro))

    if docname == FUNDERS_INDEX and app.curioss_all_calls:
        intro = (f"Every call that is open now in CURIOSS's "
                 f"[list of funding opportunities]({FUNDING_LIST}), soonest deadline first.\n")
        block = calls_block(app.curioss_all_calls, intro, with_funder=True, docname=docname)
        text = text.rstrip("\n") + "\n\n" + block

    source[0] = text


def outdated(app, env, added, changed, removed):
    """Re-read every page the data touches, so incremental builds pick up new data."""
    pages = set(app.curioss_members) | set(app.curioss_calls)
    if app.curioss_all_calls:
        pages.add(FUNDERS_INDEX)
    return [p for p in pages if p in env.found_docs]


def setup(app):
    app.connect("builder-inited", load)
    app.connect("source-read", source_read)
    app.connect("env-get-outdated", outdated)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
