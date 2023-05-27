def engineer_prompt(user_input):
    """
    Function to engineer a prompt suitable for the GPT-3 API from user input.

    Args:
        user_input (str): The user's input.

    Returns:
        str: The engineered prompt.
    """

    # Add a prefix to the user input
    prompt = f"I dreamt about {user_input} last night, what does it mean?"

    return prompt

def engineer_followup_prompt(user_input):
    """
    Takes user input and engineers a follow-up prompt for the GPT-3 model.
    This function is used for all user inputs after the first in a conversation.
    """

    prompt = user_input
    return prompt
