import random
import streamlit as st



# PAGE CONFIGURATION


st.set_page_config(
    page_title="EcoPulse",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="auto"
)


# MISSION POOL


MISSION_POOL = [
    "🌸 Find a flowering plant.",
    "🐝 Find an insect interacting with a plant.",
    "🍃 Find two leaves that look different.",
    "💧 Find a water drop resting on a leaf.",
    "🪶 Find a feather on the ground.",
    "🌳 Find a tree with unusual bark.",
    "🕷️ Find a spider web.",
    "🌱 Find a small plant growing near a larger plant.",
    "🐜 Find ants working together.",
    "🌼 Find a flower being visited by an insect.",
    "🍂 Find a leaf that has started changing color.",
    "🌿 Find a plant growing in an unusual place.",
    "🐦 Spot a bird and observe it without disturbing it.",
    "🪨 Find a natural object with an interesting texture.",
    "☀️ Find a plant growing in a sunny location.",
]

# SESSION STATE
#

if "score" not in st.session_state:
    st.session_state.score = 0

if "missions" not in st.session_state:
    st.session_state.missions = random.sample(
        MISSION_POOL,
        5
    )

if "completed_missions" not in st.session_state:
    st.session_state.completed_missions = 0

if "exploring" not in st.session_state:
    st.session_state.exploring = False


# HEADER


st.title("🌱 EcoPulse")

st.subheader(
    "Turn your walk into a biodiversity adventure."
)

st.write(
    "Complete outdoor missions, discover local biodiversity, "
    "and use AI to learn about what you find."
)

st.divider()


# BIO-BLITZ MISSIONS


st.header("🌿 Today's Bio-Blitz")

st.write(
    "Complete these missions while exploring the world around you."
)

for i, mission in enumerate(
    st.session_state.missions,
    start=1
):
    st.info(
        f"🎯 **Mission {i}:** {mission}"
    )



# START EXPLORING


if st.button(
    "🚶 Start Exploring",
    use_container_width=True
):
    st.session_state.exploring = True

    st.success(
        "Great! Put your phone away and start exploring. 🌳"
    )


if st.session_state.exploring:
    st.caption(
        "💡 Tip: Spend a few minutes observing your surroundings "
        "before taking out your phone."
    )


st.divider()


# PROGRESS


st.header("🌱 Your Progress")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "BioPoints",
        st.session_state.score
    )

with col2:
    st.metric(
        "Missions",
        f"{st.session_state.completed_missions} / 5"
    )


st.divider()

# RECORD DISCOVERY
# ============================================================

st.header("📸 Record Your Discovery")

st.write(
    "Found something interesting outside? "
    "Take a photo and upload it here."
)

uploaded_file = st.file_uploader(
    "Upload your discovery",
    type=["jpg", "jpeg", "png"]
)


# ============================================================
# DISPLAY UPLOADED IMAGE
# ============================================================

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Your discovery",
        use_container_width=True
    )

    st.write(
        "Ready to learn more about your discovery?"
    )

    if st.button(
        "🔍 Analyze Discovery",
        use_container_width=True
    ):

        st.info(
            "🤖 AI analysis will be connected here next."
        )


st.divider()


# ============================================================
# AI DISCOVERY
# ============================================================

st.header("🔎 AI Discovery")

st.write(
    "Your AI identification and biodiversity information "
    "will appear here."
)

st.write("**Identification:** —")

st.write("**Explanation:** —")

st.write("**BioPoints earned:** —")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌱 EcoPulse — Explore more. Scroll less."
)