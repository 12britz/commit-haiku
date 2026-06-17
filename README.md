# commit-haiku

A Claude Code plugin that generates haiku poetry from your git changes.

## Installation

### Option 1: Plugin directory (recommended)

Load the plugin in any Claude Code session:

```bash
claude --plugin-dir /path/to/commit-haiku
```

Or add it to your project's Claude Code config at `~/.claude/settings.json`:

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

### Option 2: Project-scoped MCP

The `.mcp.json` at the project root also works as a standalone project-scoped MCP server. Claude Code will pick it up automatically when you're in this directory.

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
