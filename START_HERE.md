# MathQuest update — copy and paste into GitHub

This update contains three complete Python files. Keep the other files in your existing repository.

1. Open `app.py` in GitHub, click the pencil (Edit), select all the old code and replace it with the entire supplied `app.py`. Commit changes.
2. Replace `question_engine.py` in the same way. Commit changes.
3. At the repository root, choose Add file → Create new file. Name it `teacher_dashboard.py`, paste the entire supplied file and commit. Put it alongside app.py, not in assets or components.
4. In your Streamlit app settings, open Secrets. Add this line, substituting your own private password:

```toml
teacher_password = "YOUR_OWN_LONG_PRIVATE_PASSWORD"
```

Do not put the actual password in a Python file or public GitHub repository.

5. Save the secrets. Streamlit normally updates after GitHub commits; reboot the app if it still displays the old version.
6. In the sidebar select Teacher dashboard, enter your password and click Log in. Filter by year, topic or level, or search a nickname. Export all results to CSV exports every saved run even when filters are selected.
7. Select Student adventure to return to the quiz. Your music file stays at assets/study_music.mp3.

## What changed

- Dashboard login, logout, search, filters and CSV export.
- Six skill families per topic. Each level's six individual questions cover all six families. Matching and ordering provide further practice.
- More varied word problems, missing values, conversions, reverse calculations, and data interpretation.
- Exact fraction marking and four distinct MCQ choices. Probability choices stay between zero and one.
- Existing MP3 player and plain numerical choices retained.

## Which records are available?

The existing save behaviour is preserved: only completed adventures for students who tick the leaderboard sharing checkbox are saved. The dashboard shows saved run summaries, including nickname, year, path, topic, level, score and completion time. It does not contain every individual answer or unfinished adventures.

The current SQLite database is local to the running app. Streamlit Community Cloud can discard local files during reboot or redeployment. Export records before rebooting if you need to retain them. Permanent storage requires an external database; creating a data folder in GitHub does not provide that.

## Checks

Python files compiled successfully. Across 1,080 generated adventures (32,400 questions), checked all topic/year combinations, skill coverage, correct-answer scoring, unique MCQ choices, and sorted ordering answers. These generator checks do not independently prove every word-problem formula. The dashboard module was previously tested for missing secrets, incorrect password, successful login, search, logout and CSV escaping; the updated combined app has not been tested in a browser here.
