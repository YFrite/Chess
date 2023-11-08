import asyncio

from src.Game import Game

if __name__ == "__main__":
    asyncio.run(Game(screen_size=(1280, 720)).start())
