from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from .config import DEBUG

templates = Jinja2Templates(directory="templates")


async def homepage(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request})


def create_app() -> Starlette:
    routes = [
        Route("/", homepage),
        Mount("/public", StaticFiles(directory="public"), name="public"),
    ]

    app = Starlette(debug=DEBUG, routes=routes)

    return app
