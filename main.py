import streamlit as st
from components.sidebar import sidebar
from mermaid import generate_diagram
from prompt import SendChatRequest

def clear_submit():
    st.session_state["submit"] = False

# Set general streamlit config with title and header
st.set_page_config(page_title="MermaidGPT", page_icon="🧜‍♀️", layout="wide")
st.header("🧜‍♀️MermaidGPT")

# Initialize prompt so that it persists between runs
st.session_state.prompt = st.session_state.get('prompt', '')

def show_markdown():
    st.session_state["stage"] = "show_markdown"
    prompt = st.session_state["prompt"]
    result = SendChatRequest(prompt, st.session_state["chart_type"], st.session_state["orientation"])
    st.session_state["markdown"] = result

def show_image():
    st.session_state["stage"] = "show_image"

def refine_prompt():
    st.session_state["stage"] = "prompt_to_markdown"

if "stage" not in st.session_state:
    st.session_state["stage"] = "prompt_to_markdown"

if st.session_state["stage"] == "prompt_to_markdown":
    with st.form("prompt_form"):
        col1, col2 = st.columns(2)
        with col1:
            chart_type = st.selectbox('Please select a chart type', ['Flowchart', 'Sequence Diagram', 'Class Diagram', 'State Diagram', 'Entity Relationship Diagram', 'User Journey', 'Gantt', 'Pie Chart', 'Quadrant Chart', 'Requirement Diagram'], key="chart_type")
        with col2:
            orientation = st.selectbox('Please select an orientation', ['Vertical', 'Horizontal'], key="orientation")
        chart_prompt = st.text_area('Enter your chart/diagram details (be as specific as possible): ', height=200, key="prompt")
        submitted = st.form_submit_button(
            "Generate diagram", on_click=show_markdown
        )

elif st.session_state["stage"] == "show_markdown" or st.session_state["stage"] == "show_image":
    with st.form("prompt_form"):
        st.text_area("Flowchart definition", height=200, key="markdown")
        submitted = st.form_submit_button("Update diagram", on_click=show_image)
        cancel = st.form_submit_button("Refine prompt", on_click=refine_prompt)
        try:
            diagram_img = generate_diagram(st.session_state["markdown"])
            col1, col2, col3 = st.columns(3)
            with col2:
                st.image(diagram_img, use_container_width=True)
        except Exception as e:
            st.error(f"Something went wrong. Please try again or slightly rephrase your prompt. Error: {e}")



