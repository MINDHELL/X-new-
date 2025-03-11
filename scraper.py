import os
import requests
from bs4 import BeautifulSoup
import aiohttp
import aiofiles

async def get_tweets(username):
    url = f"https://nitter.net/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return []
            
            soup = BeautifulSoup(await response.text(), "html.parser")
            tweets = []

            for tweet in soup.select(".timeline-item"):
                text = tweet.select_one(".tweet-content").text.strip()
                media_urls = [img["src"] for img in tweet.select(".tweet-media img")]
                tweet_url = "https://nitter.net" + tweet.select_one("a.tweet-link")["href"]
                
                tweets.append({"text": text, "media_urls": media_urls, "url": tweet_url})
    
    return tweets

async def download_media(urls, username):
    media_dir = f"downloads/{username}"
    os.makedirs(media_dir, exist_ok=True)
    downloaded_files = []

    async with aiohttp.ClientSession() as session:
        for url in urls:
            filename = os.path.join(media_dir, os.path.basename(url))
            async with session.get(url) as response:
                if response.status == 200:
                    async with aiofiles.open(filename, "wb") as f:
                        await f.write(await response.read())
                    downloaded_files.append(filename)

    return downloaded_files
