from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
FAVICON = config("FAVICON", cast=str, default=None)
