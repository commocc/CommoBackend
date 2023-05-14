import logging
import os, sys

sys.path.append('../')
sys.path.append('.')

from dotenv import load_dotenv

from config.envs import envs
from bots.clients.openai_helper import OpenAIHelper
from bots.clients.telegram_bot import ChatGPT3TelegramBot


def main():
    # Read .env file
    load_dotenv()

    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )


    # Setup configurations
    openai_config = {
        'api_key': envs.OPENAI_API_KEY,
        'show_usage': envs.SHOW_USAGE,
        'proxy': envs.PROXY_URL,

        # 'gpt-3.5-turbo' or 'gpt-3.5-turbo-0301'
        'model': envs.OPENAI_MODEL,

        # A system message that sets the tone and controls the behavior of the assistant.
        'assistant_prompt': 'You are a helpful assistant.',

        # Number between 0 and 2. Higher values like 0.8 will make the output more random,
        # while lower values like 0.2 will make it more focused and deterministic.
        'temperature': 1,

        # How many chat completion choices to generate for each input message.
        'n_choices': 1,

        # The maximum number of tokens allowed for the generated answer
        'max_tokens': 1200,

        # Number between -2.0 and 2.0. Positive values penalize new tokens based on whether
        # they appear in the text so far, increasing the model's likelihood to talk about new topics.
        'presence_penalty': 0,

        # Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing
        # frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
        'frequency_penalty': 0,

        # The DALL·E generated image size
        'image_size': '512x512'
    }

    telegram_config = {
        'token': envs.TELEGRAM_BOT_TOKEN,
        'allowed_user_ids': envs.get_allowed_telegram_user_ids(),
        'proxy': envs.PROXY_URL
    }

    # Setup and run ChatGPT and Telegram bot
    openai_helper = OpenAIHelper(config=openai_config)
    telegram_bot = ChatGPT3TelegramBot(config=telegram_config, openai=openai_helper)
    telegram_bot.run()


if __name__ == '__main__':
    main()
