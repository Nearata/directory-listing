from datetime import datetime
from pathlib import Path
from typing import List, Optional

from humanize import naturalsize
from markdown import markdown
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates, _TemplateResponse

from .config import CUSTOM_CSS, DEBUG, FAVICON, HEADER, RENDER_README

templates = Jinja2Templates(directory="templates")
templates.env.globals.update(
    {"favicon": FAVICON, "header": HEADER, "custom_css": CUSTOM_CSS}
)


async def homepage(request: Request) -> _TemplateResponse:
    url = request.url_for("homepage")
    query: Optional[str] = request.query_params.get("dir")

    files: List[Path] = []
    parent_directory = None
    current_path = None

    if query:
        current_path = Path("public/" + query)
        files.extend(current_path.glob("*"))

        if query != "/":
            parent_directory = f"{url}?dir={Path(query).parent.as_posix()}"
    else:
        current_path = Path("public")
        files.extend(current_path.glob("*"))

    files = [i for i in files if i.name != ".gitkeep"]

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

    readme = current_path.joinpath("readme.md")
    html = None

    if RENDER_README and readme.exists():
        with readme.open() as r:
            html = markdown(r.read())

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "files": sorted(files2, key=lambda d: d["is_dir"], reverse=True),
            "parent_directory": parent_directory,
            "readme": html,
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
