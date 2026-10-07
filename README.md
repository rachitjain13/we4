# BIG BOSS — HOUSE COMMAND CENTER 👁️
**Complete Web Application Build Specification & Executive Operations Manual**

An executive-level operational command center engineered for the Big Boss House. Built with a **strict, high-contrast black & white monochrome design aesthetic** inspired by minimalist SaaS platforms, ChatGPT, Linear, and dark mission-control operations centers.

---

## 🏛️ System Philosophy: Strict Monochrome

The entire user interface strictly utilizes **only black, white, and neutral grays**.
- **No red, green, blue, yellow, pink, orange, purple, or neon colors.**
- **No colorful gradients or gaming UI elements.**
- States and alerts are expressed purely through **contrast, bold typography, borders, and monochrome badges**:
  - `#000000` Pure Black
  - `#080808` Main Background
  - `#111111` Secondary Background
  - `#181818` Cards
  - `#222222` Borders
  - `#333333` Dividers
  - `#666666` Muted Text
  - `#AAAAAA` Secondary Text
  - `#FFFFFF` Primary Text

---

## ⚡ Complete Feature Checklist (All 13 Modules)

- [x] **01 Contestant Management**: Complete roster of 10 contestants across Team Alpha & Team Beta. Full management panel for points adjustment, captaincy assignment, immunity granting/stripping, nomination citations, and permanent eviction.
- [x] **02 Live Leaderboard**: Real-time points ranking in descending order. Top `#01` leader prominence, delta calculations from front-runner, team aggregates, and **strict exclusion of evicted housemates**.
- [x] **03 Task Management**: Complete lifecycle (`PENDING` ➔ `IN PROGRESS` ➔ `COMPLETED`). Marking completion **automatically disburses configured point bounties** to individual contestants or all active members of an assigned team.
- [x] **04 Point System**: Precision point addition and deduction with mandatory justification citations. Strictly enforces a **minimum floor of 0 points** and blocks evicted contestants.
- [x] **05 Questions / Puzzle Challenge**: Dedicated cipher and puzzle challenge arena. Supports **Hexadecimal**, **ASCII / Number Sequence**, **Morse / Symbol**, **Text Riddles**, and **Image Schematics**. Features solving contestant selection, real-time answer verification, instant point disbursement, subtle shake error animation, and full Big Boss question CRUD controls.
- [x] **06 Captaincy**: Enforces the **single-captain rule**. Appointing a new captain automatically demotes the predecessor, updates global header indicators, and logs the event.
- [x] **07 Nominations**: Formal nomination desk. **Strict rule enforced**: Immune contestants cannot be nominated (`◉ IMMUNE — NOMINATION DISABLED`). Duplicate nominations are prevented.
- [x] **08 Immunity**: Shield granting and removal. Granting immunity to an already-nominated housemate automatically clears them from the Danger Zone.
- [x] **09 Danger Zone**: High-risk containment block rendered in strict monochrome with bold white borders (`NO RED`). Displays citations, timestamps, points at risk, and quick pardon/eviction controls.
- [x] **10 Big Boss Announcement**: Priority-tiered broadcast studio (`NORMAL`, `IMPORTANT`, `CRITICAL`). Active broadcasts pin to a persistent header banner across all views, with an archive log.
- [x] **11 Task Timer**: Live countdown timer powered by non-blocking Streamlit fragments (`START`, `PAUSE`, `RESET`, custom MM:SS). Reaching `00:00` flashes `TIME'S UP` and automatically fires an official Big Boss broadcast.
- [x] **12 House Statistics**: Live metrics covering house points, roster states, task completion rates, question solving analytics (Solved, Remaining, Points Awarded, Top Solver), and monochrome points distribution chart.
- [x] **13 Eviction System**: Multi-step confirmation dialog with `CANCEL` and `CONFIRM EVICTION` buttons. Permanently removes contestants from active house, leaderboard, tasks, nominations, questions, and captaincy.

---

## 🔒 Global Business Rules (Strictly Enforced)

1. **Evicted Point Restriction**: Evicted contestants cannot receive points.
2. **Evicted Task Restriction**: Evicted contestants cannot receive tasks.
3. **Evicted Nomination Restriction**: Evicted contestants cannot be nominated.
4. **Evicted Immunity Restriction**: Evicted contestants cannot receive immunity.
5. **Evicted Captaincy Restriction**: Evicted contestants cannot become captain.
6. **Evicted Question Restriction**: Evicted contestants cannot solve challenge questions.
7. **Immunity Precedence**: Immune contestants cannot be nominated under any circumstances.
8. **Duplicate Prevention**: Duplicate nominations are impossible.
9. **Single Captain**: Only one captain can exist at any given time.
10. **Task Exclusivity**: Completed tasks cannot be completed twice.
11. **Question Exclusivity**: A solved question cannot be solved a second time.
12. **Leaderboard Filtering**: Leaderboard strictly excludes evicted contestants.
13. **Danger Zone Consistency**: Danger Zone only contains currently nominated contestants.
14. **Real-time State**: Statistics always reflect live application state.
15. **Activity Logging**: All major actions create immutable activity log entries.
16. **Point Floor**: Points cannot fall below zero.

---

## 📁 Project Structure

```text
big-boss-command-center/
├── app.py                     # Main executive operations dashboard
├── requirements.txt           # Dependencies (streamlit, pandas)
├── README.md                  # Comprehensive operations manual & demo flow
├── test_app_logic.py          # Automated test suite (all rules verified)
├── data/
│   ├── contestants.json       # Seed roster of 10 housemates
│   ├── tasks.json             # Seed house tasks
│   └── questions.json         # Seed puzzle challenge questions
├── utils/
│   ├── state.py               # Session state initialization & logging
│   ├── contestants.py         # Contestant domain logic & validation rules
│   ├── tasks.py               # Task management & point auto-disbursement
│   ├── questions.py           # Puzzle challenge engine & verification
│   └── ui.py                  # Strict monochrome UI components & toast helpers
└── assets/
    ├── style.css              # Strict monochrome stylesheet & micro-animations
    └── blueprint.svg          # Classified surveillance blueprint schematic
```

---

## 🚀 Run Instructions

```bash
cd C:\Users\htc\.gemini\antigravity\scratch\big-boss-command-center
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🧪 Evaluator Demo Flow

1. **Overview**: View house status, 7 KPI cards, current captain (**Rahul**), and live activity feed.
2. **Contestants**: Inspect contestant roster; add points to **Kabir** and observe toast and score updates.
3. **Leaderboard**: Switch to `▌ Leaderboard` and see rankings update.
4. **Tasks**: Create and complete a house task; confirm automatic points disbursement to team/contestant.
5. **Questions / Puzzle Challenge**:
   - Navigate to `▌ Questions`.
   - Observe the 3 progress cards (`0 / 5 SOLVED`, `0 PTS`, `5 REMAINING`).
   - Select solving contestant: **Aarav**.
   - Review Q1 (Hex): `46 89 5e 05 ab 1e 74 07 1c 7a cb`.
   - Submit incorrect answer `"wrong"`: observe subtle card shake and `✕ INCORRECT ANSWER. Try again.`
   - Submit correct answer `"solaris"`: observe `✓ CORRECT ANSWER! +500 POINTS`, card transitions to `✓ SOLVED`, and Aarav receives +500 points immediately!
   - Switch to `▌ Leaderboard` to observe Aarav's points jump by +500.
   - Review Q5 (Image): Examine the monochrome surveillance blueprint schematic and submit `"vault 9"`.
6. **Captaincy**: Appoint a new House Captain and verify top header updates.
7. **Nominations**: Try nominating immune contestant (blocked), then nominate non-immune contestant.
8. **Danger Zone**: Inspect nominated contestants in the risk containment block.
9. **Announcements**: Broadcast an announcement and verify top banner across all views.
10. **Timer**: Start/pause/reset the live task countdown timer.
11. **House Statistics**: Inspect comprehensive analytics, including the new **Questions & Challenge Analytics** panel (Questions Solved, Remaining, Points Awarded, Top Solver).
12. **Eviction**: Evict a contestant with confirmation; verify they are excluded from the leaderboard, nominations, and question solving.
