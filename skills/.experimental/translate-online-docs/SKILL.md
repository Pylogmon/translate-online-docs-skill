---
name: translate-online-docs
description: Crawl, preserve, translate, and export online documentation or web books. Use when a user asks Codex to translate an online documentation site, docs portal, web book, tutorial collection, API reference, guide, or any URL-based multi-page publication into a specified language, while preserving structure and optionally producing mdBook or PDF deliverables.
---

# Translate Online Docs

## Overview

Use this skill to turn an online document set into local Markdown, translate it in parallel, and export the translated result as mdBook or PDF when requested.

## Workflow

1. Confirm the target language, start URL, output format (`markdown`, `mdBook`, `PDF`, or both), and crawl scope if the user's request is ambiguous.
2. Read `references/workflow.md` before crawling. It contains agent-led crawl judgment, Defuddle usage, translation batching, and export guidance.
3. Create a project directory with this layout:

```text
<project>/
  source-md/
  translated/<language-code>/
  exports/
  crawl-manifest.json
```

4. Crawl the source by agent judgment, not by a recursive matching script. Convert the start URL with Defuddle, inspect the page's table of contents, sidebar, previous/next links, breadcrumbs, and in-page links, then decide which links are part of the same document or book before fetching them.
5. Maintain `crawl-manifest.json` manually as the crawl proceeds: record each accepted URL, local Markdown path, referring page, reason for inclusion, skipped links with reasons, and failures.
6. Save each accepted page into `source-md/` using a directory structure that mirrors the document's conceptual hierarchy. Prefer the site's own chapter/section order over raw URL shape when they conflict.
7. Translate all Markdown files into `translated/<language-code>/`, preserving the exact relative paths. Use subagents or multi-agent tools when available: assign disjoint file batches, require each worker to preserve Markdown structure, code blocks, links, anchors, frontmatter keys, and file paths.
8. Reconcile the translated tree: ensure every source file has a translated counterpart, internal Markdown links still resolve, and terminology is consistent.
9. If the user asks for mdBook, run `scripts/prepare_mdbook.py` against the translated tree, then build with `mdbook build` if available.
10. If the user asks for PDF, prefer a generated mdBook followed by an installed PDF workflow (`mdbook-pdf`, browser print, or `pandoc`) that fits local tooling. Verify the PDF opens and contains the expected document order.

## Key Rules

- Treat crawl scope as a semantic boundary. Let the agent decide whether each discovered link belongs to the requested document/book using navigation context, content role, and user intent; do not rely on URL-prefix matching alone.
- Save source Markdown before translating. Never translate directly from live pages without a preserved local source tree.
- Keep code blocks, CLI commands, API names, option names, URLs, frontmatter keys, and identifiers unchanged unless the user explicitly asks to localize them.
- Translate prose, headings, captions, admonition text, table prose, and alt text into the requested language.
- Preserve directory structure between `source-md/` and `translated/<language-code>/`; downstream mdBook/PDF generation depends on this.
- Report any skipped pages, failed Defuddle conversions, or tool gaps in the final answer.

## Resources

- `scripts/prepare_mdbook.py`: Copies a translated Markdown tree into an mdBook project and generates `book.toml` plus `src/SUMMARY.md`.
- `references/workflow.md`: Detailed operational guidance for agent-led crawling, translation workers, validation, mdBook, and PDF export.
