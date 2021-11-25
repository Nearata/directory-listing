from uvicorn import run as uvicorn_run
from directory_listing.main import create_app


app = create_app()

def main() -> None:
    uvicorn_run(
        "app:app",
        host="127.0.0.1",
        port=8765,
        reload=True
    )


if __name__ == "__main__":
    main()
