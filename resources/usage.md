# NLB MCP helper prompt

Use these tools to find titles and availability:
- `search_titles`: keyword search (returns top 5 titles with minimal record info: title, author, and per-record brn/format/availability when present).
- `search_titles_advanced`: fielded search with optional filters and paging (also limited to top 5 and minimal record info).
- `availability_by_title`: branch-level availability for a title using `brn` (or isbn/control_no). Returns branchId, brn, available/total/status when provided by NLB.
- `availability_at_branch`: availability for a title at a specific branch (requires `branch_id` + `brn`/isbn/control_no). Same minimal availability fields as above.
- `list_branches`: lookup branch codes/names (C005 Library Location); use this to choose `branch_id`.
- Resources: `nlb-mcp://usage` (this guide), `nlb-mcp://branches` (branch codes JSON).

Common flow to check a title at a branch:
1) Call `search_titles` (or `search_titles_advanced`) with title/keywords.
2) Prefer the first `brn` from the returned records; prefer records with format "Book" for shelf availability (ebooks are not on shelf).
3) If you need a branch code, call `list_branches` or read `nlb-mcp://branches` and pick the `code` that matches the desired library.
4) Call `availability_at_branch` with `branch_id` and the `brn` (or ISBN/control number).

Notes:
- Only BRN/ISBN/control_no are accepted for availability; we send BRN to `/GetAvailabilityInfo` when provided.
- Outputs are trimmed for brevity (top 5 search results; availability fields limited to ids and counts).
- NLB API keys are provided via server env; no user-supplied secrets needed.
