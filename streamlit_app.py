import streamlit as st
import json
import os

st.set_page_config(page_title="Karteikarten App", layout="centered")

SAVE_FILE = "karten.json"


# ---------------- SAVE / LOAD ----------------
def save_cards():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.cards, f, ensure_ascii=False, indent=2)
    st.success("💾 Karten gespeichert!")


def load_cards():
    if not os.path.isfile(SAVE_FILE):
        st.warning("❗ Noch keine gespeicherten Karten vorhanden.")
        return

    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        st.session_state.cards = json.load(f)

    st.success("📥 Karten geladen!")


# ---------------- INITIAL STATE ----------------
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


# ---------------- ADD CARD (SAFE!) ----------------
def add_card(front, back):
    st.session_state.cards.append({"front": front, "back": back})


# ---------------- TRAINING ----------------
def start_training():
    if not st.session_state.cards:
        st.warning("Keine Karten vorhanden!")
        return

    st.session_state.queue = st.session_state.cards.copy()
    st.session_state.repeat = []
    st.session_state.current = st.session_state.queue.pop(0)
    st.session_state.flipped = False


def next_card(known):
    if not known:
        st.session_state.repeat.append(st.session_state.current)

    if st.session_state.queue:
        st.session_state.current = st.session_state.queue.pop(0)
    else:
        if st.session_state.repeat:
            st.session_state.queue = st.session_state.repeat.copy()
            st.session_state.repeat = []
            st.session_state.current = st.session_state.queue.pop(0)
        else:
            st.session_state.current = None

    st.session_state.flipped = False


# ---------------- UI ----------------
st.title("📚 Karteikarten App mit Speicherfunktion")


# ----- SPEICHERN & LADEN -----
st.subheader("💾 Speichern / 📥 Laden")
c1, c2 = st.columns(2)

with c1:
    if st.button("📥 Laden"):
        load_cards()

with c2:
    if st.button("💾 Speichern"):
        save_cards()


# ----- KARTE ERSTELLEN -----
st.header("Neue Karte hinzufügen")

front = st.text_input("Vorderseite")
back = st.text_input("Rückseite")

if st.button("➕ Karte speichern"):
    if front.strip() and back.strip():
        add_card(front.strip(), back.strip())
        st.success("Karte hinzugefügt!")
    else:
        st.warning("Bitte beide Felder ausfüllen.")

st.write(f"🗂️ Anzahl Karten: **{len(st.session_state.cards)}**")


# ----- START TRAINING -----
st.write("---")
st.header("Training")

if st.button("▶️ Start"):
    start_training()


# ----- TRAINING ANZEIGE -----
if st.session_state.current:
    st.subheader("Aktuelle Karte")

    # Vorderseite
    if not st.session_state.flipped:
        st.info(st.session_state.current["front"])
        if st.button("🔄 Umdrehen"):
            st.session_state.flipped = True

    # Rückseite
    else:
        st.success(st.session_state.current["back"])

        b1, b2 = st.columns(2)
        with b1:
            if st.button("✓ Gewusst"):
                next_card(True)
        with b2:
            if st.button("✕ Nicht gewusst"):
                next_card(False)

elif st.session_state.cards and not st.session_state.current:
    st.success("🎉 Durchgang abgeschlossen!")
