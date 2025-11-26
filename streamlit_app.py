import streamlit as st

st.set_page_config(page_title="Karteikarten App", layout="centered")

# ---- INITIAL STATE ----
if "cards" not in st.session_state:
    st.session_state.cards = []
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current" not in st.session_state:
    st.session_state.current = None
if "flipped" not in st.session_state:
    st.session_state.flipped = False
if "repeat" not in st.session_state:
    st.session_state.repeat = []
if "front_text" not in st.session_state:
    st.session_state.front_text = ""
if "back_text" not in st.session_state:
    st.session_state.back_text = ""

# ---- ADD CARD ----
def add_card():
    front = st.session_state.front_text.strip()
    back = st.session_state.back_text.strip()

    if front and back:
        st.session_state.cards.append({"front": front, "back": back})

    # Felder sicher zurücksetzen
    st.session_state.front_text = ""
    st.session_state.back_text = ""


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
    else:
        if len(st.session_state.repeat) > 0:
            st.session_state.queue = st.session_state.repeat.copy()
            st.session_state.repeat = []
            st.session_state.current = st.session_state.queue.pop(0)
        else:
            st.session_state.current = None

    st.session_state.flipped = False


# ---------------------------------------------
#                 UI
# ---------------------------------------------
st.title("📚 Karteikarten App")


# --------------------- CREATE CARDS ---------------------
st.header("Karten erstellen")

st.text_input("Vorderseite", key="front_text")
st.text_input("Rückseite", key="back_text")

if st.button("Karte hinzufügen"):
    add_card()
    st.success("Karte hinzugefügt!")


# --------------------- START TRAINING ---------------------
st.write("---")
st.header("Training starten")

if st.button("▶️ Start"):
    start_training()


# --------------------- TRAINING VIEW ---------------------
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

elif st.session_state.cards and st.session_state.queue == []:
    st.success("🎉 Training abgeschlossen! Alle Karten wurden gelernt.")
