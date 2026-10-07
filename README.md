# EXCELerate Penguin MathQuest

A working Streamlit starter project for EXCELerate Learning Space. Waddle guides students through Primary 4–6 mathematics practice.

## 1. What is included

- Start screen: first name/nickname, Primary year, learning path, topic and difficulty.
- Beginner, Moderate and Challenging: 10 questions per level, or 30 in an all-level adventure.
- Four mixed question styles: numerical entry, MCQ, matching and real drag-and-drop ordering.
- Drag-and-drop also has up/down buttons for phones and keyboard users.
- Fractions/equations rendered using LaTeX; exact equivalent fractions, decimals, mixed numbers and percentages accepted.
- Three optional hints; points, correct answers, current/best streak and progress.
- SQLite leaderboard grouped by year, learning path, topic and difficulty. Sharing is optional.
- Personalised downloadable PDF participation certificate, including total score and questions, plus each completed difficulty's result.
- Result CSV and question/solution review; original optional study music.

You do not need to copy the code snippets from the earlier conversation. The files in this project replace those snippets.

## 2. Download and extract

1. Download the project ZIP.
2. Extract/unzip it. Do not run the app inside the ZIP.
3. Find the folder `EXCELerate-Penguin-MathQuest`. It contains `app.py` and `requirements.txt`.
4. Install Python 3.12 if you do not already have it. On Windows, enable **Add Python to PATH** during installation. Official installer: https://www.python.org/downloads/
5. A computer is needed for the setup. Students can use phones/tablets once the app is hosted or shared on your Wi-Fi.

## 3. Windows setup (Command Prompt)

Open the project folder in File Explorer. Click its address bar, type `cmd` and press Enter. This opens Command Prompt in the correct folder.

Run these commands **one line at a time**:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If your installed Python is a different compatible version, use `py -m venv .venv` instead of the first command. The tested version is Python 3.12.

If using VS Code, open the extracted folder with **File → Open Folder** and use a **Command Prompt** terminal. The activation command above is for Command Prompt, not PowerShell.

## 4. Mac setup (Terminal)

Open Terminal, type `cd ` (include the space), drag the extracted project folder into Terminal and press Enter. Then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If `python3` is unavailable, install Python first. Linux uses these same commands; some Linux systems also require their Python venv package.

## 5. Open and try the app

Open http://localhost:8501 in your browser if it does not open automatically. Keep the terminal running.

1. Enter a first name or nickname.
2. Select Primary 4, 5 or 6.
3. Select your learning path and topic.
4. Select one difficulty, or **All three levels**.
5. Choose whether to share the completed run on the leaderboard.
6. Click **Start adventure**.
7. Answer each question. For matching, use each answer once. For ordering, solve A/B/C first, then arrange their cards by the answer from smallest to largest.
8. Optional: ask Waddle for hints. The displayed points update before submission.
9. Click **Submit answer**, read the solution, then click **Next adventure**.
10. After the final question, click **Finish adventure**. Download the PDF certificate and/or CSV results.
11. The leaderboard appears on the completion screen, alongside your position if you opted to share.

**Music:** enable Study music in the sidebar, then press Play on the audio player. Browser rules may prevent autoplay. The included 16-second original melody loops; no downloaded commercial track is required.

## 6. Scoring rules

| Difficulty | No hint | Hint 1 | Hint 2 | Hint 3 | Questions | Maximum points |
|---|---:|---:|---:|---:|---:|---:|
| Beginner | 10 | 8 | 6 | 5 | 10 | 100 |
| Moderate | 20 | 17 | 14 | 10 | 10 | 200 |
| Challenging | 30 | 25 | 20 | 15 | 10 | 300 |

The all-level adventure has 30 questions and a maximum of 600 points.

- Only the first valid submission counts. Repeated clicks/reruns cannot increase the score again.
- Blank or invalid numerical input does not count as a submission.
- A wrong answer earns zero points and resets the current streak. The solution is shown so the student can learn before continuing.
- Matching/order questions earn points only if the entire set is correct. They count as one question, although they contain three small problems.
- Accuracy counts correct questions, independent of hint deductions.
- Everyone who completes an adventure can download a participation certificate.
- Starting a new adventure generates new questions; questions may recur across separate adventures.

## 7. Question bank and learning paths

Original question templates cover:

Whole Numbers, Operations, Fractions, Decimals, Percentages, Money, Time, Measurement, Geometry, Ratio & Proportion, Data Handling and Probability.

Ratio & Proportion and Probability are enabled from Primary 5 in the starter. This is an application choice, not an official syllabus claim.

The bank uses shared mathematics skills for Cambridge, Malaysian and Mixed selections. Learning path currently labels the adventure and separates leaderboard results; it does **not** select different officially mapped question banks. Review and map templates to your taught syllabus before describing the app as curriculum-aligned. Questions are in English and money problems use RM.

Primary year changes the Whole Numbers range. Most other templates currently vary by difficulty rather than separate year-specific learning outcomes. The generator gives varied practice, but this is a starter bank rather than complete Primary 4–6 coverage.

## 8. File guide

| File | What to edit |
|---|---|
| `app.py` | Screen flow, branding, widgets, feedback, downloads |
| `curriculum.py` | Topics, available levels/learning paths and hint point values |
| `question_engine.py` | Original question templates, number ranges, question mix |
| `answer_checker.py` | Safe equivalent-number checking |
| `scoring.py` | Marking, one-time scoring and streaks |
| `leaderboard.py` | Result persistence and ranking |
| `certificate.py` | PDF text, colours and layout |
| `components/drag_drop.py` | Python-to-JavaScript ordering component |
| `components/order.js` | Drag/drop and accessible move buttons |
| `components/order.css` | Ordering card styles |
| `.streamlit/config.toml` | App colours |
| `assets/` | Certificate fonts, font licence, original study music |
| `tests/` | Automated checks |

The app automatically creates `data/leaderboard.sqlite3` when leaderboard storage is used. Do not upload real student results to GitHub.

## 9. Make changes safely

**Change points:** edit `POINTS` in `curriculum.py`. The four numbers are no hint, one hint, two hints and three hints.

**Change question numbers/types:** edit `kinds` in `build_adventure()` in `question_engine.py`. Its length sets questions per difficulty. Update the start-screen count text and README if you change the default 10. The certificate and progress use the actual number of questions automatically. Keep all students on the same question-count settings for fair rankings; old leaderboard results are not automatically migrated when you change scoring/counts.

**Change question difficulty:** edit the `base()` branches. `d=0` is Beginner, `d=1` is Moderate and `d=2` is Challenging. Each branch returns instruction, LaTeX, exact answer, first hint and worked solution.

**Improve hints:** edit the three hints built inside `make_question()`. The starter's first hint is topic-specific; hints 2 and 3 are general scaffolding. You can replace them with more detailed question-specific stages.

**Add a topic:** add the name in `curriculum.py`, then a matching branch in `base()`. Numeric/MCQ questions use one base problem; matching/order generate three different base problems with distinct answers. Ensure the template offers enough distinct answers to support these styles.

**Change study music:** replace `assets/study_music.wav` with your own licensed WAV. If using an MP3, change the filename in `app.py` accordingly.

**Certificate names:** bundled DejaVu fonts support Latin names and many other characters. For scripts they do not cover, replace the two `CertificateFont` TTF files with appropriately licensed fonts supporting those characters. Font paths are local assets.

## 10. Share on the same Wi-Fi

From the project folder, with your environment activated:

```bash
python -m streamlit run app.py --server.address=0.0.0.0
```

Use the Network URL shown in the terminal on students' devices. Your computer and students' devices must be on the same network, the computer must stay awake, and your firewall must allow this connection. `localhost` on a student's phone refers to the phone itself and will not open your computer's app.

## 11. Optional: deploy a demonstration online

Streamlit Community Cloud can deploy the source from GitHub. It is a suitable demonstration route. Durable class leaderboard hosting needs a persistent disk or an external database; this project's SQLite database should not be assumed durable on a temporary cloud filesystem.

1. Create a GitHub repository, e.g. `excelerate-penguin-mathquest`.
2. Upload the **contents** of the extracted project folder, so `app.py` and `requirements.txt` are at repository root. Include `components`, `assets` and `.streamlit` as well.
3. Do not upload `.venv`, cache folders or your `data/leaderboard.sqlite3` file.
4. Sign in at https://share.streamlit.io with your GitHub account.
5. Select **Create app** and choose the repository and branch.
6. Set the main file path to `app.py` and Python version to 3.12 in the deployment settings when offered.
7. Deploy, then test a complete adventure using the resulting URL before giving it to students.

For durable hosting, run one app server with a persistent volume and set the environment variable `MATHQUEST_DB` to a path on that volume. Examples:

Mac/Linux:
```bash
export MATHQUEST_DB=/your/persistent/folder/leaderboard.sqlite3
python -m streamlit run app.py
```
Windows Command Prompt:
```bat
set MATHQUEST_DB=C:\YourPersistentFolder\leaderboard.sqlite3
python -m streamlit run app.py
```

SQLite in this project supports several sessions on one server. Multiple app replicas require a shared database design; copying SQLite files between replicas is not supported.

## 12. Daily use and backup

To reopen later: open Terminal/Command Prompt in the folder, activate `.venv`, then run `python -m streamlit run app.py` again. Stop the app with **Ctrl+C** in the terminal.

Back up `data/leaderboard.sqlite3` (or your configured database path) with the app stopped. To reset the local leaderboard, stop the app, make a backup, then remove that database file. It will be recreated empty.

Progress is stored in the browser's Streamlit session. A full browser refresh/disconnection may reset an unfinished adventure. Completed opted-in runs are stored in the database. Names are self-entered and repeated completed runs are allowed; this is a practice leaderboard, not a verified assessment system.

## 13. Troubleshooting

| Problem | What to do |
|---|---|
| Python/py not found | Install Python; on Windows enable Add Python to PATH and reopen the terminal. |
| Cannot open `requirements.txt` or `app.py` | You are in the wrong folder. Open the folder containing both files. |
| `No module named streamlit` | Activate `.venv`, then run `python -m pip install -r requirements.txt`. |
| Ordering component errors | Install the provided requirements in your active environment. This component uses Streamlit components v2; older Streamlit releases may not work. |
| Port 8501 already in use | Stop the old app, or run `python -m streamlit run app.py --server.port=8502`. |
| Decimal/fraction marked wrong | Use an exact answer; `1/3` is accepted, a rounded `0.333` is not. |
| Mobile dragging difficult | Use the card's up/down buttons. |
| Music silent | Click Play; check your device volume. |
| Missing certificate/music assets | Extract and keep the full project folder, including `assets`. |
| Leaderboard disappears after a cloud restart | Use durable hosting/persistent disk; see section 11. |
| Matching options show the same choice twice | Each row is independent. Select each option exactly once to earn full points. |

## 14. Optional automated checks

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Checks cover numeric equivalence, all topic/year generators, marking idempotency, hint points, streaks, database grouping/save deduplication, PDF output and the Streamlit start/submission flow. AppTest does not execute browser JavaScript, so also manually check drag/drop and touch controls before classroom use.

## Technical references

- Streamlit components v2 registration: https://docs.streamlit.io/develop/api-reference/custom-components/st.components.v2.component
- Component mounting/state callbacks: https://docs.streamlit.io/develop/concepts/custom-components/components-v2/mount
- Community Cloud deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Deployment file organization: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization

Original question templates, vector penguin and music were created for this project. The certificate fonts have their licence in `assets/FONT_LICENSE.txt`.
