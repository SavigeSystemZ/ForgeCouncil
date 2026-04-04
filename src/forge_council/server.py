"""CLI entry: `forge-council-api` or `python -m forge_council.server`."""

from __future__ import annotations


def main() -> None:
    import uvicorn

    host = __import__("os").environ.get("FC_API_HOST", "127.0.0.1")
    port = int(__import__("os").environ.get("FC_API_PORT", "8010"))
    uvicorn.run(
        "forge_council.api_app:app",
        host=host,
        port=port,
        factory=False,
        reload=__import__("os").environ.get("FC_API_RELOAD", "").lower() in ("1", "true", "yes"),
    )


if __name__ == "__main__":
    main()
