import re

from .model_loader import generate_response


def clean_response(response):

    response = re.sub(
        r"<think>.*?</think>",
        "",
        response,
        flags=re.DOTALL
    )

    response = response.replace(
        "<think>",
        ""
    )

    response = response.replace(
        "</think>",
        ""
    )

    return response.strip()


def ask_ibcy(message, history=None):

    response = generate_response(
        message,
        history
    )

    response = clean_response(response)

    return response