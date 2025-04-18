from dotenv import dotenv_values

from config.settings import *  # noqa: F401,F403

MOCK_EXTERNAL_API = dotenv_values(".env.test")["MOCK_EXTERNAL_API"]
