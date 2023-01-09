"""Program entry point."""
import pyglet
from app import app
from app.widgets import stream_widget, widget, waypoint_widget


def main():
    """Program entry point."""
    width = 1280
    height = 720

    pyglet.resource.path = ["assets"]
    pyglet.resource.reindex()

    widgets = [
        stream_widget.StreamWidget(
            widget.Size(width, height),
            """v4l2src device=/dev/video0 ! image/jpeg, width=640, height=360 ! jpegdec !
                videoconvert ! video/x-raw, width=640, height=360, format=RGB !
                appsink sync=false max-buffers=1 drop=true name=sink emit-signals=true""",
        ),
        waypoint_widget.WaypointWidget(widget.Size(width, height)),
    ]

    hud = app.App(width, height, widgets)
    hud.run()


if __name__ == "__main__":
    main()
