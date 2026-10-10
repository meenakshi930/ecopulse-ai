import streamlit as st

from ai.missions import generate_missions


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EcoPulse",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="auto"
)


# ============================================================
# SESSION STATE
# ============================================================

if "score" not in st.session_state:
    st.session_state.score = 0

if "missions" not in st.session_state:
    st.session_state.missions = []

if "completed_missions" not in st.session_state:
    st.session_state.completed_missions = 0

if "exploring" not in st.session_state:
    st.session_state.exploring = False


# ============================================================
# HEADER
# ============================================================

st.title("🌱 EcoPulse")

st.subheader(
    "Turn your walk into a biodiversity adventure."
)

st.write(
    "Complete outdoor missions, discover local biodiversity, "
    "and use AI to learn about what you find."
)

st.divider()


# ============================================================
# EXPLORATION PREFERENCES
# ============================================================

st.header("🌍 Choose Your Exploration")

environment = st.selectbox(
    "Where are you exploring?",
    [
        "Park",
        "College Campus",
        "Garden",
        "Forest",
        "Street",
        "Lake Area"
    ]
)

difficulty = st.selectbox(
    "Mission difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

biodiversity_type = st.selectbox(
    "What do you want to observe?",
    [
        "General Biodiversity",
        "Plants",
        "Insects",
        "Birds",
        "Trees",
        "Flowers"
    ]
)


# ============================================================
# GENERATE AI MISSIONS
# ============================================================

if st.button(
    "🌱 Generate My Missions",
    use_container_width=True
):

    with st.spinner("🤖 Creating your biodiversity missions..."):

        missions = generate_missions(
            environment,
            difficulty,
            biodiversity_type
        )

    st.session_state.missions = missions
    st.session_state.completed_missions = 0
    st.session_state.exploring = False


st.divider()


# ============================================================
# BIO-BLITZ MISSIONS
# ============================================================

st.header("🌿 Today's Bio-Blitz")

st.write(
    "Complete these missions while exploring the world around you."
)

if st.session_state.missions:

    for i, mission in enumerate(
        st.session_state.missions,
        start=1
    ):

        st.info(
            f"🎯 **Mission {i}:** {mission}"
        )

else:

    st.info(
        "Choose your exploration preferences and "
        "generate your missions to begin."
    )


# ============================================================
# START EXPLORING
# ============================================================

if st.session_state.missions:

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


# ============================================================
# PROGRESS
# ============================================================

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


# ============================================================
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
            "🤖 AI image analysis will be connected here next."
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
