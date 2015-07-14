import bpy

import core


class PosterFrameRenderer(core.BaseThumbnailRenderer):

    def __init__(self, input_image="", domain="math"):
        self.input_image = input_image
        self.domain = domain

    def set_up(self):
        scene = self.get_scene()
        nodes = scene.node_tree.nodes

        image_valid = self.set_image(nodes["InputImage"], self.input_image)
        if not image_valid:
            return "Failed to load image"

        domain_color = self.get_domain_color(self.domain)
        nodes["DomainColor"].outputs[0].default_value = domain_color
