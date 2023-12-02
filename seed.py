import streamlit as st

# Declare tools for openai assistant to use
tools = [
    {
        "type": "function",
        "function": {
            "name": "update_map",
            "description": "Update map to center on a particular location",
            "parameters": {
                "type": "object",
                "properties": {
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location to center the map on"
                    },
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location to center the map on"
                    },
                    "zoom": {
                        "type": "integer",
                        "description": "Zoom level of the map"
                    }
                },
                "required": ["longitude", "latitude", "zoom"]
            }
        }
    },
    {
        "type": "function",
        "function":  {
            "name": "add_markers",
            "description": "Add list of markers to the map",
            "parameters": {
                "type": "object",
                "properties": {
                    "longitudes": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "List of longitude of the location to each marker"
                    },
                    "latitudes": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "List of latitude of the location to each marker"
                    },
                    "labels": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of text to display on the location of each marker"
                    }
                },
                "required": ["longitudes", "latitudes", "labels"]
            }
        }
    },

]


# We will update map state in session state
def update_map(longitude: float, latitude: float, zoom: int):
    """Update map to center on a particular location."""
    st.session_state["map"] = {
        "latitude": latitude,
        "longitude": longitude,
        "zoom": zoom,
    }

    return "Map updated!"


def add_markers(latitudes: float, longitudes: float, labels: str):
    """OpenAI tool to update markers in-app
    """

    st.session_state["markers_state"] = {
        "lat": latitudes,
        "lon": longitudes,
        "text": labels,
    }
    return "Markers added"


available_functions = {
    "update_map": update_map,
    "add_marker": add_markers,
}

SEED_INSTRUCTION = "You are a helpful travel assistant that can write and execute code, and has access to a digital map to display information."