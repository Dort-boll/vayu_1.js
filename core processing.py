# Python script (robust_data_processing.py)

import aiohttp
import asyncio
import json
import multiprocessing
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                logging.error(f"Failed to fetch data from {url}. Status code: {response.status}")
                return None
    except Exception as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None

def extract_information(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        tag_counts = {}
        for tag in soup.find_all():
            tag_name = tag.name
            tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
        return tag_counts
    except Exception as e:
        logging.error("Error extracting information:", e)
        return {}

def process_data(url, html_content):
    try:
        extracted_info = extract_information(html_content)
        processed_data = {url: extracted_info}
        return processed_data
    except Exception as e:
        logging.error("Error processing data:", e)
        return {}

def send_data_for_execution(transformed_data):
    try:
        serialized_data = json.dumps(transformed_data)
        temp_file_path = 'transformed_data.json'
        with open(temp_file_path, 'w') as file:
            file.write(serialized_data)
        logging.info("Transformed data sent for execution.")
    except Exception as e:
        logging.error("Error sending data for execution:", e)

async def main():
    urls = [
        "https://storage.googleapis.com/openimages/web/index.html",
        "https://www.dbpedia.org/",
        # Add more URLs here if needed
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        html_contents = await asyncio.gather(*tasks)

        with multiprocessing.Pool() as pool:
            processed_results = pool.starmap(process_data, zip(urls, html_contents))

        transformed_data = {}
        for result in processed_results:
            transformed_data.update(result)

        send_data_for_execution(transformed_data)

if __name__ == "__main__":
    asyncio.run(main())
