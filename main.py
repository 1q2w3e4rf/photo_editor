import json
from maim import NewYearBot

if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)
    
    bot_token = config["bot_token"]
    if not bot_token:
        raise ValueError("Bot token not found in config.json")

    bot = NewYearBot(bot_token)
    bot.run()