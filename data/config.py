from environs import Env # pip install environs

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

VK_ACCESS_TOKEN = env("VK_ACCESS_TOKEN")
VK_GROUP_IDS = env("VK_GROUP_IDS")
VK_GROUP_COL = env("VK_GROUP_COL")

VK_APP_ID = env("VK_APP_ID")

COLUMNS_CHANNELS = {'LV': 'F'}


