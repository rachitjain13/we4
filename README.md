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

## ⚡ 12 Mandatory Features Checklist

- [x] **01 Contestant Management**: Complete roster of 10 contestants across Team Alpha & Team Beta. Full management panel for points adjustment, captaincy assignment, immunity granting/stripping, nomination citations, and permanent eviction.
- [x] **02 Live Leaderboard**: Real-time points ranking in descending order. Top `#01` leader prominence, delta calculations from front-runner, team aggregates, and **strict exclusion of evicted housemates**.
- [x] **03 Task Management**: Complete lifecycle (`PENDING` ➔ `IN PROGRESS` ➔ `COMPLETED`). Marking completion **automatically disburses configured point bounties** to individual contestants or all active members of an assigned team.
- [x] **04 Point System**: Precision point addition and deduction with mandatory justification citations. Strictly enforces a **minimum floor of 0 points** and blocks evicted contestants.
- [x] **05 Captaincy**: Enforces the **single-captain rule**. Appointing a new captain automatically demotes the predecessor, updates global header indicators, and logs the event.
- [x] **06 Nominations**: Formal nomination desk. **Strict rule enforced**: Immune contestants cannot be nominated (`◉ IMMUNE — NOMINATION DISABLED`). Duplicate nominations are prevented.
- [x] **07 Immunity**: Shield granting and removal. Granting immunity to an already-nominated housemate automatically clears them from the Danger Zone.
- [x] **08 Danger Zone**: High-risk containment block rendered in strict monochrome with bold white borders (`NO RED`). Displays citations, timestamps, points at risk, and quick pardon/eviction controls.
- [x] **09 Big Boss Announcement**: Priority-tiered broadcast studio (`NORMAL`, `IMPORTANT`, `CRITICAL`). Active broadcasts pin to a persistent header banner across all views, with an archive log.
- [x] **10 Task Timer**: Live countdown timer powered by non-blocking Streamlit fragments (`START`, `PAUSE`, `RESET`, custom MM:SS). Reaching `00:00` flashes `TIME'S UP` and automatically fires an official Big Boss broadcast.
- [x] **11 House Statistics**: 12 live metrics (Highest Scorer, Lowest Scorer, House Average, Total Points, Active Count, Evicted Count, Captain, Immune Count, Total Tasks, Completed, Pending, Nominees) + monochrome horizontal points distribution chart.
- [x] **12 Eviction System**: Multi-step confirmation dialog with `CANCEL` and `CONFIRM EVICTION` buttons. Permanently removes contestants from active house, leaderboard, tasks, nominations, and captaincy.

---

## 🔒 14 Global Business Rules (Strictly Enforced)

1. **Evicted Point Restriction**: Evicted contestants cannot receive points.
2. **Evicted Task Restriction**: Evicted contestants cannot receive tasks.
3. **Evicted Nomination Restriction**: Evicted contestants cannot be nominated.
4. **Evicted Immunity Restriction**: Evicted contestants cannot receive immunity.
5. **Evicted Captaincy Restriction**: Evicted contestants cannot become captain.
6. **Immunity Precedence**: Immune contestants cannot be nominated under any circumstances.
7. **Duplicate Prevention**: Duplicate nominations are impossible.
8. **Single Captain**: Only one captain can exist at any given time.
9. **Task Exclusivity**: Completed tasks cannot be completed twice.
10. **Leaderboard Filtering**: Leaderboard strictly excludes evicted contestants.
11. **Danger Zone Consistency**: Danger Zone only contains currently nominated contestants.
12. **Real-time State**: Statistics always reflect live application state.
13. **Activity Logging**: All major actions create immutable activity log entries.
14. **Point Floor**: Points cannot fall below zero.

---

## 📁 Project Structure

```text
big-boss-command-center/
├── app.py                     # Main executive operations dashboard
├── requirements.txt           # Dependencies (streamlit, pandas)
├── README.md                  # Comprehensive operations manual
├── test_app_logic.py          # Automated test suite (all business rules verified)
├── data/
│   ├── contestants.json       # Seed roster of 10 housemates
│   └── tasks.json             # Seed house tasks
├── utils/
│   ├── state.py               # Session state initialization & logging
│   ├── contestants.py         # Contestant domain logic & validation rules
│   ├── tasks.py               # Task management & point auto-disbursement
│   └── ui.py                  # Strict monochrome UI components & toast helpers
└── assets/
    └── style.css              # Strict monochrome stylesheet & micro-animations
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

## 🧪 Evaluator Demo Flow (25 Steps)

1. **Open Overview**: View initial house status, KPI cards (10 active, Rahul as Captain, Aarav as top scorer), and live activity feed.
2. **Review Roster in Contestants**: Navigate to `▌ Contestants` and filter by `Team Alpha` or `Active Only`.
3. **Add Points to Contestant**: Select **Kabir**, go to `Point Control`, add `100 Points` with reason `"Physical challenge triumph"`.
4. **Observe Toast & Score Update**: Notice the monochrome toast (`✓ +100 points added to Kabir`) and score updating from 720 to 820.
5. **Open Leaderboard**: Switch to `▌ Leaderboard` and observe Kabir's updated ranking and score.
6. **Create a Task**: Navigate to `▌ Tasks`, expand `＋ CREATE NEW CHALLENGE / TASK`, title it `"Midnight Ration Search"`, assign to `Team Beta`, reward `150`, duration `30 min`, click `BROADCAST & CREATE TASK`.
7. **Start Task**: Click `▶ START TASK` on the newly created task (status transitions to `IN PROGRESS`).
8. **Complete Task**: Click `✔ MARK COMPLETE`.
9. **Verify Points Disbursement**: Observe all active members of Team Beta receive `+150 PTS` and tasks completed increment.
10. **Change House Captain**: Under `▌ Contestants` ➔ `Captaincy`, appoint **Aarav** as Captain. Observe the top header update immediately to `CAPTAIN: AARAV`.
11. **Test Immunity Protection**: Go to `▌ Nominations`. Select **Aarav** (who holds immunity). Observe the banner: `◉ IMMUNE — NOMINATION DISABLED` with the button disabled.
12. **Nominate Contestant**: Select **Kabir**, enter citation `"Failed morning endurance drill"`, click `NOMINATE FOR EVICTION`.
13. **Inspect Danger Zone**: Navigate to `▌ Danger Zone`. Observe Kabir rendered in the containment block with full citation details.
14. **Grant Immunity to Clear Nomination**: Go to `▌ Contestants` ➔ select **Kabir** ➔ `Immunity` ➔ `GRANT IMMUNITY`. Return to `▌ Danger Zone` to verify Kabir is automatically removed from danger.
15. **Broadcast Big Boss Directive**: Navigate to `▌ Announcements`, type `"All contestants report to the living room immediately."`, set Priority to `Critical`, click `BROADCAST ANNOUNCEMENT`. Observe the top banner appear across all screens.
16. **Run Task Timer**: Navigate to `▌ Control Room` ➔ `1. Task Timer`. Click `START COUNTDOWN` and watch the digital timer tick down live every second.
17. **Test Timer Alarm**: Click `TRIGGER TIME'S UP NOW` to test the alarm and automatic broadcast trigger.
18. **Review House Statistics**: Open `2. House Statistics` tab to see live KPIs and the monochrome horizontal points chart.
19. **Evict Contestant**: Open `3. Eviction Registry` tab, select **Nisha**, review the warning dialog, enter citation `"Eliminated in public vote"`.
20. **Test Cancellation**: Click `CANCEL` to test safety cancellation.
21. **Execute Eviction**: Click `CONFIRM EVICTION`.
22. **Verify Eviction Registry**: Verify Nisha moves to the `EVICTED CONTESTANTS REGISTRY` with final points crossed out.
23. **Confirm Leaderboard Exclusion**: Navigate to `▌ Leaderboard` — verify Nisha is no longer listed on the active leaderboard.
24. **Confirm Nomination Ineligibility**: Try nominating Nisha in `▌ Nominations` — confirm she cannot be selected or nominated.
25. **Inspect Full Activity Ledger**: Navigate to `▌ Control Room` ➔ `4. Full Activity Ledger`. Filter by category (`POINTS`, `TASK`, `CAPTAINCY`, `EVICTION`) to inspect the chronological audit trail.
