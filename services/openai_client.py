import logging
from http.client import responses
from openai import AsyncOpenAI
from pyexpat.errors import messages
from config import CHATGPT_TOKEN

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=CHATGPT_TOKEN)


async def get_random_fact():
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = [
                {
                    "role": "system",
                    "content": "You'r a assistant who tell interesting facts! Answer in Russian"
                },
                {
                    "role": "user",
                    "content": "Tell a random interesting fact. The fact should be interesting, cognitive and impressive!"
                }
            ],
            max_tokens = 200,
            temperature= 0.8
        )

        fact = response.choices[0].message.content.strip()
        # logger.info(f"{fact}")
        logger.info("Fact was successfully returned")
        return fact

    except Exception as e:
        logger.error(f"Error while trying to get fact: {e}")
        return "Oops...  Something went wrong. Try again later!"