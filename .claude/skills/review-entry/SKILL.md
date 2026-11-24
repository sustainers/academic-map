---
name: review-entry
description: Review a PR (or local change) that adds or edits an entry in universities/, organizations/, research-institutions/, or service-providers/. Checks that the entry is referenced everywhere it should be (_toc.yml, the folder's index.md, member lists like CURIOSS), and catches content problems CI can't, such as broken link markdown or text copied from a sibling entry. Use when asked to review, check, or look at a PR that adds an institution, or invoked as /review-entry <PR number or file>.
---

# Review a new or edited entry

The argument is a PR number, a branch, or a path to an entry file. If none is given, use the files changed on the current branch compared to `origin/main`.

## 1. Gather the change

- For a PR: `gh pr view <n> --json title,author,body,headRefName,headRepositoryOwner,maintainerCanModify,files,statusCheckRollup` and `gh pr diff <n>`.
- If CI failed, read the failing log: `gh run view <run-id> --log-failed`. CI runs `npm run lint`, then `npm run check-toc`, then the link checker.
- Note which entry files are **added** vs **modified**. New entries need every check below; modified entries mainly need steps 3 and 4.

## 2. Run the automated checks locally

Check out the PR branch (`gh pr checkout <n>` or fetch it), then run:

```bash
npm run lint
npm run check-toc
```

`check-toc` (in `scripts/check-toc-completeness.sh`) checks the `_toc.yml` entry, the folder `index.md` entry, and the member lists in `MEMBERSHIP_LISTS`. Local markdownlint may be newer than CI and report `MD059` ("[here]" link text) on many existing files; ignore those unless the PR introduced them.

## 3. Check every place the entry should be referenced

For each new file `<dir>/<slug>.md`, confirm all of these, even if the script passes, because the script doesn't check order or style:

| Where | What to check |
| --- | --- |
| `_toc.yml` | A `- file: <dir>/<slug>.md` line under the right section, in the same alphabetical position as its neighbours. Add a `title:` if siblings use short titles (e.g. `UC San Francisco`). |
| `<dir>/index.md` | A link in the list, alphabetical, matching sibling style. `organizations/index.md` is grouped by category, so pick the closest category and bold the link (bold means "has a page"). If the org is already listed with an external link, replace it with the internal page. |
| Member lists | For each organization in the entry's `*Member of*:` line that has its own page with a member list (currently `organizations/curioss.md`, via `MEMBERSHIP_LISTS` in the script), the entry must be linked there, alphabetically, using the sibling naming style (e.g. `University of California, San Francisco`). |
| Sibling entries | If the institution belongs to a family that already has entries (e.g. other UC campuses, other UT campuses), compare the new entry against one sibling to match field names and structure. |

To find every place a sibling is referenced, which shows where the new one should go:

```bash
grep -rn "<sibling-slug>" --include=*.md --include=*.yml . | grep -v -e node_modules -e _build
```

## 4. Check the content

Read the whole new file and check:

- **Template fields** match siblings: `- *OSPO*:`, `- *Personnel*:`, `- *Link*:`, `- *Member of*:`, then `## General Description`, an activities or objectives section, and `## Primary Contacts`.
- **Link markdown is well formed.** Look for `[text#(url)`, `[text](url` missing `)`, `[text] (url)`, or bare `[text]` with no URL. Neither markdownlint nor the link checker catches these.
- **Every URL resolves:** `curl -s -o /dev/null -w '%{http_code}' -L <url>` for each one.
- **Copied boilerplate.** If the description was copied from a sibling (very common for UC and UT campuses), look for the sibling's name, campus slug, or URL left behind (e.g. a `ucospo.net/santa-barbara/` link in a UCSF entry). Diff against the likely source sibling if it looks similar.
- **Editorial rules** from `contributing.md`: "open source", never "open-source" (the custom lint rule `no-hyphenated-open-source` enforces this, but check headings and link text too).
- **Contacts:** `mailto:` links are well formed and consistent in style.
- **Filename** is lowercase kebab-case and matches the title.

## 5. Report

Give the user one short list of findings, grouped as:

1. **Why CI fails**, if it does, with file:line.
2. **Missing references**: which of `_toc.yml`, `index.md` and member lists need a line, and the exact line to add.
3. **Content problems** CI doesn't catch.
4. **Minor / optional** items, labelled as such.

State which URLs you checked and their status. Don't call the PR ready if anything in 1 to 3 is outstanding.

## 6. If asked to fix

The user's preferred workflow for contributor PRs:

- Make the fixes on the PR's own branch. Check `headRepositoryOwner`: if it's `CURIOSSorg`, push directly. If it's a fork, it needs `maintainerCanModify: true`; otherwise ask whether to leave a review instead.
- Make **one granular commit per fix**, and show the diff and ask for confirmation before each commit.
- If a fix exposes a wider problem (e.g. a member list that is out of order or missing other entries), ask before widening the scope.
- Run `npm run lint` and `npm run check-toc` before asking to push, and ask before pushing.
- Never add Claude or Anthropic attribution to commits, PR text, or comments.
