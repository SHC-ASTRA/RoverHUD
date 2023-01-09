"""WaypointWidget implementation."""
from app import app, graphics
from app.widgets import widget
import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec3


class WaypointWidget(widget.Widget):
    """Widget for projecting 3D waypoints onto a camera stream."""

    # vertex_source = """#version 150 core
    #     in vec3 position;
    #     in vec4 colors;
    #     out vec4 vertex_colors;

    #     uniform WindowBlock
    #     {                       // This UBO is defined on Window creation, and available
    #         mat4 projection;    // in all Shaders. You can modify these matrixes with the
    #         mat4 view;          // Window.view and Window.projection properties.
    #     } window;

    #     uniform mat4 rover_view;

    #     void main()
    #     {
    #         gl_Position = window.projection * rover_view * vec4(position, 1.0);
    #         vertex_colors = colors;
    #     }
    # """  # noqa

    # fragment_source = """#version 150 core
    #     in vec4 vertex_colors;
    #     out vec4 final_color;

    #     void main()
    #     {
    #         final_color = vertex_colors;
    #     }
    # """

    def __init__(
        self, size: widget.Size, position: widget.Position = widget.Position()
    ):
        super().__init__(size, position)

        # World Setup
        # self.rover_position = Vec3(0, 0, 5)
        # self.rover_normal = Vec3(0, 1, 0)
        # self.rover_direction = Vec3(0, 0, -1)

        # OpenGL Setup
        # self.vert_shader = Shader(self.vertex_source, "vertex")
        # self.frag_shader = Shader(self.fragment_source, "fragment")
        # self.shader_program = ShaderProgram(self.vert_shader, self.frag_shader)
        # self.group = graphics.ShaderGroup(self.shader_program)

        # self.update_rover_view()

    def register(self, app: app.App):
        """
        Register WaypointWidget with current app.

        Args:
            app (app.App): Current application.

        """
        self.batch = app.Background3D

        # self.test_pyramid = self.shader_program.vertex_list(
        #     3,
        #     pyglet.gl.GL_TRIANGLES,
        #     batch=self.batch,
        #     position="f",
        #     group=self.group,
        #     colors="Bn",
        # )
        # self.test_pyramid.position[:] = (-2, 5, -10, 5, 0, -10, 5, 5, -10)
        # self.test_pyramid.colors[:] = (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 0)

        # self.test_waypoint = Waypoint(
        #     0, 0, 0, self.shader_program, self.batch, self.group
        # )

        self.test = pyglet.resource.model("waypoint.obj", batch=self.batch)
        self.rotate = 0

    def update(self, app: app.App):
        """
        Update the state of the WaypointWidget.

        Args:
            app (app.App): Current application.

        """
        # self.test_waypoint.rotate_y(0.02)
        self.rotate += 0.01
        self.test.matrix = Mat4.from_translation((0, 0, 0)) @ Mat4.from_rotation(
            self.rotate, Vec3(1, 0, 0)
        )

        # self.rover_position -= Vec3(-1, 0, 0)
        # print(self.rover_position)
        # self.update_rover_view()

    # # OpenGL Methods
    # def update_rover_view(self):
    #     self.shader_program.bind()

    #     self.shader_program["rover_view"] = Mat4.look_at(
    #         position=self.rover_position,
    #         target=self.rover_position + self.rover_direction,
    #         up=self.rover_normal,
    #     )

    #     self.shader_program.unbind()


class Waypoint:
    """
    Class to represent waypoint.

    Class Variables:
        height: height in meters from top to bottom
        width: width in meters from side to side

    Layout:
        0: top vertex
        1: front-right vertex
        2: front-left vertex
        3: back-right vertex
        4: back-left vertex
        5: bottom vertex
    """

    height = 1.5
    width = 0.75

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        program: ShaderProgram,
        batch: pyglet.graphics.Batch,
        group: graphics.ShaderGroup,
    ):
        self.x, self.y, self.z = x, y, z
        self.vertex_outline = program.vertex_list_indexed(
            count=6,
            mode=pyglet.gl.GL_TRIANGLES,
            indices=[0, 1, 2]
            + [0, 2, 3]
            + [0, 3, 4]
            + [0, 4, 1]
            + [5, 1, 2]
            + [5, 2, 3]
            + [5, 3, 4]
            + [5, 4, 1],
            batch=batch,
            group=group,
            position="f",
            colors="Bn",
        )
        self.generate_vertices()

    def generate_vertices(self):
        w2 = self.width / 2
        h2 = self.height / 2
        x, y, z = self.x, self.y, self.z

        top = [x, y + h2, z]
        bottom = [x, y - h2, z]
        fr = [x + w2, y, z + w2]
        fl = [x - w2, y, z + w2]
        br = [x + w2, y, z - w2]
        bl = [x - w2, y, z - w2]

        self.vertices = top + fr + fl + br + bl + bottom

        self.vertex_outline.position[:] = self.vertices
        self.vertex_outline.colors[:] = (
            [255, 0, 0, 255]
            + [0, 255, 0, 255]
            + [0, 0, 255, 255]
            + [0, 255, 255, 255]
            + [255, 255, 0, 255]
            + [255, 255, 255, 255]
        )

    def rotate_y(self, theta):
        pass
