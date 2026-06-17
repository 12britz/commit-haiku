# commit-haiku

A Claude Code plugin that generates haiku poetry from your git changes.

## Installation

### Option 1: In-session (easiest)

Inside a Claude Code session, run:

```
/plugin install commit-haiku --dir /path/to/commit-haiku
```

Then reload plugins:

```
/reload-plugins
```

### Option 2: CLI flag

Launch Claude Code with the plugin:

```bash
claude --plugin-dir /path/to/commit-haiku
```

### Option 3: Permanent config

Add to `~/.claude/settings.json`:

```json
{
  "plugins": {
    "enabledPlugins": {
      "commit-haiku": {
        "source": "/path/to/commit-haiku"
      }
    }
  }
}
```

### Option 4: Project-scoped MCP (no plugin install)

The `.mcp.json` in this repo acts as a standalone project-scoped MCP server. Claude Code picks it up automatically when working in this directory — no plugin setup needed.

## Usage

In a Claude Code session, ask:

- _"Generate a haiku for my changes"_
- _"What does commit-haiku say about this commit?"_
- _"Give me a poem about what I just changed"_

The plugin's skill auto-triggers when Claude detects you're asking about commit poetry. It provides one MCP tool:

| Tool | Description |
|------|-------------|
| `generate_commit_haiku` | Analyzes git diff and returns a 5-7-5 haiku. Optional `diff_text` parameter for custom input. |

## How it works

The MCP server (`servers/commit-haikus-server`) reads `git diff --cached` (or falls back to `git diff HEAD`), classifies the change type (add, fix, remove, refactor, general), and crafts a haiku using keyword-aware templates and syllable counting.
