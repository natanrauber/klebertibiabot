from datetime import datetime


def dateTime() -> str:
    """
    Returns the current date and time as a string in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        str: A string representation of the current date and time.

    Note:
        Documented using Google style docstrings by ChatGPT, an OpenAI language model.
    """
    return str(datetime.now())[0:19]
