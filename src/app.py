###########
# Imports #
###########

import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import openai

import os
import base64
import asyncio
import traceback
from PIL import Image
from transformers import AutoTokenizer

# import modules
from config import *
from utils import *


#############
# Functions #
#############

@st.cache_data(show_spinner=False)
def get_local_img(file_path: str) -> str:
    # Load a byte image and return its base64 encoded string
    return base64.b64encode(open(file_path, "rb").read()).decode("utf-8")

@st.cache_data(show_spinner=False)
def get_favicon(file_path: str):
    # Load a byte image and return its favicon
    return Image.open(file_path)

@st.cache_data(show_spinner=False)
def get_tokenizer():
    return AutoTokenizer.from_pretrained("gpt2", low_cpu_mem_usage=True)

@st.cache_data(show_spinner=False)
def get_css() -> str:
    # Read CSS code from style.css file
    with open(os.path.join(ROOT_DIR, "src", "style.css"), "r") as f:
        return f"<style>{f.read()}</style>"

def get_chat_message(contents: str = "", align: str = "left") -> str:
    # Formats the message in an chat fashion (user right, reply left)
    div_class = "AI-line"
    color = "rgb(240, 242, 246)"
    file_path = os.path.join(ROOT_DIR, "src", "assets", "AI_icon.png")
    src = f"data:image/gif;base64,{get_local_img(file_path)}"
    if align == "right":
        div_class = "human-line"
        color = "rgb(165, 239, 127)"
        if "USER" in st.session_state:
            src = st.session_state.USER.avatar_url
        else:
            file_path = os.path.join(ROOT_DIR, "src", "assets", "user_icon.png")
            src = f"data:image/gif;base64,{get_local_img(file_path)}"
    icon_code = f"<img class='chat-icon' src='{src}' width=32 height=32 alt='avatar'>"
    formatted_contents = f"""
    <div class="{div_class}">
        {icon_code}
        <div class="chat-bubble" style="background: {color};">
        &#8203;{contents}
        </div>
    </div>
    """
    return formatted_contents

async def main(human_prompt: str) -> dict:
    res = {'status': 0, 'message': "Success"}
    try:
        # Strip the prompt of any potentially harmful html/js injections
        human_prompt = human_prompt.replace("<", "&lt;").replace(">", "&gt;")

        # Update both chat log and the model memory
        st.session_state.Log.append(f"Human: {human_prompt}")
        st.session_state.Memory.append({'role': "user", 'content': human_prompt})

        # Clear the input box after human_prompt is used
        prompt_box.empty()

        with chat_box:
            # Write the latest human message first
            line = st.session_state.Log[-1]
            contents = line.split("Human: ")[1]
            st.markdown(get_chat_message(contents, align="right"), unsafe_allow_html=True)

            reply_box = st.empty()
            reply_box.markdown(get_chat_message(), unsafe_allow_html=True)

            # This is one of those small three-dot animations to indicate the bot is "writing"
            writing_animation = st.empty()
            file_path = os.path.join(ROOT_DIR, "src", "assets", "loading.gif")
            writing_animation.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;<img src='data:image/gif;base64,{get_local_img(file_path)}' width=30 height=10>", unsafe_allow_html=True)

            # Step 1: Generate the AI-aided image prompt using ChatGPT API
            prompt_res = await generate_prompt_from_memory_async(TOKENIZER, st.session_state.Memory)

            if DEBUG:
                with st.sidebar:
                    st.write("prompt_result:")
                    st.json(prompt_res, expanded=False)

            if prompt_res['status'] != 0:
                res['status'] = prompt_res['status']
                res['message'] = prompt_res['message']
                return res

            # Call the OpenAI ChatGPT API
            chatbot_response = await get_chatbot_reply_async(prompt_res['data']['messages'])

            if DEBUG:
                with st.sidebar:
                    st.write("chatbot_response:")
                    st.json({'str': chatbot_response}, expanded=False)

            if "Description:" in chatbot_response:
                reply_text, image_prompt = chatbot_response.split("Description:")
            else:
                reply_text = chatbot_response

            if reply_text.startswith("梦神说: "):
                reply_text = reply_text.split("梦神说: ", 1)[1]


            # Render the reply as chat reply
            message = f"{reply_text}"
    
            if DEBUG:
                message += f"""<br>{image_prompt}"""
            reply_box.markdown(get_chat_message(message), unsafe_allow_html=True)

            # Clear the writing animation
            writing_animation.empty()

            # Update the chat log and the model memory
            st.session_state.Log.append(f"AI: {message}")
            st.session_state.Memory.append({'role': "assistant", 'content': reply_text})

    except:
        res['status'] = 2
        res['message'] = traceback.format_exc()

    return res


#####################
# Environment setup #
#####################

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

errors = []

# Set your OpenAI API Key; streamlit's doc: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
openai.api_key = st.secrets["OPENAI_API_KEY"]

if len(errors) > 0:
    st.error("\n".join(errors))
    st.stop()


######################
# Initialize the App #
######################

# Icons
favicon = get_favicon(os.path.join(ROOT_DIR, "src", "assets", "AI_icon.png"))

# Page layout settings
st.set_page_config(
    page_title="泰裤辣解梦",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get help': 'https://www.bing.com/',
        'Report a bug': "https://www.bing.com/",
        'About': "# 这里是泰裤辣**解梦**中心!"
    }
)

# Get options from URL
query_params = st.experimental_get_query_params()
if "debug" in query_params and query_params["debug"][0].lower() == "true":
    st.session_state.DEBUG = True

if "DEBUG" in st.session_state and st.session_state.DEBUG:
    DEBUG = True

# Init Tokenizer
with st.spinner("准备中..."):
    TOKENIZER = get_tokenizer()  # First time after deployment takes a few seconds


################
# Streamlit UI #
################

# Define main layout
st.title(":cat::crystal_ball:")
st.subheader("欢迎来到招财猫猫运势中心！")
st.subheader("")
chat_box = st.container()
add_vertical_space(2)
prompt_box = st.empty()
add_vertical_space(2)
footer = st.container()

with footer:
    # st.markdown("""
    # <div align=right><small>
    # Page views: <img src="https://www.cutercounter.com/hits.php?id=hvxndaff&nd=5&style=1" border="0" alt="hit counter"><br>
    # Unique visitors: <img src="https://www.cutercounter.com/hits.php?id=hxndkqx&nd=5&style=1" border="0" alt="website counter"><br>
    # GitHub <a href="https://github.com/tipani86/CatGDP"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/tipani86/CatGDP?style=social"></a>
    # </small></div>
    # """, unsafe_allow_html=True)
    # add_vertical_space(2)
    st.write('Made with ❤️ by [Creative_Ataraxia](<https://github.com/Creative-Ataraxia?tab=repositories>)')

if DEBUG:
    with st.sidebar:
        st.subheader("Debug area")

st.markdown(get_css(), unsafe_allow_html=True)


####################
# State Management #
####################

if "Memory" not in st.session_state:
    st.session_state.Memory = [{'role': "system", 'content': INITIAL_PROMPT}]
    st.session_state.Log = [INITIAL_PROMPT]

# Render chat history so far
with chat_box:
    for line in st.session_state.Log[1:]:
        # For AI response
        if line.startswith("AI: "):
            contents = line.split("AI: ")[1]
            st.markdown(get_chat_message(contents), unsafe_allow_html=True)

        # For human prompts
        if line.startswith("Human: "):
            contents = line.split("Human: ")[1]
            st.markdown(get_chat_message(contents, align="right"), unsafe_allow_html=True)

# Define an input box for human prompts
with prompt_box:
    human_prompt = st.text_input("问:cat::cat::", value="", help="请简单描述您的梦境", key=f"text_input_{len(st.session_state.Log)}")

# Gate the subsequent chatbot response to only when the user has entered a prompt
if len(human_prompt) > 0:
    run_res = asyncio.run(main(human_prompt))
    # if main() return with success status:
    if run_res['status'] == 0 and not DEBUG:
        # rerun to react to updates
        st.experimental_rerun()
    else:
        if run_res['status'] != 0:
            st.error(run_res['message'])
        with prompt_box:
            if st.button("显示文字输入框"):
                st.experimental_rerun()
