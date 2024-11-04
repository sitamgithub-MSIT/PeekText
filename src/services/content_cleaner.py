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

    # Extract and preserve the title
    title_match = re.search(
        r"^(?:Title:)\s*(.*?)(?:\n|$)", content, flags=re.IGNORECASE
    )
    title = title_match[1].strip() if title_match else ""

    # Remove metadata header while preserving title
    content = re.sub(
        r"(?:^|\n)Title:\s*.*?\n+URL Source:\s*.*?\n+(?:Published Time:\s*.*?\n+)?(?:Markdown Content:\s*\n+)?",
        f"{title}\n\n",
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )

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
    content = re.sub(r"^#+\s*(.*?)$", r"\1", content, flags=re.MULTILINE)  # ATX headers
    content = re.sub(
        r"^(.*?)\n[=-]+\n", r"\1\n", content, flags=re.MULTILINE
    )  # Setext headers

    # Handle lists
    content = re.sub(
        r"^\s*[-*+]\s+", "\t• ", content, flags=re.MULTILINE
    )  # Unordered lists
    content = re.sub(
        r"^\s*\d+\.\s+", "\t• ", content, flags=re.MULTILINE
    )  # Ordered lists

    # Remove bold and italic formatting
    content = re.sub(r"\*\*\*(.*?)\*\*\*", r"\1", content)  # Bold + italic
    content = re.sub(r"\*\*(.*?)\*\*", r"\1", content)  # Bold
    content = re.sub(r"\*(.*?)\*", r"\1", content)  # Italic
    content = re.sub(r"_{3}(.*?)_{3}", r"\1", content)  # Bold + italic
    content = re.sub(r"_{2}(.*?)_{2}", r"\1", content)  # Bold
    content = re.sub(r"_(.*?)_", r"\1", content)  # Italic

    # Remove links and images
    content = re.sub(
        r"!\[.*?\]\(.*?\)|\[(.*?)\]\(.*?\)", r"\1", content
    )  # Combine image and link removal

    # Remove HTML tags
    content = re.sub(r"<[^>]+?>", "", content, flags=re.DOTALL)

    # Remove horizontal rules
    content = re.sub(r"^[-*_]{3,}\s*$", "", content, flags=re.MULTILINE)

    # Remove footnotes
    content = re.sub(r"\[\^.+?\](?:\: .*?$)?", "", content, flags=re.MULTILINE)

    # Remove task lists
    content = re.sub(r"^\s*-\s*\[[xX ]\]\s*", "\t• ", content, flags=re.MULTILINE)

    # Remove publication, time, follow, like, share, sign-in, sign-out, and []() patterns
    content = re.sub(
        r"\b(?:publication|time|follow|like|share|sign-in|sign-out)\b",
        "",
        content,
        flags=re.IGNORECASE,
    )
    content = re.sub(r"\[\]\(.*?\)", "", content)

    # Remove author and metadata lines
    content = re.sub(
        r"^\s*[\w\s]+\n·\nPublished in\n[\w\s-]+\n·\n\d+ min read\n·\n[\w\s,]+\n\d+\nListen\n",
        "",
        content,
        flags=re.MULTILINE,
    )

    # Ensure no extra lines within code blocks
    content = re.sub(
        r"(```(?:\w*\n)?)\n+([^`]*?)\n+(```)", r"\1\2\3", content, flags=re.DOTALL
    )

    # Remove large gaps
    content = re.sub(
        r"\n{2,}", "\n", content
    )  # Replace multiple newlines with a single newline

    # Add proper new lines between sections
    content = re.sub(
        r"(\n)([A-Z][^\n]*\n)", r"\1\n\2", content
    )  # Add new line before section headers
    content = re.sub(
        r"(\n)(\t• )", r"\1\n\2", content
    )  # Add new line before list items

    # Clean up whitespace
    content = re.sub(
        r"[ \t]+$", "", content, flags=re.MULTILINE
    )  # Remove trailing whitespace
    content = re.sub(
        r"^[ \t]+", "", content, flags=re.MULTILINE
    )  # Remove leading whitespace
    content = re.sub(r"\n{3,}", "\n\n", content)  # Ensure max of two newlines
    content = content.strip()

    # Return the cleaned content
    return content
