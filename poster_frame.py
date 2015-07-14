import bpy

import core


class PosterFrameRenderer(core.BaseThumbnailRenderer):

    def __init__(self, input_image="", has_image=True):
        self.input_image = input_image
        self.has_image = has_image

    def set_up(self):
        scene = self.get_scene()
        nodes = scene.node_tree.nodes

        image_valid = self.set_image(nodes["InputImage"], self.input_image)
        self.set_switch(nodes["ImageExists"], image_valid)
        if self.has_image and not image_valid:
            return "Failed to load image"
