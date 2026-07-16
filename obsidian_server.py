#!/usr/bin/env python3
import os
import sys
import fnmatch
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("obsidian-scribe")

# Configure path to the Obsidian Vault
VAULT_DIR = os.path.expanduser("~/Obsidian Vault")

def get_safe_path(title: str) -> str:
    """Resolve note title to an absolute path, preventing path traversal attacks."""
    # Ensure note title ends with .md
    if not title.lower().endswith(".md"):
        title += ".md"
        
    # Resolve absolute path
    resolved_path = os.path.abspath(os.path.join(VAULT_DIR, title))
    
    # Verify the file is actually located inside the Vault directory
    if not resolved_path.startswith(os.path.abspath(VAULT_DIR)):
        raise PermissionError("Access denied: Note path is outside the designated Obsidian Vault.")
        
    return resolved_path

# --- MCP TOOLS ---

@mcp.tool()
def list_notes() -> str:
    """Lists all note files (.md) currently inside the Obsidian Vault."""
    try:
        if not os.path.exists(VAULT_DIR):
            return f"❌ Error: Vault directory '{VAULT_DIR}' does not exist."
            
        notes = []
        for root, _, files in os.walk(VAULT_DIR):
            for file in files:
                if file.endswith(".md"):
                    rel_path = os.path.relpath(os.path.join(root, file), VAULT_DIR)
                    # Strip .md extension for display
                    notes.append(rel_path[:-3])
                    
        if not notes:
            return "🗂️ Your Obsidian Vault is empty."
            
        output = [f"🗂️ Notes in Obsidian Vault ({len(notes)} total):"]
        for note in sorted(notes):
            output.append(f"- [[{note}]]")
            
        return "\n".join(output)
    except Exception as e:
        return f"❌ Error listing notes: {e}"

@mcp.tool()
def read_note(title: str) -> str:
    """Reads the full Markdown contents of a specific note in the vault.
    
    Args:
        title: The title of the note (e.g. 'Discrete Mathematics' or 'University/Homework').
    """
    try:
        note_path = get_safe_path(title)
        
        if not os.path.exists(note_path):
            return f"❌ Error: Note '{title}' does not exist."
            
        with open(note_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        return (
            f"📄 Note: [[{title}]]\n"
            f"=========================================\n"
            f"{content}\n"
        )
    except Exception as e:
        return f"❌ Error reading note: {e}"

@mcp.tool()
def create_note(title: str, content: str) -> str:
    """Creates a new note file inside the vault with the specified content.
    
    Args:
        title: Title of the note (e.g. 'Study Guidelines').
        content: Markdown content to write inside the note.
    """
    try:
        note_path = get_safe_path(title)
        
        # Create parent folders if note title contains subdirectories
        os.makedirs(os.path.dirname(note_path), exist_ok=True)
        
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"✅ Note [[{title}]] created successfully!"
    except Exception as e:
        return f"❌ Error creating note: {e}"

@mcp.tool()
def append_note(title: str, content: str) -> str:
    """Appends Markdown content to the end of an existing note in the vault.
    
    Args:
        title: Title of the note to update.
        content: Content to append to the end of the note.
    """
    try:
        note_path = get_safe_path(title)
        
        if not os.path.exists(note_path):
            return f"❌ Error: Note [[{title}]] does not exist. Use create_note instead."
            
        with open(note_path, "a", encoding="utf-8") as f:
            f.write("\n" + content)
            
        return f"✅ Content successfully appended to note [[{title}]]!"
    except Exception as e:
        return f"❌ Error updating note: {e}"

@mcp.tool()
def search_notes(query: str) -> str:
    """Performs a full-text search across all notes in the vault for a keyword.
    
    Args:
        query: Phrase or keyword to search for (case-insensitive).
    """
    try:
        if not os.path.exists(VAULT_DIR):
            return "❌ Error: Vault directory does not exist."
            
        query_lower = query.lower()
        matches = []
        
        for root, _, files in os.walk(VAULT_DIR):
            for file in files:
                if file.endswith(".md"):
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, VAULT_DIR)
                    note_title = rel_path[:-3]
                    
                    try:
                        with open(abs_path, "r", encoding="utf-8") as f:
                            for line_num, line in enumerate(f, 1):
                                if query_lower in line.lower():
                                    matches.append({
                                        "title": note_title,
                                        "line": line_num,
                                        "content": line.strip()
                                    })
                    except Exception:
                        continue  # Skip unreadable files
                        
        if not matches:
            return f"🔍 No matches found in vault for query: '{query}'"
            
        output = [f"🔍 Search results for: '{query}' ({len(matches)} matches found):"]
        for m in matches:
            output.append(f"- [[{m['title']}]]:L{m['line']} -> {m['content']}")
            
        return "\n".join(output)
    except Exception as e:
        return f"❌ Error searching notes: {e}"

if __name__ == "__main__":
    mcp.run()
