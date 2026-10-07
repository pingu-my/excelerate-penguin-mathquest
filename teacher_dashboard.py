"""Teacher-only read access to the existing MathQuest results database."""
import csv
import hashlib
import hmac
import io
from contextlib import closing

import streamlit as st
from leaderboard import connect


def export_csv(records):
    """UTF-8 CSV for Excel, with student-entered text treated as text."""
    output = io.StringIO(newline="")
    columns = [
        "run_id", "name", "primary_year", "syllabus", "topic", "mode",
        "score", "correct", "questions", "accuracy", "best_streak",
        "completed_at",
    ]
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    for record in records:
        safe = {}
        for key in columns:
            value = record.get(key, "")
            if isinstance(value, str) and value.lstrip().startswith(
                ("=", "+", "-", "@")
            ):
                value = "'" + value
            safe[key] = value
        writer.writerow(safe)
    return output.getvalue().encode("utf-8-sig")


def teacher_dashboard():
    st.title("🔒 Teacher Dashboard")

    try:
        password = st.secrets["teacher_password"]
    except (KeyError, FileNotFoundError):
        password = None

    if not isinstance(password, str) or not password.strip():
        st.info(
            'Teacher login is not configured. Add teacher_password '
            'in Streamlit app Settings → Secrets.'
        )
        return

    expected = hashlib.sha256(password.encode("utf-8")).hexdigest()
    authenticated = hmac.compare_digest(
        st.session_state.get("_teacher_auth", ""), expected
    )

    if not authenticated:
        with st.form("teacher_login", clear_on_submit=True):
            entered = st.text_input("Teacher password", type="password")
            submitted = st.form_submit_button("Log in")
        if submitted:
            candidate = hashlib.sha256(entered.encode("utf-8")).hexdigest()
            if hmac.compare_digest(candidate, expected):
                st.session_state["_teacher_auth"] = expected
                st.rerun()
            else:
                st.error("Incorrect password.")
        return

    if st.button("Log out", key="teacher_logout"):
        st.session_state.pop("_teacher_auth", None)
        st.rerun()
        return

    st.caption(
        "All saved completed runs across Primary years, topics and levels. "
        "With the current app, only students who opted into leaderboard "
        "sharing have their completed results saved."
    )
    st.button("Refresh results", key="teacher_refresh")

    try:
        with closing(connect()) as connection:
            records = [
                dict(row)
                for row in connection.execute(
                    "SELECT * FROM results ORDER BY completed_at DESC"
                ).fetchall()
            ]
    except Exception:
        st.error("Could not read the results database. Try refreshing.")
        return

    if not records:
        st.info("No saved results yet.")
        return

    c1, c2 = st.columns(2)
    c1.metric("Saved adventures", len(records))
    c2.metric("Different nicknames", len({r["name"] for r in records}))

    st.download_button(
        "📥 Export all results to CSV",
        data=export_csv(records),
        file_name="MathQuest_All_Results.csv",
        mime="text/csv",
        key="teacher_export_all",
    )

    c1, c2, c3 = st.columns(3)
    year = c1.selectbox(
        "Primary year", ["All"] + sorted({r["primary_year"] for r in records}),
        key="teacher_year",
    )
    topic = c2.selectbox(
        "Topic", ["All"] + sorted({r["topic"] for r in records}),
        key="teacher_topic",
    )
    level = c3.selectbox(
        "Adventure level", ["All"] + sorted({r["mode"] for r in records}),
        key="teacher_level",
    )
    search = st.text_input("Search nickname", key="teacher_name").strip().casefold()

    filtered = [
        r for r in records
        if (year == "All" or r["primary_year"] == year)
        and (topic == "All" or r["topic"] == topic)
        and (level == "All" or r["mode"] == level)
        and (not search or search in r["name"].casefold())
    ]
    st.write(f"Showing {len(filtered)} of {len(records)} saved adventures.")
    if filtered:
        st.dataframe(filtered, hide_index=True, width="stretch")
    else:
        st.info("No results match these filters.")
