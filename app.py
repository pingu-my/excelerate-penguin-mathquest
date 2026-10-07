from pathlib import Path
from uuid import uuid4
import base64
import csv
import io

import streamlit as st
import streamlit.components.v1 as components

from curriculum import PATHS, DIFFICULTIES, POINTS, available_topics
from question_engine import build_adventure
from teacher_dashboard import teacher_dashboard
from answer_checker import number
from scoring import record, summary
from leaderboard import save, rows
from certificate import create_certificate
from components.drag_drop import ordering


st.set_page_config(
    page_title="EXCELerate Penguin MathQuest",
    page_icon="🐧",
    layout="centered",
)

with st.sidebar:
    app_view = st.radio("Open", ["Student adventure", "Teacher dashboard"], key="app_view")

if app_view == "Teacher dashboard":
    teacher_dashboard()
    st.stop()

st.title("🐧 EXCELerate Penguin MathQuest")
st.markdown(
    "**EXCELerate Learning Space** · Learn • Practise • Explore • EXCEL"
)
st.caption("Waddle is your mathematics adventure guide.")


@st.cache_data
def load_music(music_path, modified_time):
    """Cache the encoded music; refresh when the file changes."""
    return base64.b64encode(
        Path(music_path).read_bytes()
    ).decode("ascii")


with st.sidebar:
    st.header("🐧 Waddle’s corner")
    st.write(
        "Use paper for your working. Think carefully before submitting."
    )
    st.caption(
        "Each question is scored on its first submission. "
        "A matching or ordering question earns points only "
        "when the whole answer is correct."
    )

    if st.toggle(
        "🎵 Study music",
        value=True,
        key="study_music_enabled",
    ):
        music_path = (
            Path(__file__).parent / "assets/study_music.mp3"
        )

        if music_path.exists():
            encoded_music = load_music(
                str(music_path),
                music_path.stat().st_mtime_ns,
            )

            components.html(
                f"""
                <audio
                    id="waddle-music"
                    controls
                    loop
                    preload="auto"
                    aria-label="Waddle's study music"
                    style="width:100%;"
                >
                    <source
                        src="data:audio/mpeg;base64,{encoded_music}"
                        type="audio/mpeg"
                    >
                </audio>

                <p
                    id="music-message"
                    style="font:12px sans-serif;color:#666;"
                ></p>

                <script>
                    const music =
                        document.getElementById("waddle-music");

                    // 0.10 = 10% starting volume.
                    // Change to 0.05 for 5%.
                    music.volume = 0.10;

                    music.play().catch(() => {{
                        document.getElementById(
                            "music-message"
                        ).textContent =
                            "Press Play to start the study music.";
                    }});
                </script>
                """,
                height=100,
            )

        else:
            st.info(
                "Upload study_music.mp3 into the assets folder."
            )

    if "quest" in st.session_state and st.button("Return to start"):
        del st.session_state.quest
        st.rerun()


if "quest" not in st.session_state:
    st.subheader("Choose your adventure")

    name = st.text_input(
        "Student first name or nickname",
        max_chars=50,
    )

    year = st.selectbox("Primary year", [4, 5, 6])
    syllabus = st.selectbox("Learning path", PATHS)

    topic = st.selectbox(
        "Mathematics topic",
        available_topics(year, syllabus),
    )

    mode = st.radio(
        "Adventure level",
        DIFFICULTIES + ["All three levels"],
    )

    st.write("10 questions per level · All three levels = 30 questions")

    st.caption(
        "Starter practice uses shared mathematics skills. "
        "The learning path is recorded in your results; "
        "this version does not claim official curriculum alignment."
    )

    consent = st.checkbox(
        "Show my nickname and completed result on this app’s leaderboard",
        value=False,
    )

    if st.button("🚀 Start adventure", type="primary"):
        if not name.strip():
            st.warning("Enter your first name or nickname to begin.")
        else:
            st.session_state.quest = {
                "run_id": uuid4().hex,
                "profile": {
                    "name": name.strip(),
                    "year": year,
                    "syllabus": syllabus,
                    "topic": topic,
                    "mode": mode,
                },
                "questions": build_adventure(
                    year, syllabus, topic, mode
                ),
                "index": 0,
                "results": [],
                "hints": 0,
                "share": consent,
                "saved": False,
            }
            st.rerun()

    st.stop()


quest = st.session_state.quest
profile = quest["profile"]
stats = summary(quest["results"])

st.subheader(
    f"Primary {profile['year']} · {profile['topic']}"
)

c1, c2, c3 = st.columns(3)

c1.metric("⭐ Points", stats["score"])
c2.metric(
    "✅ Correct",
    f"{stats['correct']}/{stats['questions']}",
)
c3.metric("🔥 Streak", stats["streak"])

st.progress(
    quest["index"] / len(quest["questions"])
)


if quest["index"] == len(quest["questions"]):
    st.success(
        "🏆 Adventure complete! Keep waddling towards excellence!"
    )

    st.write(
        f"**{stats['correct']}/{stats['questions']} correct · "
        f"{stats['accuracy']:.1f}% accuracy · "
        f"{stats['score']} points**"
    )

    level_results = []

    for difficulty in dict.fromkeys(
        result["difficulty"] for result in quest["results"]
    ):
        difficulty_stats = summary(
            [
                result
                for result in quest["results"]
                if result["difficulty"] == difficulty
            ]
        )

        level_results.append(
            {
                "Level": difficulty,
                "score": difficulty_stats["score"],
                "correct": difficulty_stats["correct"],
                "questions": difficulty_stats["questions"],
            }
        )

    st.table(level_results)

    if quest["share"] and not quest["saved"]:
        try:
            save(
                quest["run_id"],
                profile,
                stats,
            )
            quest["saved"] = True

        except Exception:
            st.warning(
                "Could not save the leaderboard result. "
                "Your certificate is still available. "
                "Reload to retry."
            )

    st.download_button(
        "🎓 Download PDF certificate",
        create_certificate(
            profile,
            quest["results"],
            quest["run_id"],
        ),
        file_name="EXCELerate_MathQuest_Certificate.pdf",
        mime="application/pdf",
    )

    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=[
            "id",
            "difficulty",
            "correct",
            "points",
            "hints",
            "response",
        ],
    )

    writer.writeheader()
    writer.writerows(quest["results"])

    st.download_button(
        "Download my question results (CSV)",
        output.getvalue(),
        file_name="MathQuest_Results.csv",
        mime="text/csv",
    )

    with st.expander("Review your questions and solutions"):
        for i, (question, result) in enumerate(
            zip(quest["questions"], quest["results"]),
            1,
        ):
            feedback = (
                "Correct"
                if result["correct"]
                else "Keep practising"
            )

            st.markdown(
                f"**Question {i} · "
                f"{question['difficulty']} · "
                f"{feedback}**"
            )

            st.write(question["instruction"])

            if question["latex"]:
                st.latex(question["latex"])

            if question["question_type"] in [
                "matching",
                "drag_drop",
            ]:
                problems = question.get(
                    "pairs",
                    question.get("problems", []),
                )

                for problem in problems:
                    st.write(problem["prompt"])
                    st.latex(problem["solution"])

                if question["question_type"] == "drag_drop":
                    st.write(
                        "Order: "
                        + " → ".join(question["answer"])
                    )

            else:
                st.latex(question["solution"])

    st.subheader("🏆 Waddle’s Hall of Fame")

    st.caption(
        "Completed runs for the same Primary year, "
        "learning path, topic and level. "
        "Nicknames are self-entered; "
        "this is a friendly practice leaderboard."
    )

    try:
        entries = rows(profile)

        if not entries:
            st.info(
                "No shared results in this adventure yet."
            )

        else:
            if quest["saved"]:
                rank = next(
                    (
                        i
                        for i, entry in enumerate(entries, 1)
                        if entry["run_id"] == quest["run_id"]
                    ),
                    None,
                )

                st.write(
                    f"Your adventure position: #{rank}"
                )

            leaderboard_display = [
                {
                    "Rank": i,
                    "Nickname": entry["name"],
                    "Points": entry["score"],
                    "Correct": (
                        f"{entry['correct']}/"
                        f"{entry['questions']}"
                    ),
                    "Accuracy": (
                        f"{entry['accuracy']:.1f}%"
                    ),
                }
                for i, entry in enumerate(entries[:10], 1)
            ]

            st.dataframe(
                leaderboard_display,
                hide_index=True,
            )

    except Exception:
        st.warning(
            "Leaderboard is currently unavailable."
        )

    if st.button("🔄 Start a new adventure"):
        del st.session_state.quest
        st.rerun()

    st.stop()


question = quest["questions"][quest["index"]]
key = f"{quest['run_id']}_{question['id']}"

answered = (
    len(quest["results"]) > quest["index"]
)

st.markdown(
    f"### Question {quest['index'] + 1}/"
    f"{len(quest['questions'])} · "
    f"{question['difficulty']}"
)

st.caption(
    f"{question['question_type'].replace('_', ' ').title()} · "
    f"Up to {POINTS[question['difficulty']][0]} points"
)

st.write(question["instruction"])

if question["latex"]:
    st.latex(question["latex"])

response = None


if not answered:
    if question["question_type"] == "numeric":
        response = st.text_input(
            "Your answer",
            key=key,
            placeholder="e.g. 20, 0.5, 1/2, 1 1/2 or 50%",
        )

        st.caption(
            "Use the units in the question; "
            "type the number only. "
            "Fractions and exact equivalent decimals "
            "or percentages are accepted. "
            "Do not round unless asked."
        )

    elif question["question_type"] == "mcq":
        response = st.radio(
            "Choose one answer",
            question["options"],
            index=None,
            format_func=str,
            key=key,
        )

    elif question["question_type"] == "matching":
        response = []

        for i, problem in enumerate(question["pairs"]):
            st.write(
                f"**{chr(65 + i)}.** {problem['prompt']}"
            )

            if problem["latex"]:
                st.latex(problem["latex"])

            selected_answer = st.selectbox(
                "Choose the matching answer",
                question["options"],
                index=None,
                format_func=str,
                key=f"{key}_match_{i}",
            )

            response.append(selected_answer)

    else:
        for problem in question["problems"]:
            st.write(
                f"**{problem['label']}.** "
                f"{problem['prompt']}"
            )

            if problem["latex"]:
                st.latex(problem["latex"])

        response = ordering(
            question["cards"],
            key,
        )

    if quest["hints"] < 3:
        if st.button(
            f"💡 Ask Waddle for hint {quest['hints'] + 1}",
            key=key + "_hint",
        ):
            quest["hints"] += 1
            st.rerun()

    for hint in question["hints"][:quest["hints"]]:
        st.info("🐧 " + hint)

    available_points = POINTS[
        question["difficulty"]
    ][quest["hints"]]

    st.caption(
        f"Correct answer now earns {available_points} points."
    )

    if st.button(
        "🐧 Submit answer",
        type="primary",
        key=key + "_submit",
    ):
        complete = (
            response is not None
            and response != ""
            and (
                not isinstance(response, list)
                or all(
                    value is not None
                    for value in response
                )
            )
        )

        if (
            question["question_type"] == "numeric"
            and complete
        ):
            try:
                number(response)

            except (ValueError, ZeroDivisionError):
                complete = False

                st.warning(
                    "Use a valid number or fraction, "
                    "without units. "
                    "A fraction cannot have zero "
                    "as its denominator."
                )

        if not complete:
            st.warning(
                "Complete your answer before submitting."
            )

        else:
            record(
                quest["results"],
                question,
                response,
                quest["hints"],
            )
            st.rerun()


else:
    result = quest["results"][quest["index"]]

    if result["correct"]:
        st.success(
            f"🎉 Waddle-tastic! "
            f"+{result['points']} points!"
        )

    else:
        st.info(
            "🐧 Good effort. Study the solution, "
            "then try the next problem."
        )

    st.write(
        "Your submitted answer:",
        str(result["response"]),
    )

    st.markdown("**Solution**")

    if question["question_type"] in [
        "matching",
        "drag_drop",
    ]:
        problems = question.get(
            "pairs",
            question.get("problems", []),
        )

        for problem in problems:
            st.latex(problem["solution"])

        if question["question_type"] == "drag_drop":
            st.write(
                "Correct order: "
                + " → ".join(question["answer"])
            )

    else:
        st.latex(question["solution"])

    is_last_question = (
        quest["index"] + 1 == len(quest["questions"])
    )

    next_button_label = (
        "Finish adventure 🏆"
        if is_last_question
        else "Next adventure ➜"
    )

    if st.button(
        next_button_label,
        type="primary",
        key=key + "_next",
    ):
        quest["index"] += 1
        quest["hints"] = 0
        st.rerun()
