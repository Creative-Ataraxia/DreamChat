###########
# Imports #
###########

import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

# import modules
from prompt_engineering import engineer_prompt, engineer_followup_prompt
from gpt import generate_gpt_response


#############
# Functions #
#############

## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("请输入: ", "", help="请简单描述您的梦境", key="input")
    return input_text


####################
# State Management #
####################

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["欢迎来到泰裤辣解梦中心!"]

if 'human_input' not in st.session_state:
    st.session_state['human_input'] = []


################
# Streamlit UI #
################

# Page layout settings
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

# Sidebar UI
with st.sidebar:
    st.title('泰裤辣解梦:crystal_ball:')
    st.markdown('''
    ## 一起聊聊你昨晚的梦吧！
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Creative_Ataraxia](<https://github.com/Creative-Ataraxia?tab=repositories>)')

# App general layout
response_container = st.container()
colored_header(label='', description='', color_name='blue-30')
add_vertical_space(3)
input_container = st.container()

# Applying the user input box
with input_container:
    user_input = get_text()

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        if st.session_state['generated'] == ["欢迎来到泰裤辣解梦中心!"]:
            prompt = engineer_prompt(user_input)
        else:
            prompt = engineer_followup_prompt(user_input)

        st.session_state.human_input.append(user_input)
        
        # Use a spinner while fetching response from GPT-3 API
        with st.spinner('接收信号中...请耐心等待...'):
            gpt_response = generate_gpt_response(prompt, max_tokens=300)

        if gpt_response is None:
            st.error("App在梦境里走丢了。。。")
        else:    
            st.session_state.generated.append(gpt_response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            if i < len(st.session_state['human_input']):
                message(st.session_state['generated'][i], key=str(i))
                message(st.session_state['human_input'][i], is_user=True, key=str(i) + '_user')
            else:
                message(st.session_state['generated'][i], key=str(i))
