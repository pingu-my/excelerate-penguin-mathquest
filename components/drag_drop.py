"""True ordering interaction using Streamlit's bidirectional components v2."""
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parent
@st.cache_resource
def component():
    return st.components.v2.component('waddle_order', html='<div class="board"></div>',
        css=(ROOT/'order.css').read_text(), js=(ROOT/'order.js').read_text())

def ordering(cards, key):
    state = st.session_state.get(key)
    initial = list(state.order) if state and state.order else cards
    result = component()(data={'order':initial}, default={'order':initial},
                         on_order_change=lambda: None, key=key)
    return list(result.order)
