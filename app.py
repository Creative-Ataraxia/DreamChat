import streamlit as st
import time

from prompt_engineering import engineer_prompt, engineer_followup_prompt
from gpt import generate_gpt_response

def clear_chat_history():
    st.session_state.chat_history = "欢迎来到泰裤辣解梦中心!\n\n"

st.set_page_config(
    page_title="泰裤辣解梦",
    page_icon="🧙",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get help': 'https://www.bing.com/',
        'Report a bug': "https://www.bing.com/",
        'About': "# 这里是泰裤辣**解梦**中心!"
    }
)

st.title("泰裤辣解梦:crystal_ball:")
st.text("")
st.write("一起聊聊你昨晚的梦吧！")
st.text("")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = '欢迎来到泰裤辣解梦中心!\n\n'

with st.form(key='my_form'):
    user_input = st.text_input('我昨晚梦到了:', key='dream_input')
    submit_button = st.form_submit_button('解梦！')

if submit_button:
    if st.session_state.chat_history == '欢迎来到泰裤辣解梦中心!\n\n':
        prompt = engineer_prompt(user_input)
    else:
        prompt = engineer_followup_prompt(user_input)

    # Use a spinner while fetching response from GPT-3 API
    with st.spinner('Generating response...'):
        gpt_response = generate_gpt_response(prompt, max_tokens=300)

    if gpt_response is None:
        st.error("App在梦境里走丢了。。。")
    else:
        st.session_state.chat_history += f"您梦到了: {user_input}\n\n{gpt_response}\n\n\n"
        st.write(gpt_response)

st.text_area("解梦记录", st.session_state.chat_history, disabled=True, height=350, max_chars=None, key='chat_history')

st.text("")

if st.button("清除记录", key="clear_button", on_click=clear_chat_history):
    pass

