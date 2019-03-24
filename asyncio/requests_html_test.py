from pprint import pprint

import asyncio

from timeit import default_timer
from concurrent.futures import ThreadPoolExecutor

from requests_html import AsyncHTMLSession, HTML

async def fetch(session, url):
    r = await session.get(url)
    await r.html.arender()
    return r.html.raw_html

def parseWebpage(page):
    print(page)

async def get_data_asynchronous():  
    urls = [
        'http://www.fpb.pt/fpb2014/!site.go?s=1&show=jog&id=258215'
    ]  

    with ThreadPoolExecutor(max_workers=20) as executor:
        with AsyncHTMLSession() as session:
            # Set any session parameters here before calling `fetch` 

            # Initialize the event loop        
            loop = asyncio.get_event_loop()

            # Use list comprehension to create a list of
            # tasks to complete. The executor will run the `fetch`
            # function for each url in the urlslist
            tasks = [
                await loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, url) # Allows us to pass in multiple arguments to `fetch`
                )
                for url in urls
            ]

            # Initializes the tasks to run and awaits their results
            for response in await asyncio.gather(*tasks):
                parseWebpage(response)

def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

main()
