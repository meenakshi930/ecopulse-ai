import streamlit as st

from ai.missions import generate_missions
from ai.vision import analyze_discovery
from services.inaturalist import get_species_info


st.set_page_config(
    page_title="EcoPulse",
    page_icon="🌱",
    layout="centered"
)


# -----------------------------
# Session State
# -----------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "missions" not in st.session_state:
    st.session_state.missions = []

if "completed_missions" not in st.session_state:
    st.session_state.completed_missions = []

if "discovery_result" not in st.session_state:
    st.session_state.discovery_result = None

if "inaturalist_result" not in st.session_state:
    st.session_state.inaturalist_result = None


# -----------------------------
# Header
# -----------------------------

st.title("🌱 EcoPulse")
st.subheader("AI Bio-Blitz")

st.write(
    "Explore the outdoors, discover biodiversity, "
    "and learn about what you find."
)


# -----------------------------
# User Preferences
# -----------------------------

st.header("🌿 Plan Your Exploration")

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
    "Choose difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

biodiversity_type = st.selectbox(
    "What do you want to discover?",
    [
        "General Biodiversity",
        "Plants",
        "Insects",
        "Birds",
        "Trees",
        "Flowers"
    ]
)


# -----------------------------
# Generate Missions
# -----------------------------

if st.button(
    "🌱 Generate My Missions",
    use_container_width=True
):

    with st.spinner(
        "🤖 Creating your biodiversity missions..."
    ):

        missions = generate_missions(
            environment,
            difficulty,
            biodiversity_type
        )

    st.session_state.missions = missions
    st.session_state.completed_missions = []
    st.session_state.score = 0
    st.session_state.discovery_result = None
    st.session_state.inaturalist_result = None


# -----------------------------
# Display Missions
# -----------------------------

if st.session_state.missions:

    st.header("🎯 Your Missions")

    for i, mission in enumerate(
        st.session_state.missions
    ):

        st.write(
            f"### Mission {i + 1}"
        )

        st.write(mission)

        if i not in st.session_state.completed_missions:

            if st.button(
                f"✅ Complete Mission {i + 1}",
                key=f"complete_{i}"
            ):

                st.session_state.completed_missions.append(i)

                st.session_state.score += 10

                st.rerun()

        else:

            st.success("Mission completed!")


# -----------------------------
# Progress
# -----------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🌱 BioPoints",
        st.session_state.score
    )

with col2:
    st.metric(
        "🎯 Missions",
        f"{len(st.session_state.completed_missions)}/"
        f"{len(st.session_state.missions)}"
    )


# -----------------------------
# Discovery Upload
# -----------------------------

st.divider()

st.header("📸 Discover Something")

uploaded_file = st.file_uploader(
    "Upload a photo of your discovery",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file:

    st.image(
        uploaded_file,
        caption="Your discovery",
        use_container_width=True
    )

    if st.button(
        "🔍 Analyze Discovery",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 Analyzing your discovery..."
        ):

            result = analyze_discovery(
                uploaded_file
            )

        st.session_state.discovery_result = result

        identification = result.get(
            "identification",
            "Unknown"
        )

        # -----------------------------
        # iNaturalist Lookup
        # -----------------------------

        if identification != "Unknown":

            with st.spinner(
                "🌿 Finding biodiversity information..."
            ):

                species_info = get_species_info(
                    identification
                )

            st.session_state.inaturalist_result = (
                species_info
            )

        else:

            st.session_state.inaturalist_result = None


# -----------------------------
# AI Discovery Result
# -----------------------------

if st.session_state.discovery_result:

    result = st.session_state.discovery_result

    st.divider()

    st.header("🔎 AI Discovery")

    st.write(
        f"**Identification:** "
        f"{result.get('identification', 'Unknown')}"
    )

    st.write(
        f"**Confidence:** "
        f"{result.get('confidence', 'Low')}"
    )

    st.write(
        f"**Explanation:** "
        f"{result.get('explanation', '')}"
    )

    st.write(
        f"**AI Biodiversity Information:** "
        f"{result.get('biodiversity_information', '')}"
    )


# -----------------------------
# iNaturalist Result
# -----------------------------

if st.session_state.inaturalist_result:

    info = st.session_state.inaturalist_result

    st.divider()

    st.header("🌿 iNaturalist Information")

    st.write(
        f"**Scientific Name:** "
        f"{info.get('name', 'Unknown')}"
    )

    st.write(
        f"**Common Name:** "
        f"{info.get('common_name', 'Unknown')}"
    )

    st.write(
        f"**Rank:** "
        f"{info.get('rank', 'Unknown')}"
    )

    observations = info.get(
        "observations_count"
    )

    if observations is not None:

        st.write(
            f"**iNaturalist Observations:** "
            f"{observations}"
        )

    wikipedia_url = info.get(
        "wikipedia_url"
    )

    if wikipedia_url:

        st.markdown(
            f"[Learn more on Wikipedia]({wikipedia_url})"
        )


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "🌱 EcoPulse — Explore more. Scroll less."
)
