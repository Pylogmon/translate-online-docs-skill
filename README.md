# Translate Online Docs Skill

A universal agent skill ([Agent Skills standard](https://agentskills.io)) for crawling, translating, and exporting online documentation.

## Skill

- `translate-online-docs`: Crawl an online documentation site or web book by agent judgment, save the source as Markdown, translate it into a target language, and optionally export mdBook or PDF deliverables.

## Install

### Claude Code

```bash
git clone https://github.com/pylogmon/translate-online-docs-skill.git ~/.claude/skills/dot-skill
```

Restart Claude Code or start a new session to discover the skill.

## Notes

This skill intentionally leaves recursive crawl decisions to the agent. The bundled script only prepares a translated Markdown tree as an mdBook project.
