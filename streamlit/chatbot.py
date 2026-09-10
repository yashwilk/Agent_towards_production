"""OpenAI chat completion wrapper for the Streamlit app."""

import openai

import config

client = openai.OpenAI(api_key=config.OPENAI_API_KEY)


def generate_response(user_prompt: str) -> str:
    """
    Sends the user prompt to OpenAI and returns the AI's response.

    Parameters
    ----------
    user_prompt : str
        The input message from the user.

    Returns
    -------
    str
        The AI-generated response as plain text.
    """
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.choices[0].message.content
