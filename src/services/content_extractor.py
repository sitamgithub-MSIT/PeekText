import re


def extract_text(content: str) -> str:
    """
    Extracts and processes text content from a given string.

    Args:
        content (str): The input text content to be processed.

    Returns:
        str: The cleaned and processed text content.
    """
    # Normalize line endings to \n and remove any BOM characters
    content = content.replace("\r\n", "\n").replace("\r", "\n").strip()

    # Extract the title with more flexible pattern matching
    title_match = re.search(r"(?:^|\n)Title:\s*(.*?)(?:\n|$)", content)
    title = title_match.group(1).strip() if title_match else ""

    # Using non-greedy matching and accounting for variable whitespace
    content = re.sub(
        r"(?:^|\n)Title:\s*.*?\n+URL Source:\s*.*?\n+(?:Published Time:\s*.*?\n+)?(?:Markdown Content:\s*\n+)?",
        f"{title}\n\n",
        content,
        flags=re.DOTALL,
    )

    # Convert headers to uppercase and remove Markdown formatting
    content = re.sub(
        r"^(#+\s*)(.*?)$",
        lambda match: match.group(2).upper(),
        content,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r"^(.*?)\n[-=]+\n",
        lambda match: match.group(1).upper() + "\n",
        content,
        flags=re.MULTILINE,
    )

    # Convert bold and italic text to uppercase without Markdown formatting
    content = re.sub(r"\*\*(.*?)\*\*", lambda match: match.group(1).upper(), content)
    content = re.sub(r"\*(.*?)\*", lambda match: match.group(1).upper(), content)

    # Convert lists to plain text with indentation and bullet points
    content = re.sub(
        r"^\s*\*\s*(.*?)$",
        lambda match: "\t* " + match.group(1).upper(),
        content,
        flags=re.MULTILINE,
    )

    # Remove Markdown link formatting, keeping only the text
    content = re.sub(r"\[(.*?)\]\(.*?\)", lambda match: match.group(1).upper(), content)

    # Remove image tags, links, and captions
    content = re.sub(r"!\[.*?\]\(.*?\)", "", content)
    content = re.sub(r"!IMAGE \d+", "", content)
    content = re.sub(r"Demo Image-\d+", "", content)

    # Replace escaped numbers in lists (e.g., `4\.`) with plain numbers
    content = re.sub(r"(\d)\\\.", r"\1.", content)

    # Clean up excessive whitespace and normalize spacing
    content = re.sub(r"\n{3,}", "\n\n", content)  # Limit to max double newlines
    content = re.sub(r"[ \t]+\n", "\n", content)  # Remove trailing whitespace
    content = content.strip()  # Remove leading/trailing whitespace

    # Return the cleaned content
    return content
