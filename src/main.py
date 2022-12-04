"""Program entry point."""
from app import app


def main():
    """Program entry point."""
    hud = app.App()
    hud.run()


if __name__ == "__main__":
    main()
