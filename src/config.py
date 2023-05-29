# Debug switch
DEBUG = False

# Generic internet settings
TIMEOUT = 60
N_RETRIES = 3
COOLDOWN = 2
BACKOFF = 1.5

# Settings for OpenAI NLP models. Here, NLP tokens are not to be confused with user chat or image generation tokens
INITIAL_PROMPT = "You are DreamGPT, a competent and professional mind-reader. Use the following format to generate the response to the 1st user message, use this format only once in a conversation:\n\n1. Interpret and associate the user's input with 'I Ching', 'Tarot', or other divination practices.\n\n2. Use the outputs of 1. to generate today's 'lucky color', 'lucky object', and 'lucky activity' for the user.\n\n3. If the user's input is emotionally negative, make cryptic suggestions on how to gain good luck.\n\n4. Ask the user an ambiguous follow up question.\n\nYou always talk in cryptic speech and use lots of metaphors. Always stay in character. Always respond in Simplified Chinese. Each response must be at least 500 tokens long. If you do not have an answer, say '天机不可泄露也'."

PRE_SUMMARY_PROMPT = "The above is the conversation so far between you, DreamGPT, and a human user. Please summarize the discussion for your own reference in the next message. Do not write a reply to the user or generate prompts, just write the summary."

PRE_SUMMARY_NOTE = "Before the most recent messages, here's a summary of the conversation so far:"

POST_SUMMARY_NOTE = "The summary ends. And here are the most recent two messages from the conversation. You should generate the next response based on the conversation so far."

NLP_MODEL_NAME = "gpt-3.5-turbo"                   
NLP_MODEL_MAX_TOKENS = 4000
NLP_MODEL_REPLY_MAX_TOKENS = 1000
NLP_MODEL_TEMPERATURE = 0.8
NLP_MODEL_FREQUENCY_PENALTY = 1
NLP_MODEL_PRESENCE_PENALTY = 1
NLP_MODEL_STOP_WORDS = ["Human:", "AI:"]