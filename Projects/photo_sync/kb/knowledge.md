# Photo Sync Agent Knowledge Base

This document serves as the index for all architectural constraints.

## Constraints
1. **Schema-First**: `core_schema.rb` is strictly read-only for agents. It dictates the Database DDL and the memory entities. Do not alter it dynamically.
2. **Data Flow**: External inputs -> `dry-struct` (Entity) -> Amber Context -> Sequel Repo.
3. **Anti-Corruption**: Amber rules must use `src/adapters/` and `src/repositories/` to execute external side effects.
