# commit-haiku

A Claude Code plugin that generates haiku poetry from your git changes.

## Installation

### From a local plugin directory

```bash
git clone https://github.com/12britz/commit-haiku.git
cd commit-haiku
claude --plugin-dir .
```

Or in `~/.claude/settings.json`:

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

### Zero-config MCP (no plugin install)

The `.mcp.json` in this repo is picked up automatically when Claude Code opens this directory — the `generate_commit_haiku` MCP tool works without any plugin setup.

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
