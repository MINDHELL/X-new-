import asyncio
from pyrogram import Client, filters
from scraper import get_tweets, download_media
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("twitter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command to download all posts from a Twitter username
@app.on_message(filters.command("download"))
async def download_tweets(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply("Usage: `/download username`")
        return
    
    username = args[1].strip()
    await message.reply(f"🔍 Fetching posts from **{username}**...")

    tweets = await get_tweets(username)
    if not tweets:
        await message.reply("❌ No posts found or unable to scrape.")
        return

    total_tweets = len(tweets)
    sent_count = 0

    for i, tweet in enumerate(tweets):
        media_files = await download_media(tweet["media_urls"], username)
        caption = f"📝 {tweet['text']}\n🔗 [View on Twitter]({tweet['url']})"

        await message.reply_document(
            document=media_files[0], caption=caption
        ) if media_files else await message.reply_text(caption)
        
        sent_count += 1
        await asyncio.sleep(1)

    await message.reply(f"✅ Finished downloading. {sent_count}/{total_tweets} posts sent.")

app.run()
