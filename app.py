from pathlib import Path
from uuid import uuid4
import base64
import csv
import io
from html import escape

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

# All artwork is embedded: no additional images or downloads are needed.
PENGUIN = """<svg viewBox="0 0 180 200" role="img" aria-label="Waddle the happy penguin">
<ellipse cx="90" cy="185" rx="65" ry="9" fill="#aad9e6"/>
<ellipse cx="90" cy="106" rx="58" ry="77" fill="#263b54"/>
<ellipse cx="90" cy="122" rx="44" ry="55" fill="#fffdf7"/>
<ellipse cx="65" cy="76" rx="22" ry="26" fill="#fffdf7"/>
<ellipse cx="115" cy="76" rx="22" ry="26" fill="#fffdf7"/>
<circle cx="67" cy="77" r="5" fill="#263b54"/><circle cx="113" cy="77" r="5" fill="#263b54"/>
<g fill="none" stroke="#65bed2" stroke-width="4"><circle cx="65" cy="78" r="19"/>
<circle cx="115" cy="78" r="19"/><path d="M84 78h12"/></g>
<ellipse cx="47" cy="99" rx="10" ry="6" fill="#ffb5bb"/>
<ellipse cx="133" cy="99" rx="10" ry="6" fill="#ffb5bb"/>
<path d="M79 100 Q90 117 101 100 Q90 92 79 100" fill="#ffbd5b"/>
<path d="M35 111 Q3 129 22 153 L45 134M145 111 Q173 84 167 70 Q150 83 137 118" fill="#263b54"/>
<path d="M49 116 Q90 132 131 116" fill="none" stroke="#a58bd5" stroke-width="13"/>
<path d="M116 122v26" stroke="#a58bd5" stroke-width="13"/>
<ellipse cx="64" cy="181" rx="22" ry="9" fill="#ffbd5b"/>
<ellipse cx="117" cy="181" rx="22" ry="9" fill="#ffbd5b"/>
<path d="M64 140l26 6 26-6v26l-26 6-26-6z" fill="#75c9b4" stroke="#fff" stroke-width="3"/>
<path d="M90 146v26" stroke="#fff" stroke-width="3"/></svg>"""

st.markdown("""<style>
.stApp {background: linear-gradient(160deg,#e7f7ff 0%,#f4f0ff 55%,#fff7e8 100%);color:#263b54;}
[data-testid="stMainBlockContainer"] {max-width:850px;padding-top:2rem;}
[data-testid="stSidebar"] {background:#f1faff;}
h1,h2,h3,p,label {color:#263b54;}
[data-testid="stWidgetLabel"] p {font-weight:700;font-size:1rem;}
[data-testid="stTextInput"] input {font-size:1.15rem;min-height:48px;}
.stButton button,.stDownloadButton button {border-radius:18px;min-height:48px;font-weight:700;border:2px solid #b8dbe7;}
.stButton button[kind="primary"] {background:#316ba4;color:white;border-color:#316ba4;box-shadow:0 4px 0 #244d78;}
[data-testid="stMetric"] {background:#ffffff;border:2px solid #daebf3;border-radius:20px;padding:14px;}
[data-testid="stAlert"] {border-radius:18px;}
.hero {display:flex;align-items:center;gap:22px;background:#ffffffdd;border:3px solid white;border-radius:30px;padding:22px;box-shadow:0 9px 28px #80a4bb20;}
.hero svg {width:130px;flex-shrink:0;animation:waddle 3s ease-in-out infinite;}
.hero h1 {font-size:clamp(1.55rem,4vw,2.2rem);margin:6px 0;line-height:1.15;}
.eyebrow {font-size:.8rem;font-weight:800;letter-spacing:.12em;color:#526d8c;}
.hero p {margin:8px 0;font-size:1.05rem;}
.pill {display:inline-block;background:#eee8ff;border-radius:30px;padding:7px 12px;font-weight:700;font-size:.85rem;color:#5a4583;}
.map {display:flex;gap:8px;justify-content:space-between;margin:18px 0;}
.stop {flex:1;text-align:center;background:#ffffffb3;border:2px solid #d8e8ef;border-radius:18px;padding:12px 4px;font-size:.8rem;}
.stop b {display:block;font-size:1.5rem;}
.stop.active {background:#e6f8f0;border-color:#5ea995;box-shadow:0 3px 0 #b7ded0;}
.bubble {background:#fff;border:2px solid #d6eaf1;border-radius:20px;padding:14px 18px;margin:16px 0;font-size:1.05rem;}
.badges {display:flex;flex-wrap:wrap;gap:8px;margin:14px 0;}
.badge {background:#fff0c9;border-radius:20px;padding:9px 13px;color:#65501e;font-weight:700;}
@keyframes waddle {0%,100% {transform:rotate(-3deg) translateY(0)}50% {transform:rotate(3deg) translateY(-4px)}}
@media(prefers-reduced-motion:reduce) {.hero svg {animation:none;}}
@media(max-width:540px) {.hero {gap:12px;padding:16px;}.hero svg {width:85px;}.stop {font-size:.7rem;}.map {gap:4px;}}
</style>""", unsafe_allow_html=True)


def game_message(message):
    st.markdown(f'<div class="bubble">🐧 <b>Waddle says:</b> {escape(message)}</div>', unsafe_allow_html=True)


def rewards(results):
    """Cosmetic rewards never alter assessment points or leaderboard scores."""
    streak = best = correct = 0
    for result in results:
        if result["correct"]:
            correct += 1
            streak += 1
            best = max(best, streak)
