# hindsight-skills

AI coding agent skills for [Hindsight](https://hindsight.dev) — long-term memory for AI agents.

Works with **Claude Code**, **Codex**, **Gemini CLI**, **Cursor**, **Kiro**, and **Factory Droid**.

Most agents forget everything between sessions. Hindsight fixes that. It extracts facts, builds entity graphs, and synthesizes mental models from conversations — so your agent remembers users, learns patterns, and gets better over time.

These skills give your coding agent deep expertise in Hindsight's architecture, so you can go from "I want my agent to remember things" to working code in a single session.

## See it work

```
You:    /hindsight-architect

Claude: [detects your Next.js + Python codebase, finds no existing Hindsight config]
        What does your application do, and who uses it?

You:    It's a customer support agent for our SaaS platform. Each customer
        has multiple users who open tickets. The agent needs to remember
        past interactions so it doesn't ask the same questions twice.

Claude: I see three memory opportunities:
        1. Per-user conversation history — remember what each user has told you
        2. Per-customer product knowledge — learn how each customer uses your platform
        3. Cross-customer issue patterns — detect recurring problems across your base

        Should we design for all three, or start with a subset?

You:    All three. We're on Hindsight Cloud.

Claude: [asks about recall optimization: balanced, completeness, or cost]
        [asks about enterprise requirements: PII, compliance, security]

Claude: Here's your memory architecture:

        # Memory Implementation Plan: support-agent
        ## Bank Configuration — single bank, per-user tag isolation
        ## Tag Schema — userId:{id}, customerId:{id}
        ## Retain Strategy — full conversation upsert with document_id
        ## Recall Strategy — 10K token budget, any_strict tag matching
        ## Mental Models — 3 models with auto-refresh:
           - Per-user preferences (communication style, expertise level)
           - Per-customer product usage (features, configuration, pain points)
           - Cross-customer issue tracker (recurring problems, unresolved bugs)
        ## Client Setup — Python SDK with environment variables
        ## Implementation Checklist — 9 steps, executable in order
```

Six questions. One implementation plan. Working code for your stack.

## Skills

| Skill | What it does |
|-------|-------------|
| `/hindsight-architect` | Memory architecture design. Understands your application, identifies where memory adds value, and produces a complete implementation plan — bank config, tag schema, retain/recall patterns, mental models, and working code. |
| `/hindsight-docs` | Full Hindsight reference. API operations, SDK guides, configuration, deployment, cookbook recipes. Your agent searches these docs to answer specific questions or debug your integration. |

## Install

### Claude Code

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup
```

Or add to your repo so teammates get it:

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git .claude/skills/hindsight-skills
cd .claude/skills/hindsight-skills && ./setup
```

### Codex, Gemini CLI, or Cursor

These agents all follow the [SKILL.md standard](https://github.com/anthropics/claude-code) and discover skills from `.agents/skills/` or `~/.codex/skills/`.

Install to one repo:

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git .agents/skills/hindsight-skills
cd .agents/skills/hindsight-skills && ./setup --host codex
```

Install globally:

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup --host codex
```

### Kiro

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup --host kiro
```

### Factory Droid

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup --host factory
```

### Auto-detect

If you have multiple agents installed, setup will find and register with all of them:

```bash
git clone --depth 1 https://github.com/vectorize-io/hindsight-skills.git ~/hindsight-skills
cd ~/hindsight-skills && ./setup --host auto
```

### npx

```bash
npx skills add vectorize-io/hindsight-skills --skill hindsight-architect
npx skills add vectorize-io/hindsight-skills --skill hindsight-docs
```

## What the architect actually knows

The architect skill isn't a generic template generator. It has deep knowledge of Hindsight internals and makes real architecture decisions:

**Retain** — Knows that `document_id` enables conversation upsert (same ID = replace + re-extract), that content over 3K chars is auto-chunked, that `context` guides extraction quality, and that you send full conversations, not deltas.

**Recall** — Understands the 4 parallel retrieval strategies (semantic, BM25, graph, temporal), how `tags_match` modes work (`any` includes untagged, `any_strict` excludes), and how to size token budgets for your use case.

**Tags** — Knows tags are for identity scoping (userId, customerId), not content classification. Designs tag schemas that enforce memory isolation and prevent cross-user data leakage.

**Mental models** — Understands that `source_query` determines what to synthesize, `tags` filter whose memories to analyze, and `trigger: { refresh_after_consolidation: true }` enables auto-refresh. Designs retrieval strategies so your application can find the right model at runtime.

**Reflect** — Knows this is an expensive agentic loop (up to 10 iterations), not a routine pre-response call. Recommends recall + direct mental model fetch for the pre-response pattern, and reflect only for complex disposition-influenced reasoning.

**Deployment** — Detects your stack (Python, Node.js, framework) and generates code for your specific setup: Hindsight Cloud, self-hosted, or embedded.

## Troubleshooting

**Skills not showing up?** Re-run setup and restart your agent:
```bash
cd ~/hindsight-skills && ./setup        # or --host codex, --host auto, etc.
```

**Slash commands don't autocomplete?** Skills must be at `~/.claude/skills/{name}/SKILL.md` (Claude Code), `~/.codex/skills/{name}/SKILL.md` (Codex/Gemini/Cursor), `~/.kiro/skills/{name}/SKILL.md` (Kiro), or `~/.factory/skills/{name}/SKILL.md` (Factory Droid). The setup script handles this — run it again if something got out of sync.

**Want to update?**
```bash
cd ~/hindsight-skills && git pull && ./setup --host auto
```

## Requirements

- An AI coding agent: [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://openai.com/index/codex/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Cursor](https://cursor.com), [Kiro](https://kiro.dev), or [Factory Droid](https://factory.ai)
- A [Hindsight](https://hindsight.dev) account — sign up at [ui.hindsight.vectorize.io](https://ui.hindsight.vectorize.io)

## License

MIT. Free and open source.

[hindsight.dev](https://hindsight.dev) · [Documentation](https://docs.hindsight.dev) · [GitHub](https://github.com/vectorize-io/hindsight)
