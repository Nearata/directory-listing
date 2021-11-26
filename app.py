from uvicorn import run as uvicorn_run

from directory_listing.main import create_app
from directory_listing.config import DEBUG


app = create_app()

def main() -> None:
    uvicorn_run(
        "app:app",
        host="127.0.0.1",
        port=8765,
        reload=DEBUG
    )


if __name__ == "__main__":
    main()
