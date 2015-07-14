import bpy

import core


class YouTubeRenderer(core.BaseThumbnailRenderer):

    def __init__(self, input_image="", has_image=True, title_text=""):
        self.input_image = input_image
        self.has_image = has_image
        self.title_text = title_text

    def set_up(self):
        scene = self.get_scene()
        nodes = scene.node_tree.nodes

        # Camera orthographic scale is set to 5.0;
        # these are the dimensions of a single quadrant, in Blender units.
        width = 5.0
        height = width * (720.0 / 1280.0)

        # Offset from the edge of the canvas
        offset = 0.02 * width

        nominal_text_size = 0.5  # in Blender units

        # The actual text height is considerably smaller than nominal.
        # Determine the scaling factor experimentally
        # by setting the nominal text size to 1.0
        # and measuring the ascent manually.
        # If the font changes, you may have to re-measure this.
        actual_text_height = nominal_text_size * 0.5627

        # Assign properties to the text geometry.
        text_geom = bpy.data.curves["TitleText"]
        text_geom.body = self.title_text.upper()
        text_geom.size = nominal_text_size
        self.set_switch(nodes["TextExists"], self.title_text)

        # Position text object appropriately.
        bpy.data.objects["TitleText"].location = (
            (0, height - offset - actual_text_height, 0))

        image_valid = self.set_image(nodes["InputImage"], self.input_image)
        self.set_switch(nodes["ImageExists"], image_valid)
        if self.has_image and not image_valid:
            return "Failed to load image"
