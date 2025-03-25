import asyncio

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
import os

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import (
    save_fabrics_to_csv,
)
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()

print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))


async def crawl_fabrics():
    """
    Main function to crawl venue data from the website.
    """
    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "fabric_crawl_session" 

    # Initialize state variables
    page_number = 1
    all_fabrics = []
    seen_names = set()

    # Start the web crawler context
    # https://docs.crawl4ai.com/api/async-webcrawler/#asyncwebcrawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            # Fetch and process data from the current page
            fabrics, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                BASE_URL,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                seen_names,
            )

            if no_results_found:
                print("No more fabrics found. Ending crawl.")
                break  # Stop crawling when "No Results Found" message appears

            if not fabrics:
                print(f"No fabrics extracted from page {page_number}.")
                break  # Stop if no venues are extracted

            # Add the venues from this page to the total list
            all_fabrics.extend(fabrics)
            page_number += 1  # Move to the next page

            # Pause between requests to be polite and avoid rate limits
            await asyncio.sleep(2)  # Adjust sleep time as needed

    # Save the collected venues to a CSV file
    if all_fabrics:
        save_fabrics_to_csv(all_fabrics, "fabrics.csv")
        print(f"Saved {len(all_fabrics)} venues to 'complete_venues.csv'.")
    else:
        print("No fabrics were found during the crawl.")

    # Display usage statistics for the LLM strategy
    llm_strategy.show_usage()


async def main():
    """
    Entry point of the script.
    """
    await crawl_fabrics()


if __name__ == "__main__":
    asyncio.run(main())
