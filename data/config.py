from environs import Env  # pip install environs

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

VK_ACCESS_TOKEN = env("VK_ACCESS_TOKEN")
VK_GROUP_IDS = env("VK_GROUP_IDS")
VK_GROUP_COL = env("VK_GROUP_COL")

VK_APP_ID = env("VK_APP_ID")

YOUTUBE_CHANNELS = env("YOUTUBE_CHANNELS")
COLUMNS_CHANNELS = env("COLUMNS_CHANNELS")

TG_ACCESS_TOKEN = env("TG_ACCESS_TOKEN")
TG_CHANNEL_IDS = env("TG_CHANNEL_IDS")
TG_CHANNEL_COL = env("TG_CHANNEL_COL")

OK_ACCESS_TOKEN = env("OK_ACCESS_TOKEN")
OK_APPLICATION_KEY=env("OK_APPLICATION_KEY")
OK_APPLICATION_SECRET_KEY=env("OK_APPLICATION_SECRET_KEY")
OK_GROUP_IDS = env("OK_GROUP_IDS")
OK_GROUP_COL = env("OK_GROUP_COL")
