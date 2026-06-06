# Translate Online Docs Skill

This repository packages one Codex skill for publishing and installation from GitHub.

## Skill

- `translate-online-docs`: Crawl an online documentation site or web book by agent judgment, save the source as Markdown, translate it into a target language, and optionally export mdBook or PDF deliverables.

## Repository Layout

```text
skills/
  .experimental/
    translate-online-docs/
      SKILL.md
      LICENSE.txt
      agents/openai.yaml
      references/workflow.md
      scripts/prepare_mdbook.py
```

## Install From GitHub

After publishing this repository, install the skill with Codex:

```text
$skill-installer install https://github.com/<owner>/translate-online-docs-skill/tree/main/skills/.experimental/translate-online-docs
```

Or install by repo and path:

```text
$skill-installer install --repo <owner>/translate-online-docs-skill --path skills/.experimental/translate-online-docs
```

Restart Codex after installation so it can discover the new skill.

## Notes

This skill intentionally leaves recursive crawl decisions to the agent. The bundled script only prepares a translated Markdown tree as an mdBook project.
