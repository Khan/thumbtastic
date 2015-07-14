"""Core renderer for thumbnails.

If you're reading this as a standalone file...don't.
Open me in blender via the main blendfile.

Reload me with Alt-R if changed (or unsure)!
"""

import bpy


def render_thumbnail(output_path, title_text="", image_path=""):
    scene = bpy.data.scenes["TextScene"]
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
    text_geom.body = title_text.upper()
    text_geom.size = nominal_text_size

    # Position text object appropriately.
    bpy.data.objects["TitleText"].location = (
        (0, height - offset - actual_text_height, 0))

    nodes["InputImage"].image.filepath = _format_path(image_path)
    image_valid = nodes["InputImage"].image.has_data

    _set_switch(nodes["TextExists"], title_text)
    _set_switch(nodes["ImageExists"], image_valid)

    scene.render.filepath = _format_path(output_path)
    render_status = bpy.ops.render.render(write_still=True)
    return "FINISHED" in render_status


def _set_switch(node, toggle):
    """Set a compositor node to either 0 or 1.

    This is how we pass boolean values to the compositing node tree.
    The truthiness of the "toggle" parameter
    is used to determine whether the node will be 1 or 0.
    """

    node.outputs[0].default_value = 1 if toggle else 0


def _format_path(path):
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
