import re


def clean_content(content: str) -> str:
    """
    Process the input markdown content and return the cleaned output.

    Args:
        content (str): The input content to process.

    Returns:
        str: The cleaned and processed output content.
    """
    # Normalize line endings and remove BOM characters
    content = content.replace("\r\n", "\n").replace("\r", "\n").strip()

    # Remove image links, standalone dates, and dots at the beginning
    content = re.sub(
        r"^(?:!\[.*?\]\(.*?\)|\d{1,2}\s*\w+\s*\d{4}|·)+\s*",
        "",
        content,
        flags=re.MULTILINE,
    )

    # Remove blockquotes
    content = re.sub(r"(^>+\s*|\n>+\s*)", "", content, flags=re.MULTILINE)

    # Handle headers (both styles)
    content = re.sub(r"^#+\s*(.*?)$", r"\1", content, flags=re.MULTILINE)
    content = re.sub(r"^(.*?)\n[=-]+\n", r"\1\n", content, flags=re.MULTILINE)

    # Handle lists
    content = re.sub(r"^\s*[-*+]\s+", "\t• ", content, flags=re.MULTILINE)
    content = re.sub(r"^\s*\d+\.\s+", "\t• ", content, flags=re.MULTILINE)

    # Remove bold and italic formatting
    content = re.sub(r"\*\*\*(.*?)\*\*\*", r"\1", content)  # Bold + italic
    content = re.sub(r"\*\*(.*?)\*\*", r"\1", content)  # Bold
    content = re.sub(r"\*(.*?)\*", r"\1", content)  # Italic
    content = re.sub(r"_{3}(.*?)_{3}", r"\1", content)  # Bold + italic
    content = re.sub(r"_{2}(.*?)_{2}", r"\1", content)  # Bold
    content = re.sub(r"_(.*?)_", r"\1", content)  # Italic

    # Remove links and images
    content = re.sub(r"!\[.*?\]\(.*?\)|\[(.*?)\]\(.*?\)", r"\1", content)

    # Remove HTML tags
    content = re.sub(r"<(http[^>]+?)>", r"\1", content, flags=re.DOTALL)

    # Remove horizontal rules
    content = re.sub(r"^[-*_]{3,}\s*$", "", content, flags=re.MULTILINE)

    # Remove footnotes
    content = re.sub(r"\[\^.+?\](?:\: .*?$)?", "", content, flags=re.MULTILINE)

    # Remove task lists
    content = re.sub(r"^\s*-\s*\[[xX ]\]\s*", "\t• ", content, flags=re.MULTILINE)

    # Remove large gaps
    content = re.sub(r"\n{2,}", "\n", content)

    # Add proper new lines between sections
    content = re.sub(r"(\n)([A-Z][^\n]*\n)", r"\1\n\2", content)
    content = re.sub(r"(\n)(\t• )", r"\1\n\2", content)

    # Clean up whitespace
    content = re.sub(r"[ \t]+$", "", content, flags=re.MULTILINE)
    content = re.sub(r"^[ \t]+", "", content, flags=re.MULTILINE)
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = content.strip()

    # Return the cleaned content
    return content
