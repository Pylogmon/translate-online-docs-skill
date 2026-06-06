# Translate Online Docs Skill

A universal agent skill ([Agent Skills standard](https://agentskills.io)) for crawling, translating, and exporting online documentation. Compatible with **Claude Code** and **OpenAI Codex**.

## Skill

- `translate-online-docs`: Crawl an online documentation site or web book by agent judgment, save the source as Markdown, translate it into a target language, and optionally export mdBook or PDF deliverables.

## Repository Layout

```text
translate-online-docs-skill/
  SKILL.md                   # Skill manifest (Agent Skills standard)
  LICENSE.txt
  README.md
  agents/openai.yaml         # Codex agent interface config
  references/workflow.md     # Operational runbook for the agent
  scripts/prepare_mdbook.py  # mdBook project scaffolding script
```

## Install

### Claude Code

Personal (all projects):

```bash
git clone https://github.com/<owner>/translate-online-docs-skill.git /tmp/translate-online-docs-skill
mkdir -p ~/.claude/skills
cp -r /tmp/translate-online-docs-skill ~/.claude/skills/translate-online-docs
```

Project-level (shared via git):

```bash
mkdir -p .claude/skills
git clone https://github.com/<owner>/translate-online-docs-skill.git .claude/skills/translate-online-docs
```

Restart Claude Code or start a new session to discover the skill.

### Codex

```text
$skill-installer install https://github.com/<owner>/translate-online-docs-skill
```

Or install by repo and path:

```text
$skill-installer install --repo <owner>/translate-online-docs-skill --path .
```

Restart Codex after installation so it can discover the new skill.

## Notes

This skill intentionally leaves recursive crawl decisions to the agent. The bundled script only prepares a translated Markdown tree as an mdBook project.
