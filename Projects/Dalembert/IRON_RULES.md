# Dalembert Ironclad Rules

## [Global]
- **Ecosystem**: Part of the Descartes ecosystem (`Descartes`, `descartes-produit`, `Dalembert`, `EnginEdge`).
- **Language & Runtime**: Ruby (`bundle exec rspec` for testing). Always use `frozen_string_literal: true`.
- **Metadata Boundary**: Never write `.gemini/`, `kb/`, `tasks/`, `docs/`, or `commands/` into the source code workspace.

## [Main Agent]
- Orchestrate task breakdown, knowledge auditing, and sub-agent delegation.
- Manage all Kanban tasks exclusively via `kanban-task-manager` MCP and knowledge records via `knowledge-manager` MCP.

## [Dev Agent]
- Write clean, idiomatic Ruby code with comprehensive RSpec unit tests (`spec/`).
- Preserve existing orthogonal model selection (`ProfileResolver`) and 12-Factor environment variable support.
- Run `bundle exec rspec` to verify all unit tests pass.
- Do NOT modify any task files or metadata in `~/.gemini/Projects/Dalembert/tasks/`.

## [Ops Agent]
- Verify `git status` and `git diff` before staging, committing, or pushing changes.
