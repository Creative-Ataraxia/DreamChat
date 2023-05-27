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
    openai.api_key = st.secrets["openai_credentials"]["API_KEY"]
    # openai.api_key = "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"

    try:
        completion = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			max_tokens=max_tokens,
			temperature=1,
			messages=[
				{"role": "user", "content": gpt_input},
			]
        )
        gpt_response = completion.choices[0].message['content'].strip()
        return f"梦神说: {gpt_response}"

    except Exception as e:
        print(f"Error fetching response from API: {e}")
        return "服务器开小差了，请稍后再试."
