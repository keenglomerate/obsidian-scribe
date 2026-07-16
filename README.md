# 🗂️ ObsidianScribe: Obsidian Vault MCP Server

A Model Context Protocol (MCP) server that connects local Obsidian note vaults to AI assistants, enabling secure reading, writing, searching, and updating of Markdown notes.

---

## 🛠️ MCP Tools Exposed

1. **`list_notes`**: Lists all notes (`.md` files) in your Obsidian vault.
2. **`read_note`**: Reads the full Markdown content of a specific note by title.
3. **`create_note`**: Creates a new note with specified title and content.
4. **`append_note`**: Appends content to the end of an existing note.
5. **`search_notes`**: Performs a full-text search across all notes in the vault for a keyword or phrase.

---

## 🚀 Setup & Registration

1. **Workspace Vault Folder:**
   The server expects your Obsidian notes vault to be located at:
   `~/Documents/Obsidian Vault/`
2. **Launch & Test:**
   ```bash
   python3 obsidian_server.py
   ```
3. **Antigravity CLI Integration:**
   Register this server in your `~/.gemini/antigravity-cli/settings.json` file under `mcpServers`:
   ```json
   "obsidian-scribe": {
     "command": "python3",
     "args": ["/absolute/path/to/obsidian_scribe/obsidian_server.py"]
   }
   ```
