import streamlit as st
import openai

def generate_gpt_response(gpt_input, max_tokens):
    """
    Function to call the ChatGPT API.

    Args:
        gpt_input (str): The prompt to send to the API.
        max_tokens (int): The maximum length of the response.

    Returns:
        str: The model's response.
    """

    # Set your OpenAI API Key; streamlit's doc: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    try:
        completion = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			max_tokens=max_tokens,
			temperature=0.5,
			messages=[
                {"role": "system", "content": "You are DreamGPT, a compotent and professional dream interpreter, you use metaphors to interpret dream stories.\nRequirements:\n- Always ask the user follow-up questions after each dream interpretation.\n- Respond in cryptic and mysterious tones.\n- Always respond in Simplified Chinese\n- Always stays in character."},
				{"role": "user", "content": gpt_input},
			]
        )
        gpt_response = completion.choices[0].message['content'].strip()
        return f"梦神说: {gpt_response}"
    
    except openai.error.APIError as e:
    #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        return f"服务器开小差了，请稍后再试.\n报错: {e}"
    
    except openai.error.APIConnectionError as e:
    #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        return f"服务器开小差了，请稍后再试.\n报错: {e}"
    
    except openai.error.RateLimitError as e:
    #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        return f"服务器开小差了，请稍后再试.\n报错: {e}"