import bpy

import core


class YouTubeRenderer(core.BaseThumbnailRenderer):

    def __init__(self, input_image=None, title_text="", domain=""):
        self.input_image = input_image
        self.title_text = title_text
        self.domain = domain

    def set_up(self):
        scene = self.get_scene()
        nodes = scene.node_tree.nodes

        # Camera orthographic scale is set to 5.0;
        # these are the dimensions of a single quadrant, in Blender units.
        width = 5.0
        height = width * (720.0 / 1280.0)

        # Determine the height at which we want the text to appear.
        base_line_height = (13.0 / 90) * (height * 2)
        newline_count = self.title_text.count('\n')
        multiline_scaling_factor = 0.5 if newline_count > 0 else 1.0
        nominal_line_height = base_line_height * multiline_scaling_factor

        # Text appears considerably smaller than the nominal size,
        # so we use this scaling factor to scale it up.
        # Determine the scaling factor experimentally
        # by setting the nominal text size to 1.0
        # and measuring the ascent manually.
        # If the font changes, you may have to re-measure this.
        actual_line_height = nominal_line_height / 0.5627

        # Assign properties to the text geometry.
        text_geom = bpy.data.curves["TitleText"]
        text_geom.body = self.title_text.upper()
        text_geom.size = actual_line_height

        # Position text object appropriately.
        vertical_offset = newline_count * actual_line_height / 2
        bpy.data.objects["TitleText"].location = (
            (0, vertical_offset, 0))

        # Set the domain color in the node tree.
        domain_color = self.get_domain_color(self.domain)
        nodes["DomainColor"].outputs[0].default_value = domain_color

        image_valid = self.set_image(nodes["InputImage"], self.input_image)
        if not image_valid:
            return "Failed to load image"
