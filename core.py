import os

import bpy


class BaseThumbnailRenderer(object):
    """Abstract base type for rendering different thumbnail setups.

    Subclasses should implement a constructor and the set_up method,
    which sets the scene parameters as appropriate for rendering.
    This class provides a number of utility methods that may prove useful.

    Users can simply call the render method, passing the output file name.
    """

    def render(self, output_file):
        """Set up and render the scene, returning any error else None.
        
        If chdir=True, the CWD will be set to the blendfile directory
        before either setup or rendering is performed.
        """

        error = self.set_up()
        if error:
            return error

        self.get_scene().render.filepath = self.format_path(output_file)
        render_status = bpy.ops.render.render(write_still=True)

        if "FINISHED" not in render_status:
            return "Render did not complete normally"
        else:
            return None

    def set_up(self):
        """Set up a scene for rendering. Should be overridden by subclasses."""
        raise NotImplementedError()

    def log(self, msg):
        print(msg)

    def get_scene(self):
        """Get the current scene."""
        return bpy.context.scene

    def set_switch(self, node, toggle):
        """Set a compositor node to either 0 or 1.

        This is how we pass boolean values to the compositing node tree.
        The truthiness of the "toggle" parameter
        is used to determine whether the node will be 1 or 0.
        """

        node.outputs[0].default_value = 1 if toggle else 0

    def set_image(self, node, path):
        """Set the image node, and return whether it loaded successfully."""

        node.image.filepath = self.format_path(path)
        image_valid = node.image.has_data
        return image_valid

    def format_path(self, path):
        """Convert a POSIX relative path to a Blender-style path.

        Absolute paths are the same in POSIX and Blender.
        However, Blender uses "//" for the current directory, not ".".
        
        Examples:
            /absolute/path.png  ==> /absolute/path.png
            relative/path.png   ==> //relative/path.png
            file.png            ==> //file.png
            ./file.png          ==> //file.png
            ./../file.png       ==> //../file.png
        """

        if path.startswith("/"):
            return path
        elif path.startswith("./"):
            return "/" + path[1:]
        else:
            return "//" + path

    def get_domain_color(self, domain):
        """Get the [r, g, b, alpha] color for a given domain.

        The input should be the domain as used in webapp;
        i.e., a string like 'math' or 'economics-finance-domain'.
        """

        # These are specified at: khan.github.io/thumbnail-sketches/
        domain_colors = {
            'math': '58c4dd',
            'science': 'c55f73',
            'humanities': 'f16257',
            'economics-finance-domain': 'd2923d',
            'computing': '76b056',
            'test-prep': 'b189c6',
            'partner-content': '46a592'
        }
        default_color = '46a592'
        hex_color = domain_colors.get(domain, default_color)
        r, g, b = (int(hex_color[2*i:2*(i+1)], 16) / 255.0 for i in range(3))
        return [r, g, b, 1.000]  # alpha
