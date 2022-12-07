"""StreamWidget implementation."""
from app import app
from app.widgets import widget
import gi
import numpy as np
import pyglet

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GstApp  # noqa


class StreamWidget(widget.Widget):
    """
    Widget for streaming data from a Gstreamer pipeline.

    Notes:
        Pipeline must include an appsink named "sink" for
        the widget to be able to hook into the stream.

        Currently only supports caps of `video/x-raw, format=RGB`.

    """

    def __init__(
        self,
        size: widget.Size,
        launch: str,
        position: widget.Position = widget.Position(),
    ):
        """
        Create a StreamWidget.

        Args:
            size (widget.Size): Size of the widget in pixels
            launch (str): Gstreamer launch string. Gets parsed into a pipeline.
            position (widget.Position, optional): _description_. Defaults to widget.Position().

        """
        self.width = size.width
        self.height = size.height
        self.launch = launch
        self.x = position.x
        self.y = position.y

        self.image = None
        self.sprite = None

        self.process_gst_launch()

    def register(self, app: app.App):
        """
        Register StreamWidget with current app.

        Args:
            app (app.App): Current application.

        """
        self.batch = app.Background2D

    def process_gst_launch(self):
        """Process Gstreamer launch string."""
        Gst.init()
        self.pipeline = Gst.parse_launch(self.launch)

        sink = self.pipeline.get_by_name("sink")
        self.pipeline.set_state(Gst.State.PLAYING)
        sink.connect("new-sample", self.on_new_sample)

    def update(self, app: app.App):
        """
        Update the state of the StreamWidget.

        The function checks to see whether self.sprite has been
        initalized yet. If not, then once an image from the stream
        is available, it creates a new sprite with it.

        If self.sprite does exist, then it updates the sprite with
        the latest image from the Gstreamer pipeline.

        Args:
            app (app.App): Current application.

        """
        if self.sprite is None:
            if self.image is not None:
                self.sprite = pyglet.sprite.Sprite(
                    x=self.x, y=self.y, img=self.image, batch=self.batch
                )
                self.scale_stream()
        else:
            self.sprite.image = self.image

    def scale_stream(self):
        """Scale video stream sprite to match widget size."""
        if self.sprite is not None:
            self.sprite.scale_x = (
                1.0 + (self.width - self.stream_width) / self.stream_width
            )
            self.sprite.scale_y = (
                1.0 + (self.height - self.stream_height) / self.stream_height
            )

    def on_new_sample(self, appsink):
        """
        Process incoming video frame from pipeline.

        Args:
            appsink (_type_): Appsink element from pipeline.

        Raises:
            RuntimeError: If there is an error transferring the
            image buffer to python.

        Returns:
            int: Dummy return value to keep C Bindings happy.

        """
        sample = appsink.pull_sample()
        caps = sample.get_caps()

        # Extract the width and height info from the sample's caps
        height = caps.get_structure(0).get_value("height")
        width = caps.get_structure(0).get_value("width")

        self.stream_width = width
        self.stream_height = height

        # Get the actual data

        buffer = sample.get_buffer()
        # Get read access to the buffer data
        success, map_info = buffer.map(Gst.MapFlags.READ)

        if not success:
            raise RuntimeError("Could not map buffer data!")

        numpy_frame = np.ndarray(
            shape=(height, width, 3), dtype=np.uint8, buffer=map_info.data
        )

        buffer.unmap(map_info)

        self.image = pyglet.image.ImageData(
            width, height, "RGB", numpy_frame.data, pitch=-(3 * width)
        )

        return 0
