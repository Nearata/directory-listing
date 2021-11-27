from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
FAVICON = config("FAVICON", cast=str, default=None)
HEADER = config("HEADER", cast=bool, default=True)
CUSTOM_CSS = config("CUSTOM_CSS", cast=CommaSeparatedStrings, default=[])
RENDER_README = config("RENDER_README", cast=bool, default=False)
