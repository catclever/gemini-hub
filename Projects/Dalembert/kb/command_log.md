# Command Log

## 2026-11-06: Git Push Decouple Provider and Model Selection Orthogonally (Option B)
- **Commit**: `181ea75`
- **Branch**: `origin/main` (`catclever/Dalembert`)
- **Command**:
  ```bash
  git add .gitignore bin/dalembert bin/dalembert-server lib/dalembert.rb lib/dalembert/agent.rb lib/dalembert/profile_resolver.rb llm.example.yml spec/dalembert/agent_spec.rb spec/dalembert/profile_resolver_spec.rb
  git commit -m "feat: decouple provider and model selection orthogonally (Option B)"
  git push origin main
  ```
- **Files**:
  - `.gitignore`: ignored `.dalembert/` local state / logs.
  - `bin/dalembert`: CLI updated for orthogonal provider and model resolution.
  - `bin/dalembert-server`: Server runner profile updates.
  - `lib/dalembert.rb`: Loaded profile_resolver.
  - `lib/dalembert/agent.rb`: Refactored agent profile initialization.
  - `lib/dalembert/profile_resolver.rb`: Added ProfileResolver with orthogonal fallback resolution and validation.
  - `llm.example.yml`: Added provider and model config documentation and examples.
  - `spec/dalembert/agent_spec.rb`: Spec suite updates for agent initialization.
  - `spec/dalembert/profile_resolver_spec.rb`: Unit test coverage for orthogonal profile resolver.
