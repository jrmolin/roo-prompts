# Global Custom Instructions

This file contains custom instructions that apply to all modes unless explicitly overridden in a mode's specific custom instructions file.

## Bulk Filesystem Operations with Filesystem MCP Server

When it is necessary to read many files, you can use the Filesystem-Operations MCP server to view the contents of large swathes of code at the one time. Every tool in Filesystem Operations can be called in bulk or you can use the folder tools to recurse all files in a folder. 

This is particularly useful for understanding the context of a codebase, identifying patterns, and making informed decisions about architecture and design.

## Knowledge Base Usage with the Knowledge Base MCP Server
We take great pride in our Knowledge Base MCP server—make it your first stop for searching, clarifying, and referencing documentation as you execute your tasks. It contains a wealth of style guides, library documentation, api documentation and more via the documentation in the ES. You can and should request new documentation to be added to the knowledge base if you need it.

When you need to clarify a concept, find documentation, or reference a specific library or API, use the Knowledge Base MCP server. It is designed to provide quick access to relevant information and documentation. You can ask questions in plain english and the MCP server will return relevant documentation or search results.

When using results from the knowledge base in your planning, include the source URL in your plan, inline with the recommendation that was guided by that result.

## Memory Management with Knowledge Base MCP

The Knowledge Base MCP server provides powerful tools for managing project memories. Effectively using these tools helps maintain project context, track decisions, and recall important information when needed.

**Importance:**
Storing key project information as memories ensures that valuable context, design decisions, and progress updates are easily accessible and searchable across different tasks and modes.

**When to Create Memories (Triggers):**
Consider creating a new memory using the `knowledge-base` MCP tools when:
*   A significant architectural or design decision is made.
*   The high-level project context, goals, features, or overall architecture changes significantly.
*   New architectural patterns or standards are introduced or modified.
*   Extremely useful information is discovered that could benefit the project.
*   Relationships between different parts of the project are established.
*   Certain files or code patterns are identified as particularly important or reusable.

**Which Tools to Use:**
*   `memory_encoding`: Use this tool to encode a single memory. Provide a descriptive `title` and the detailed `content` of the memory.
*   `memory_encodings`: Use this tool for bulk encoding of multiple memories at once. Provide a list of `Memory` objects, each with a `title` and `content`.
*   `memory_recall`: Use this tool to search the memory knowledge base by providing a list of `questions`. The tool will return relevant memories based on your query.
*   `memory_recall_last`: Use this tool to retrieve the most recent memories. You can specify the `count` of memories to retrieve.

**Memory Content and Format:**
*   **Title:** Provide a concise and descriptive title that summarizes the memory's content.
*   **Content:** Include all relevant details, context, rationale, and implications related to the memory. Be clear and specific. Include timestamps where appropriate, especially for decisions or progress updates.

By actively using these memory management tools, we can build a rich and searchable history of the project, improving efficiency and collaboration across all modes.

**Updating Memories:**
*   If a memory becomes outdated or needs clarification, use the `memory_update` tool to modify its content while preserving the original title.
*   If a memory is no longer relevant, use the `memory_delete` tool to remove it from the knowledge base.

## Starting Sub Agent Tasks

Unless asked specifically, you do not switch modes. You start a subtask agent in the mode you need and you pass significant context to get them going on their task. You only start "lead" agents and you dont bother with non-lead Agents.