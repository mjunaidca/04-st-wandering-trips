import streamlit as st
import os
import plotly.graph_objects as go

from assistant import AITripPlanner
from seed import SEED_INSTRUCTION, tools

MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_TOKEN")

st.set_page_config(
    page_title="Wandering AI Trips",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.header("Wandering AI Trips")

# Initialize and SETUP ASSISTANT
wander_ai_manager: AITripPlanner = AITripPlanner()

wander_ai_assistant = wander_ai_manager.create_assistant(
    name="Wandering AI Trips",
    instructions=SEED_INSTRUCTION,
    tools=tools,
    file_obj=[],
)

thread = wander_ai_manager.create_thread()

# INITIALIZE AND SETUO SESSION STATES
if "map" not in st.session_state:
    st.session_state.map = {
        "latitude": 39.949610,
        "longitude": -75.150282,
        "zoom": 16,
    }

if "markers_state" not in st.session_state:
    st.session_state.markers_state = None

if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = []


def on_text_input():
    """Callback method for any chat_input value change"""

    if st.session_state.input_user_msg == "":
        return

    st.session_state.conversation_state.append(
        ("user", st.session_state.input_user_msg)
    )

    wander_ai_manager.add_message_to_thread(
        content=st.session_state.input_user_msg,
        role="user",
    )

    run = wander_ai_manager.run_assistant(instructions=SEED_INSTRUCTION)

    final_res = wander_ai_manager.wait_for_completion(run=run, thread=thread)

    st.session_state.conversation_state = [
        (m.role, m.content[0].text.value)
        for m in final_res.data
    ]


left_col, right_col = st.columns(2)

with left_col:
    for role, message in st.session_state.conversation_state:
        with st.chat_message(role):
            st.write(message)

with right_col:
    figure = go.Figure(go.Scattermapbox(
        mode="markers"
    ))
    if st.session_state.markers_state is not None:
        figure.add_trace(
            go.Scattermapbox(
                mode="markers",
                marker=go.scattermapbox.Marker(
                    size=24,
                    color="red",
                ),
                lat=st.session_state.markers_state["latitudes"],
                lon=st.session_state.markers_state["longitudes"],
                text=st.session_state.markers_state["labels"],
            )
        )
    figure.update_layout(
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            center=go.layout.mapbox.Center(
                lat=st.session_state.map["latitude"],
                lon=st.session_state.map["longitude"]
            ),
            zoom=st.session_state.map["zoom"]
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(
        figure,
        config={"displayModeBar": False},
        use_container_width=True,
        key="plotly"
    )

st.chat_input(
    placeholder="Type a message...",
    key="input_user_msg",
    on_submit=on_text_input
)
