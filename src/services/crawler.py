import sys
import nest_asyncio

nest_asyncio.apply()
from crawl4ai import AsyncWebCrawler

# Local imports
from src.logger import logging
from src.exception import CustomExceptionHandling


async def extract_markdown(url: str):
    """
    Fetch data from a given URL using the AsyncWebCrawler and return the fit markdown content.

    Args:
        - url (str): The URL to fetch data from.

    Returns:
        str: The response content as a fit markdown content.
    """
    try:
        logging.info(f"Fetching data from URL: {url}")

        # Initialize the AsyncWebCrawler
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(
                url=url,
                bypass_cache=False,
                word_count_threshold=10,
                excluded_tags=[
                    "form",
                    "nav",
                    "footer",
                    "aside",
                    "header",
                    "script",
                    "style",
                    "iframe",
                    "noscript",
                    "banner",
                    "advertisement",
                    "cookie-notice",
                ],
                remove_overlay_elements=True,
                exclude_social_media_links=True,
                exclude_external_images=True,
                exclude_domains=["medium.com"],
                exclude_social_media_domains=[
                    "facebook.com",
                    "linkedin.com",
                    "twitter.com",
                    "instagram.com",
                    "pinterest.com",
                    "reddit.com",
                    "tumblr.com",
                    "tiktok.com",
                ],
                magic=True,
            )

            # Check for non-successful status codes
            if not result.success:
                error_message = f"Failed to fetch data: Status {result.status_code}"
                logging.error(error_message)
                raise CustomExceptionHandling(error_message, sys)

            logging.info(f"Received response with status code: {result.status_code}")

            # Return the cleaned markdown content
            return result.fit_markdown

    # Handle exceptions that may occur during crawling
    except Exception as e:
        # Custom exception handling
        raise CustomExceptionHandling(e, sys) from e
