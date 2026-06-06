# Online Documentation Translation Workflow

## Agent-Led Crawl Scope

Use agent judgment for recursive crawling. URL patterns are clues, not authority. The goal is to reconstruct the requested document or book, not to mirror a website.

Treat a link as part of the same document/book when at least one of these is true:

- It appears in the documentation navigation, table of contents, sidebar, previous/next links, or sitemap for the docs area.
- It is referenced as the next, previous, parent, child, chapter, section, appendix, or required conceptual continuation of the current page.
- It shares title, breadcrumb, product/version selector, layout, and navigation affordances with already accepted pages.
- It is necessary for the requested translation even if its URL shape differs from the current page.
- The user explicitly names it or the surrounding document structure clearly includes it.

Exclude links when they are clearly external, marketing pages, account/login pages, asset downloads, issue trackers, community forums, blog posts, changelogs outside the requested docs, API playgrounds, language/version duplicates not requested, or unrelated site areas.

When uncertain, prefer a small lookahead: fetch or inspect the candidate link title/snippet, then decide. Record the decision and reason in the manifest.

## Defuddle Usage

Primary method:

```bash
curl "https://defuddle.md/<url-without-https-scheme>"
```

The defuddle.md homepage documents this as appending any URL path to `defuddle.md/` and returning Markdown with YAML frontmatter.

CLI fallback when direct API output is poor or unavailable:

```bash
npx defuddle parse "https://example.com/docs/page" --md
```

If the page requires browser-only state, authentication, or heavy client rendering, use an authenticated browser or local HTML capture first, then run Defuddle CLI on the captured HTML.

## Crawling Without a Recursive Script

Maintain a crawl queue yourself:

1. Add the start URL to `pending`.
2. Convert the next pending URL with Defuddle.
3. Save the Markdown to `source-md/` using the book's conceptual structure.
4. Extract candidate links from body content, frontmatter source, headings, navigation links, previous/next links, breadcrumbs, and table of contents.
5. Decide for each candidate whether it belongs to the document/book. Add accepted unseen links to `pending`.
6. Update `crawl-manifest.json` after each page so progress survives interruption.
7. Stop when `pending` is empty or when the user-approved page budget is reached.

Use a manifest shape like this:

```json
{
  "root_url": "https://docs.example.com/start",
  "target_language": "zh-Hans",
  "pages": [
    {
      "url": "https://docs.example.com/start",
      "file": "index.md",
      "referred_by": null,
      "include_reason": "Start URL requested by user"
    }
  ],
  "skipped_links": [
    {
      "url": "https://docs.example.com/blog/post",
      "found_on": "https://docs.example.com/start",
      "skip_reason": "Blog post outside the requested book"
    }
  ],
  "failures": []
}
```

Before translating, inspect the saved tree and manifest for missing chapters, duplicates, version/language mixups, and unrelated pages.

## Translation Workers

Use subagents or multi-agent tools when available. Keep each worker prompt narrow:

```text
Translate these Markdown files from <source language> to <target language>.
Preserve file paths, frontmatter keys, code blocks, inline code, URLs, anchors,
tables, Markdown structure, and all non-prose identifiers. Write outputs to the
matching paths under <translated-dir>. Return a list of completed files and any
uncertain terminology.
```

Batch by file count and size. Avoid splitting one Markdown file across workers unless it is too large to fit; if splitting is necessary, reassemble and review headings, references, and glossary consistency.

Create or maintain a short glossary when the domain has repeated product terms. Share it with all workers and update it only after reviewing conflicts.

## Translation Validation

Check these before export:

- Every source file has a translated file at the same relative path.
- Markdown code fences are balanced.
- YAML frontmatter remains valid; translate values only when they are human-facing prose.
- Internal links resolve within the translated tree.
- Headings are translated, but explicit anchors and link targets are stable.
- Tables still have matching column counts.
- API names, command flags, package names, and code identifiers are unchanged.

## mdBook Export

Prepare an mdBook project. Resolve the script path relative to the skill directory:

- **Claude Code**: `python3 ${CLAUDE_SKILL_DIR}/scripts/prepare_mdbook.py ...`
- **Codex / local**: `python3 scripts/prepare_mdbook.py ...` (when working inside the skill directory)

```bash
python3 scripts/prepare_mdbook.py \
  --translated-dir "work/translated/zh-Hans" \
  --out "work/exports/mdbook" \
  --title "Translated Documentation"
```

Then build if `mdbook` is installed:

```bash
mdbook build "work/exports/mdbook"
```

If `mdbook` is missing and network access is required to install it, ask for approval before installing. Otherwise deliver the prepared mdBook source tree and explain the missing build step.

## PDF Export

Prefer one of these, based on local tooling:

1. Build mdBook, then use an installed mdBook PDF renderer or browser print workflow.
2. Use `pandoc` with the ordered Markdown files from `SUMMARY.md`.
3. Generate HTML from mdBook and print to PDF with a browser automation tool when available.

Always verify that the PDF exists, has nonzero size, opens successfully, and follows the expected chapter order.
