def engineer_prompt(user_input):
    """
    Function to engineer a prompt suitable for the GPT-3 API from user input.

    Args:
        user_input (str): The user's input.

    Returns:
        str: The engineered prompt.
    """

    # Add a prefix to the user input
    prompt = f"Act as a compotent and professional psychiatrist, Use metaphors to interpret the following dream scenario: '{user_input}'. Then ask the user a follow-up question. Respond in cryptic and mysterious tones, always respond in Simplified Chinese."

    return prompt

def engineer_followup_prompt(user_input):
    """
    Takes user input and engineers a follow-up prompt for the GPT-3 model.
    This function is used for all user inputs after the first in a conversation.
    """

    prompt = f"{user_input}. Consider the previous chat contexts."
    return prompt
