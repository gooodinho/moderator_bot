from environs import Env

env = Env()
env.read_env()

PER_PAGE = env.int("PER_PAGE")

BOT_TOKEN = env.str("BOT_TOKEN")
BOT_USERNAME = env.str("BOT_USERNAME")

DEVELOPERS = env.list("DEVELOPERS")
IP = env.str("ip")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

REDIS_HOST = env.str("REDIS_HOST")

POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASS}@{IP}/{DB_NAME}"
