# NLB MCP helper prompt

Use these tools to find titles and availability:
- `search_titles`: keyword search (returns `bibId`/`brn`).
- `search_titles_advanced`: fielded search with optional filters and paging.
- `availability_by_title`: availability for a title (accepts `bib_id`/ISBN/control number).
- `availability_at_branch`: availability for a title at a specific branch (requires `branch_id` + identifier).
- `list_branches`: lookup branch codes/names (C005 Library Location); use this to choose `branch_id`.

Common flow to check a title at a branch:
1) Call `search_titles` (or `search_titles_advanced`) with the title/keywords.
2) Pick the `bibId` (or `brn` if present) from results.
3) If you need a branch code, call `list_branches` and pick the `code` that matches the desired library.
4) Call `availability_at_branch` with `branch_id` and the `bib_id` (or ISBN/control number).

Notes:
- Optional fields may be omitted; normalized outputs remove nulls.
- NLB API keys are provided via server env; no user-supplied secrets needed.
