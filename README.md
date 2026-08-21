# commit-haiku

A Claude Code plugin that generates haiku poetry from your git changes.

## Installation

### From a local path

Clone the repo:

```bash
git clone https://github.com/12britz/commit-haiku.git
cd commit-haiku
```

Inside a Claude Code session:

```
/plugin install commit-haiku /path/to/commit-haiku
```

Or with the CLI flag:

```bash
claude --plugin-dir /path/to/commit-haiku
```

### From the community marketplace

First add the marketplace (once):

```
/plugin marketplace add anthropics/claude-plugins-community
```

Then install:

```
/plugin install commit-haiku@claude-community
```

Then reload:

```
/reload-plugins
```

### Project-scoped MCP (zero config)

The `.mcp.json` in this repo acts as a standalone MCP server. Claude Code picks it up automatically when working in this directory — no setup needed.

## Usage

In a Claude Code session, ask:

- _"Generate a haiku for my changes"_
- _"What does commit-haiku say about this commit?"_
- _"Give me a poem about what I just changed"_

The plugin provides one MCP tool:

| Tool | Description |
|------|-------------|
| `generate_commit_haiku` | Analyzes git diff and returns a 5-7-5 haiku. Optional `diff_text` parameter for custom input. |

## How it works

The MCP server (`servers/commit-haikus-server`) reads `git diff --cached` (or falls back to `git diff HEAD`), classifies the change type (add, fix, remove, refactor, general), and crafts a haiku using keyword-aware templates and syllable counting.
