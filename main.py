import streamlit as st
from components.sidebar import sidebar
from mermaid import generate_diagram
from prompt import SendChatRequest

def clear_submit():
    st.session_state["submit"] = False

# Set general streamlit config with title and header
st.set_page_config(page_title="MermaidGPT", page_icon="🧜‍♀️", layout="wide")
st.header("🧜‍♀️MermaidGPT")

# Initialize sidebar
#sidebar()

def show_markdown():
    st.session_state["stage"] = "show_markdown"
    result = SendChatRequest(st.session_state["prompt"], st.session_state["chart_type"], st.session_state["orientation"])
    st.session_state["markdown"] = result

def show_image():
    st.session_state["stage"] = "show_image"

def start_over():
    st.session_state["stage"] = "prompt_to_markdown"
    st.session_state["prompt"] = None
    st.session_state["markdown"] = None
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
            "Generate ", on_click=show_markdown
        )

elif st.session_state["stage"] == "show_markdown" or st.session_state["stage"] == "show_image":
    with st.form("prompt_form"):
        st.text_area("Flowchart definition", height=200, key="markdown")
        submitted = st.form_submit_button("Update image", on_click=show_image)
        cancel = st.form_submit_button("Start over", on_click=start_over)
        try:
            diagram_img = generate_diagram(st.session_state["markdown"])
            st.image(diagram_img, use_container_width=True)
        except:
            st.error("Something went wrong. Please try again or slightly rephrase your prompt.")



# button = st.button("Generate")
# if button:
#     if not st.session_state.get("OPENAI_API_KEY"):
#         st.error("Please configure your OpenAI API key!")
#     elif not chart_prompt:
#         st.error("Please enter a chart prompt!")
#     else:
#         st.session_state["submit"] = True

#         # Run OpenAI API call and receive md response
#         result = SendChatRequest(chart_prompt, chart_type, orientation)

#         st.text_area("Resulting markdown", result)

# button2 = st.button("Generate Image")
# if button2 and result:
#     # Display the image using streamlit
#     try:
#         diagram_img = generate_diagram(result)
#         st.image(diagram_img, use_container_width=True)
#     except:
#         st.error("Something went wrong. Please try again or slightly rephrase your prompt.")
#         #st.write(f'Resulting markdown: {result}')
