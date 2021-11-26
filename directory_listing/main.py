from datetime import datetime
from pathlib import Path
from typing import List

from humanize import naturalsize
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates, _TemplateResponse

from .config import DEBUG

templates = Jinja2Templates(directory="templates")


async def homepage(request: Request) -> _TemplateResponse:
    query = request.query_params.get("dir")
    files: List[Path] = []

    if query:
        files.extend(Path("public/" + query).glob("*"))
    else:
        files.extend(Path("public").glob("*"))

    for i in files:
        if i.name == ".gitkeep":
            files.remove(i)
            break

    files2 = []
    for i in files:
        f = {
            "is_dir": i.is_dir(),
            "filename": i.name,
            "size": naturalsize(i.stat().st_size, gnu=True),
            "date": datetime.fromtimestamp(i.stat().st_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
        url = request.url_for("homepage")

        if i.is_dir():
            f.update({"href": f"{url}?dir={i.as_posix().replace('public', '')}"})
        else:
            f.update(
                {
                    "href": request.url_for(
                        "public", path=i.as_posix().replace("public", "")
                    )
                }
            )

        files2.append(f)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "files": sorted(files2, key=lambda d: d["is_dir"], reverse=True),
        },
    )


def create_app() -> Starlette:
    routes = [
        Route("/", homepage),
        Mount("/public", StaticFiles(directory="public"), name="public"),
        Mount("/static", StaticFiles(directory="static"), name="static"),
    ]

    app = Starlette(debug=DEBUG, routes=routes)

    return app
