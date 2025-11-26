import streamlit as st
from random import shuffle

st.set_page_config(page_title="Karteikarten", page_icon="📚", layout="centered")

# --- INITIALISIERUNG ---
if "topics" not in st.session_state:
    st.session_state.topics = {}  # {topic_name: {"color": "#fff", "cards": [{"front":..., "back":...}]}}
if "page" not in st.session_state:
    st.session_state.page = "home"
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None
if "learn_queue" not in st.session_state:
    st.session_state.learn_queue = []
if "show_back" not in st.session_state:
    st.session_state.show_back = False


# --- SEITENWECHSEL FUNKTION ---
def go(page, topic=None):
    st.session_state.page = page
    if topic:
        st.session_state.current_topic = topic
    st.session_state.show_back = False


# -------------------------
#       HOME / THEMEN
# -------------------------
if st.session_state.page == "home":

    st.title("📚 Karteikarten")

    st.header("Deine Themen:")

    if len(st.session_state.topics) == 0:
        st.info("Noch keine Themen vorhanden.")

    for topic, data in st.session_state.topics.items():
        color = data["color"]
        if st.button(topic, key=topic, help="Thema öffnen"):
            # Lernqueue vorbereiten
            cards = data["cards"].copy()
            shuffle(cards)
            st.session_state.learn_queue = cards
            go("learn", topic)

    st.write("---")
    st.subheader("➕ Neues Thema erstellen")
    if st.button("➕ Thema hinzufügen"):
        go("new_topic")


# -------------------------
#      NEUES THEMA
# -------------------------
elif st.session_state.page == "new_topic":

    st.title("➕ Neues Thema erstellen")

    name = st.text_input("Name des Themas")
    color = st.color_picker("Farbe der Karten", "#3b82f6")

    st.subheader("Karten hinzufügen")
    if "new_cards" not in st.session_state:
        st.session_state.new_cards = []

    # Neue Karte eingeben
    front = st.text_input("Vorderseite", key="front_input")
    back = st.text_input("Rückseite", key="back_input")

    if st.button("➕ Karte hinzufügen"):
        if front and back:
            st.session_state.new_cards.append({"front": front, "back": back})
            st.session_state.front_input = ""
            st.session_state.back_input = ""
        else:
            st.warning("Bitte beide Seiten ausfüllen.")

    # Kartenliste anzeigen
    for c in st.session_state.new_cards:
        st.write(f"• **{c['front']}** → {c['back']}")

    st.write("---")

    if st.button("💾 Speichern"):
        if name == "":
            st.warning("Bitte einen Namen eingeben.")
        else:
            st.session_state.topics[name] = {
                "color": color,
                "cards": st.session_state.new_cards.copy()
            }
            st.session_state.new_cards = []
            go("home")

    if st.button("⬅️ Abbrechen"):
        st.session_state.new_cards = []
        go("home")


# -------------------------
#        LERNMODUS
# -------------------------
elif st.session_state.page == "learn":

    topic = st.session_state.current_topic
    data = st.session_state.topics[topic]
    color = data["color"]

    st.title(f"📘 Lernen: {topic}")

    if len(st.session_state.learn_queue) == 0:
        st.success("🎉 Alle Karten gelernt!")
        if st.button("⬅️ Zurück zum Menü"):
            go("home")
        st.stop()

    card = st.session_state.learn_queue[0]

    # Karte darstellen
    st.markdown(
        f"""
        <div style='padding:20px; background:{color}; border-radius:10px; text-align:center; font-size:24px;'>
            {card['back'] if st.session_state.show_back else card['front']}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Buttons
    st.write("")
    if not st.session_state.show_back:
        if st.button("🔄 Umdrehen"):
            st.session_state.show_back = True
    else:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("❌ Nicht gewusst"):
                # Karte ans Ende setzen
                st.session_state.learn_queue.append(st.session_state.learn_queue.pop(0))
                st.session_state.show_back = False

        with col2:
            if st.button("✔️ Gewusst"):
                st.session_state.learn_queue.pop(0)
                st.session_state.show_back = False

    st.write("---")
    if st.button("⬅️ Zurück"):
        go("home")
