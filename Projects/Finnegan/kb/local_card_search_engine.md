# Local-First Card Search Engine (Fuzzy Subsequence & Contiguous Bonus)

**Location**: `~/.gemini/Projects/Finnegan/kb/local_card_search_engine.md`  
**Status**: Active / Production  
**Implemented In**: `core/search/search.go`, `core/search/search_test.go`, `app.go`, `frontend/src/App.svelte`  

---

## 1. Scope & Viewport Decoupling

Finnegan's frontend enforces viewport capacity constraints to ensure smooth 60fps 3D rendering (e.g. 8~14 visible cards on stage). However, a user's consciousness repository may contain hundreds or thousands of Markdown files.

**Key Rule**: **The search engine operates over 100% of all local physical cards, completely decoupled from what is currently mounted on the screen.**

- **Search Scope**:
  1. `Scattering/`: Unsorted atomic fragments, thoughts, and captures.
  2. `Weaving/`: Organized long-form syntheses and project notes.
  3. `tempCards` (In-Memory): Active network discoveries from Bugu Babel before local promotion.
- **Data Path**:
  The frontend delegates search requests via Wails IPC (`SearchLocalCards(query)`). Go performs the scan in microsecond speeds over memory/disk structures and returns sorted `[]Card` candidates without passing unnecessary bulk payloads to the DOM.

---

## 2. Space-Free Natural Substring & Subsequence Algorithm

Chinese and multilingual thinking flows continuously without forced spaces (e.g., users naturally type `赛博沙盒` instead of `赛博 沙盒`). The matching engine implements a smart **Subsequence Matching with Contiguous Run Bonuses** (analogous to fzf and VS Code command palette):

### 2.1 UTF-8 Rune Normalization
Target and query strings are converted to lowercased rune arrays (`[]rune`), supporting seamless mixed-language queries (e.g., `bugu雷达`, `atproto协议`, `赛博Memex`).

### 2.2 Tiered Scoring Mechanism (`core/search/search.go`)

$$\text{FinalScore} = \text{BaseScore} + \text{Bonus}_{\text{contiguous}} + \text{Bonus}_{\text{boundary}} + \text{Bonus}_{\text{compact}} - \text{Penalty}_{\text{span}}$$

1. **Tier 1: Exact Contiguous Substring (Guaranteed $\ge 100$)**:
   - If the entire query string appears contiguously inside the target:
     - Base score: $100.0 + 5.0 \times \text{len}(\text{query})$.
     - Full exact string match: $+50.0$.
     - Prefix match (starts at index 0): $+25.0$.
     - Word-boundary start (preceded by space or punctuation): $+15.0$.
     - Target length penalty: $-0.05 \times (\text{len}(\text{target}) - \text{len}(\text{query}))$ (shorter targets rank higher).

2. **Tier 2: Subsequence Matching (Query Runes in Order)**:
   - When not strictly contiguous, all query runes must appear in target in order ($t_{i_1} < t_{i_2} < \dots < t_{i_k}$).
   - **Contiguous Streak Bonus**:
     Consecutive matching characters earn increasing bonuses ($\text{streak} \times 6.0$).
   - **Word Boundary Bonus**:
     Matching at the beginning of words/tokens yields $+8.0$ per occurrence.
   - **Compactness & Distance Penalty**:
     The distance span between the first and last matched character in the target incurs a penalty:
     $$\text{Penalty} = \min\left(20.0, (\text{span} - \text{len}(\text{query})) \times 0.5\right)$$
     *Note: Subsequence scores are capped strictly below 95.0, mathematically guaranteeing that any contiguous substring match always ranks above a fragmented subsequence match.*

### 2.3 Composite Multi-Field Weighting
Each card is evaluated across multiple fields:
- **Title Match**: Weighted by **$3.0\times$**
- **Tags Match**: Weighted by **$2.0\times$**
- **Content Match**: Weighted by **$1.0\times$**

Cards are sorted in descending order of composite score; ties are broken by `CreatedAt` descending (most recent first).

---

## 3. Frontend Debounce & IPC Integration

In `frontend/src/App.svelte`:
- **Input Debounce**: A timer delays search dispatch by **`250ms`**. Successive keystrokes reset the timer, preventing IPC saturation.
- **Minimum Query Length**: Search triggers when input length $\ge 2$ characters.
- **Clean Fallback**: Emptying the input instantly cancels active search sessions and triggers graceful stage restoration.
