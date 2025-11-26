import streamlit as st

st.set_page_config(page_title="Karteikarten App", layout="centered")

# ---- INITIAL STATE ----
if "cards" not in st.session_state:
    st.session_state.cards = []  # Liste aus {"front":..., "back":...}
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current" not in st.session_state:
    st.session_state.current = None
if "flipped" not in st.session_state:
    st.session_state.flipped = False
if "repeat" not in st.session_state:
    st.session_state.repeat = []  # Karten, die nochmal kommen


# ---- ADD CARD FUNCTION ----
def add_card():
    front = st.session_state.front_text.strip()
    back = st.session_state.back_text.strip()
    if front and back:
        st.session_state.cards.append({"front": front, "back": back})
        st.session_state.front_text = ""
        st.session_state.back_text = ""
        st.success("Karte hinzugefügt!")


# ---- START TRAINING ----
def start_training():
    if len(st.session_state.cards) == 0:
        st.warning("Keine Karten vorhanden!")
        return
    st.session_state.queue = st.session_state.cards.copy()
    st.session_state.repeat = []
    st.session_state.current = st.session_state.queue.pop(0)
    st.session_state.flipped = False


# ---- NEXT CARD ----
def next_card(known: bool):
    if not known:
        st.session_state.repeat.append(st.session_state.current)

    if len(st.session_state.queue) > 0:
        st.session_state.current = st.session_state.queue.pop(0)
        st.session_state.flipped = False
    else:
        # Hauptstapel vorbei → Wiederholungen anhängen
        if len(st.session_state.repeat) > 0:
            st.session_state.queue = st.session_state.repeat.copy()
            st.session_state.repeat = []
            st.session_state.current = st.session_state.queue.pop(0)
            st.session_state.flipped = False
        else:
            st.session_state.current = None


# ---------------------------------------------
#                 UI
# ---------------------------------------------
st.title("📚 Karteikarten App")

st.header("Karten erstellen")
with st.form("create_form"):
    st.text_input("Vorderseite", key="front_text")
    st.text_input("Rückseite", key="back_text")
    submitted = st.form_submit_button("Karte hinzufügen")
    if submitted:
        add_card()

st.write("---")

st.header("Training starten")
if st.button("▶️ Start"):
    start_training()

# TRAINING VIEW
if st.session_state.current:
    st.subheader("Aktuelle Karte")

    if not st.session_state.flipped:
        st.info(st.session_state.current["front"])
        if st.button("Umdrehen"):
            st.session_state.flipped = True
    else:
        st.success(st.session_state.current["back"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Gewusst"):
                next_card(True)
        with col2:
            if st.button("✕ Nicht gewusst"):
                next_card(False)

# Ende der Session
elif st.session_state.queue == [] and len(st.session_state.cards) > 0:
    st.success("🎉 Training abgeschlossen! Alle Karten wurden gelernt.")
