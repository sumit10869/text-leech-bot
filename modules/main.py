import os
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.video.tools.drawing import color_gradient

# Replace with your own API_ID, API_HASH, and BOT_TOKEN
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'

bot = Client(
    "text_to_video_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! Send me a text file, and I'll convert it to a video.")

@bot.on_message(filters.document)
async def text_to_video(client, message):
    document = message.document
    if not document.file_name.endswith(".txt"):
        await message.reply_text("Please send a .txt file.")
        return
    
    file_path = await message.download()
    with open(file_path, "r") as file:
        text_content = file.read()

    # Create a video clip from the text
    txt_clip = TextClip(text_content, fontsize=24, color='white', size=(640, 480), bg_color='black')
    txt_clip = txt_clip.set_duration(10)  # Set the duration of the video

    # Save the video
    video_path = file_path.replace(".txt", ".mp4")
    txt_clip.write_videofile(video_path, fps=24)

    # Send the video back to the user
    await message.reply_video(video_path, caption="Here's your video!")

    # Clean up files
    os.remove(file_path)
    os.remove(video_path)

bot.run()
