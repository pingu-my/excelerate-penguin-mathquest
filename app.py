from pathlib import Path
from uuid import uuid4
import base64
import csv
import io
import re
from html import escape

import streamlit as st
import streamlit.components.v1 as components

from curriculum import PATHS, DIFFICULTIES, POINTS, available_topics
from question_engine import build_adventure
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
    app_view = st.radio(
        "Open",
        ["Student adventure", "Teacher dashboard"],
        key="app_view",
    )

if app_view == "Teacher dashboard":
    try:
        from teacher_dashboard import teacher_dashboard
    except ModuleNotFoundError as exc:
        if exc.name != "teacher_dashboard":
            raise
        st.error(
            "Teacher dashboard is not installed yet. "
            "Add teacher_dashboard.py to the same folder as app.py. "
            "You can still select Student adventure in the sidebar."
        )
        st.stop()

    teacher_dashboard()
    st.stop()


# Embedded artwork: no additional image files are needed.
PENGUIN = """
<svg viewBox="0 0 180 200" role="img"
     aria-label="Waddle the happy penguin">
<ellipse cx="90" cy="185" rx="65" ry="9" fill="#aad9e6"/>
<ellipse cx="90" cy="106" rx="58" ry="77" fill="#263b54"/>
<ellipse cx="90" cy="122" rx="44" ry="55" fill="#fffdf7"/>
<ellipse cx="65" cy="76" rx="22" ry="26" fill="#fffdf7"/>
<ellipse cx="115" cy="76" rx="22" ry="26" fill="#fffdf7"/>
<circle cx="67" cy="77" r="5" fill="#263b54"/>
<circle cx="113" cy="77" r="5" fill="#263b54"/>
<g fill="none" stroke="#65bed2" stroke-width="4">
<circle cx="65" cy="78" r="19"/>
<circle cx="115" cy="78" r="19"/>
<path d="M84 78h12"/>
</g>
<ellipse cx="47" cy="99" rx="10" ry="6" fill="#ffb5bb"/>
<ellipse cx="133" cy="99" rx="10" ry="6" fill="#ffb5bb"/>
<path d="M79 100 Q90 117 101 100 Q90 92 79 100"
      fill="#ffbd5b"/>
<path d="M35 111 Q3 129 22 153 L45 134
         M145 111 Q173 84 167 70 Q150 83 137 118"
      fill="#263b54"/>
<path d="M49 116 Q90 132 131 116"
      fill="none" stroke="#a58bd5" stroke-width="13"/>
<path d="M116 122v26" stroke="#a58bd5" stroke-width="13"/>
<ellipse cx="64" cy="181" rx="22" ry="9" fill="#ffbd5b"/>
<ellipse cx="117" cy="181" rx="22" ry="9" fill="#ffbd5b"/>
<path d="M64 140l26 6 26-6v26l-26 6-26-6z"
      fill="#75c9b4" stroke="#fff" stroke-width="3"/>
<path d="M90 146v26" stroke="#fff" stroke-width="3"/>
</svg>
"""

st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(
        160deg, #e7f7ff 0%, #f4f0ff 55%, #fff7e8 100%
    );
    color: #263b54;
}
[data-testid="stMainBlockContainer"] {
    max-width: 850px;
    padding-top: 2rem;
}
[data-testid="stSidebar"] {
    background: #f1faff;
}
h1, h2, h3, p, label {
    color: #263b54;
}
[data-testid="stWidgetLabel"] p {
    font-weight: 700;
    font-size: 1rem;
}
[data-testid="stTextInput"] input {
    font-size: 1.15rem;
    min-height: 48px;
}
.stButton button, .stDownloadButton button {
    border-radius: 18px;
    min-height: 48px;
    font-weight: 700;
    border: 2px solid #b8dbe7;
}
.stButton button[kind="primary"] {
    background: #316ba4;
    color: white;
    border-color: #316ba4;
    box-shadow: 0 4px 0 #244d78;
}
[data-testid="stMetric"] {
    background: #ffffff;
    border: 2px solid #daebf3;
    border-radius: 20px;
    padding: 14px;
}
[data-testid="stAlert"] {
    border-radius: 18px;
}
.hero {
    display: flex;
    align-items: center;
    gap: 22px;
    background: #ffffffdd;
    border: 3px solid white;
    border-radius: 30px;
    padding: 22px;
    box-shadow: 0 9px 28px #80a4bb20;
}
.hero svg {
    width: 130px;
    flex-shrink: 0;
    animation: waddle 3s ease-in-out infinite;
}
.hero h1 {
    font-size: clamp(1.55rem, 4vw, 2.2rem);
    margin: 6px 0;
    line-height: 1.15;
}
.eyebrow {
    font-size: .8rem;
    font-weight: 800;
    letter-spacing: .12em;
    color: #526d8c;
}
.hero p {
    margin: 8px 0;
    font-size: 1.05rem;
}
.pill {
    display: inline-block;
    background: #eee8ff;
    border-radius: 30px;
    padding: 7px 12px;
    font-weight: 700;
    font-size: .85rem;
    color: #5a4583;
}
.map {
    display: flex;
    gap: 8px;
    justify-content: space-between;
    margin: 18px 0;
}
.stop {
    flex: 1;
    text-align: center;
    background: #ffffffb3;
    border: 2px solid #d8e8ef;
    border-radius: 18px;
    padding: 12px 4px;
    font-size: .8rem;
}
.stop b {
    display: block;
    font-size: 1.5rem;
}
.stop.active {
    background: #e6f8f0;
    border-color: #5ea995;
    box-shadow: 0 3px 0 #b7ded0;
}
.bubble {
    background: #fff;
    border: 2px solid #d6eaf1;
    border-radius: 20px;
    padding: 14px 18px;
    margin: 16px 0;
    font-size: 1.05rem;
}
.badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 14px 0;
}
.badge {
    background: #fff0c9;
    border-radius: 20px;
    padding: 9px 13px;
    color: #65501e;
    font-weight: 700;
}
@keyframes waddle {
    0%, 100% {
        transform: rotate(-3deg) translateY(0);
    }
    50% {
        transform: rotate(3deg) translateY(-4px);
    }
}
@media (prefers-reduced-motion: reduce) {
    .hero svg {
        animation: none;
    }
}
@media (max-width: 540px) {
    .hero {
        gap: 12px;
        padding: 16px;
    }
    .hero svg {
        width: 85px;
    }
    .stop {
        font-size: .7rem;
    }
    .map {
        gap: 4px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


def fraction_text(value):
    """Format fractions without changing stored answers."""
    pattern = (
        r"(?<![\w/])"
        r"(?:(-?\d+)\s+)?"
        r"(-?\d+)\s*/\s*(\d+)"
        r"(?![\w/])"
    )

    def replace(match):
        whole, numerator, denominator = match.groups()
        fraction = rf"\dfrac{{{numerator}}}{{{denominator}}}"
        prefix = whole + r"\," if whole is not None else ""
        return "$" + prefix + fraction + "$"

    return re.sub(pattern, replace, str(value))


def math_text(value):
    st.markdown(fraction_text(value))


def answer_choices(label, options, key):
    """Show stacked fractions while preserving original answer values."""
    letters = [chr(65 + i) for i in range(len(options))]
    st.caption("Read the answer cards, then choose their letter.")

    columns = st.columns(2)

    for i, option in enumerate(options):
        with columns[i % 2]:
            st.markdown(f"**{letters[i]}**")
            value = str(option)
            match = re.fullmatch(
                r"(-?\d+)\s*/\s*(\d+)",
                value,
            )

            if match:
                st.latex(
                    rf"\dfrac{{{match[1]}}}{{{match[2]}}}"
                )
            else:
                st.latex(value)

    selected = st.radio(
        label,
        letters,
        index=None,
        horizontal=True,
        key=key,
    )

    if selected is None:
        return None

    return options[letters.index(selected)]


def show_hint(hint):
    if hint.startswith("Try this calculation: "):
        st.info("🐧 Try this calculation:")
        st.latex(hint.split(": ", 1)[1])

    elif hint.startswith("Calculations to try: "):
        st.info("🐧 Try these calculations:")

        for expression in hint.split(": ", 1)[1].split("; "):
            st.latex(expression)

    else:
        st.info("🐧 " + fraction_text(hint))


def show_response(value):
    if isinstance(value, list):
        for i, answer in enumerate(value):
            math_text(f"**{chr(65 + i)}:** {answer}")
    else:
        math_text(value)


def game_message(message):
    st.markdown(
        '<div class="bubble">'
        "🐧 <b>Waddle says:</b> "
        f"{escape(message)}"
        "</div>",
        unsafe_allow_html=True,
    )


def rewards(results):
    """Fish and streak rewards do not change assessment points."""
    streak = 0
    best = 0
    correct = 0

    for result in results:
        if result["correct"]:
            correct += 1
            streak += 1
            best = max(best, streak)
        else:
            streak = 0

    return {
        "fish": correct,
        "streak": streak,
        "best": best,
    }


def adventure_map(completed, total):
    places = [
        ("🏕️", "Ice Camp"),
        ("🧊", "Frozen Lake"),
        ("🏔️", "Glacier"),
        ("👑", "Penguin Kingdom"),
    ]

    stage = min(3, int(3 * completed / max(total, 1)))
    cards = []

    for i, (icon, label) in enumerate(places):
        active = "active" if i <= stage else ""
        marker = "<br>🐧 You are here" if i == stage else ""

        cards.append(
            f'<div class="stop {active}">'
            f"<b>{icon}</b>{label}{marker}"
            "</div>"
        )

    st.markdown(
        '<div class="map" aria-label="Adventure journey">'
        + "".join(cards)
        + "</div>",
        unsafe_allow_html=True,
    )


def csv_value(value):
    value = str(value)

    if value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value

    return value


st.markdown(
    f'<div class="hero">{PENGUIN}'
    "<div>"
    '<div class="eyebrow">EXCELERATE LEARNING SPACE</div>'
    "<h1>Penguin MathQuest</h1>"
    "<p>Little steps. Big discoveries. "
    "Let’s learn with Waddle!</p>"
    '<span class="pill">🐟 Solve • Collect • Explore</span>'
    "</div></div>",
    unsafe_allow_html=True,
)


@st.cache_data
def load_music(music_path, modified_time):
    """Cache music and refresh when the file changes."""
    return base64.b64encode(
        Path(music_path).read_bytes()
    ).decode("ascii")


with st.sidebar:
    st.header("🐧 Waddle’s corner")

    st.write(
        "Use paper for your working. "
        "Think carefully before submitting."
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

    if "quest" in st.session_state:
        if st.button("Return to start"):
            del st.session_state.quest
            st.rerun()


if "quest" not in st.session_state:
    adventure_map(0, 10)

    game_message(
        "Help me reach Penguin Kingdom! "
        "Each correct answer earns a fish. "
        "Take your time and use a hint whenever you need one."
    )

    st.subheader("🎒 Pack your adventure bag")

    name = st.text_input(
        "Student first name or nickname",
        max_chars=50,
    )

    year = st.selectbox(
        "Primary year",
        [4, 5, 6],
    )

    syllabus = st.selectbox(
        "Learning path",
        PATHS,
    )

    topic = st.selectbox(
        "Mathematics topic",
        available_topics(year, syllabus),
    )

    mode = st.radio(
        "Adventure level",
        DIFFICULTIES + ["All three levels"],
    )

    st.write(
        "10 questions per level · "
        "All three levels = 30 questions"
    )

    st.caption(
        "Starter practice uses shared mathematics skills. "
        "The learning path is recorded in your results; "
        "this version does not claim official curriculum alignment."
    )

    consent = st.checkbox(
        "Show my nickname and completed result "
        "on this app’s leaderboard",
        value=False,
    )

    if st.button(
        "🐧 Let’s waddle!",
        type="primary",
    ):
        if not name.strip():
            st.warning(
                "Enter your first name or nickname to begin."
            )

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
                    year,
                    syllabus,
                    topic,
                    mode,
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
loot = rewards(quest["results"])

adventure_map(
    len(quest["results"]),
    len(quest["questions"]),
)

st.subheader(
    f"Primary {profile['year']} · {profile['topic']}"
)

c1, c2, c3 = st.columns(3)
c1.metric("⭐ Points", stats["score"])
c2.metric("🐟 Fish collected", loot["fish"])
c3.metric("🔥 Streak", loot["streak"])

st.progress(
    len(quest["results"])
    / max(1, len(quest["questions"]))
)

st.caption(
    f"{len(quest['results'])} of "
    f"{len(quest['questions'])} questions explored · "
    "A fish for every correct answer!"
)


if quest["index"] == len(quest["questions"]):
    st.success(
        "🏆 Adventure complete! "
        "Keep waddling towards excellence!"
    )

    st.write(
        f"**{stats['correct']}/{stats['questions']} correct · "
        f"{stats['accuracy']:.1f}% accuracy · "
        f"{stats['score']} points**"
    )

    game_message(
        f"You made it, {profile['name']}! "
        f"You collected {loot['fish']} fish and "
        f"your best streak was {loot['best']}. "
        "Every question helps your maths grow."
    )

    badges = ["🏁 Adventure explorer"]

    if loot["fish"] >= 1:
        badges.append("🐟 First fish")

    if loot["best"] >= 3:
        badges.append("🔥 Three in a row")

    if stats["accuracy"] >= 80:
        badges.append("⭐ Maths star")

    if stats["accuracy"] == 100:
        badges.append("👑 Perfect penguin")

    st.markdown(
        '<div class="badges">'
        + "".join(
            f'<span class="badge">{badge}</span>'
            for badge in badges
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    if not quest.get("celebrated"):
        quest["celebrated"] = True
        st.balloons()

    missed = list(
        dict.fromkeys(
            question["difficulty"]
            for question, result in zip(
                quest["questions"],
                quest["results"],
            )
            if not result["correct"]
        )
    )

    if missed:
        st.info(
            "🎯 Your next mission: review the solutions below, "
            "then practise "
            + ", ".join(map(str, missed))
            + " again."
        )

    level_results = []

    for difficulty in dict.fromkeys(
        result["difficulty"]
        for result in quest["results"]
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

    for result in quest["results"]:
        writer.writerow(
            {
                field: csv_value(result.get(field, ""))
                for field in writer.fieldnames
            }
        )

    st.download_button(
        "Download my question results (CSV)",
        output.getvalue(),
        file_name="MathQuest_Results.csv",
        mime="text/csv",
    )

    with st.expander(
        "Review your questions and solutions"
    ):
        for i, (question, result) in enumerate(
            zip(
                quest["questions"],
                quest["results"],
            ),
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

            math_text(question["instruction"])

            if question["latex"]:
                st.latex(
                    question["latex"].replace(
                        r"\frac",
                        r"\dfrac",
                    )
                )

            if question["question_type"] in [
                "matching",
                "drag_drop",
            ]:
                problems = question.get(
                    "pairs",
                    question.get("problems", []),
                )

                for problem in problems:
                    math_text(problem["prompt"])

                    st.latex(
                        problem["solution"].replace(
                            r"\frac",
                            r"\dfrac",
                        )
                    )

                if question["question_type"] == "drag_drop":
                    st.write(
                        "Order: "
                        + " → ".join(question["answer"])
                    )

            else:
                st.latex(
                    question["solution"].replace(
                        r"\frac",
                        r"\dfrac",
                    )
                )

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
                for i, entry in enumerate(
                    entries[:10],
                    1,
                )
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
    f"### ❄️ Challenge {quest['index'] + 1}/"
    f"{len(quest['questions'])} · "
    f"{question['difficulty']}"
)

st.caption(
    f"{question['question_type'].replace('_', ' ').title()} · "
    f"Up to {POINTS[question['difficulty']][0]} points"
)

math_text(question["instruction"])

if question["latex"]:
    st.latex(
        question["latex"].replace(
            r"\frac",
            r"\dfrac",
        )
    )

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
        response = answer_choices(
            "Choose one answer",
            question["options"],
            key,
        )

    elif question["question_type"] == "matching":
        response = []

        for i, problem in enumerate(question["pairs"]):
            math_text(
                f"**{chr(65 + i)}.** "
                f"{problem['prompt']}"
            )

            if problem["latex"]:
                st.latex(
                    problem["latex"].replace(
                        r"\frac",
                        r"\dfrac",
                    )
                )

            selected_answer = answer_choices(
                f"Choose the matching answer for {chr(65 + i)}",
                question["options"],
                f"{key}_match_{i}",
            )

            response.append(selected_answer)

    else:
        for problem in question["problems"]:
            math_text(
                f"**{problem['label']}.** "
                f"{problem['prompt']}"
            )

            if problem["latex"]:
                st.latex(
                    problem["latex"].replace(
                        r"\frac",
                        r"\dfrac",
                    )
                )

        response = ordering(
            question["cards"],
            key,
        )

    if quest["hints"] < min(
        3,
        len(question["hints"]),
        len(POINTS[question["difficulty"]]) - 1,
    ):
        if st.button(
            f"💡 Ask Waddle for hint {quest['hints'] + 1}",
            key=key + "_hint",
        ):
            quest["hints"] += 1
            st.rerun()

    for hint in question["hints"][:quest["hints"]]:
        show_hint(hint)

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
            "🎉 Waddle-tastic! "
            f"+{result['points']} points and +1 fish!"
        )

    else:
        st.info(
            "🐧 Good effort. Study the solution, "
            "then try the next problem."
        )

    if result["correct"] and loot["streak"] >= 3:
        game_message(
            "Amazing thinking! "
            f"{loot['streak']} correct answers in a row!"
        )

    elif not result["correct"]:
        game_message(
            "Mistakes help us learn! "
            "Compare your working with the solution, "
            "then explain the next step to yourself."
        )

    st.markdown("**Your submitted answer:**")
    show_response(result["response"])

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
            st.latex(
                problem["solution"].replace(
                    r"\frac",
                    r"\dfrac",
                )
            )

        if question["question_type"] == "drag_drop":
            st.write(
                "Correct order: "
                + " → ".join(question["answer"])
            )

    else:
        st.latex(
            question["solution"].replace(
                r"\frac",
                r"\dfrac",
            )
        )

    is_last_question = (
        quest["index"] + 1 == len(quest["questions"])
    )

    next_button_label = (
        "Finish adventure 🏆"
        if is_last_question
        else "Next ice step ➜"
    )

    if st.button(
        next_button_label,
        type="primary",
        key=key + "_next",
    ):
        quest["index"] += 1
        quest["hints"] = 0
        st.rerun()
