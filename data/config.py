from environs import Env # pip install environs

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

VK_GROUP_IDS = env.dict("VK_GROUP_IDS")
VK_APP_ID = env("VK_APP_ID")

COLUMNS_CHANNELS = {'LV': 'F'}


