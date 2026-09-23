def format_percentage(value):

    return f"{value * 100:.2f}%"


def truncate_text(
    text,
    length=500
):

    if len(text) <= length:

        return text

    return text[:length] + "..."