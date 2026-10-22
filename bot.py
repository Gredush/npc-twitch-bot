from twitchio.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_NICK = os.getenv("BOT_NICK")
CHANNEL = os.getenv("CHANNEL_NAME")


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[CHANNEL]
        )

    async def event_ready(self):
        print(f"{BOT_NICK} connected!")
        print(f"Watching: {CHANNEL}")

    async def event_message(self, message):

        if message.echo:
            return

        print(f"{message.author.name}: {message.content}")

        if "kalimera" in message.content.lower():
            await message.channel.send(
                f"Kalimera @{message.author.name}!"
            )

        await self.handle_commands(message)


bot = Bot()
bot.run()
