import core


class GeneralRenderer(core.BaseThumbnailRenderer):

    def __init__(self, input_image=None, domain=""):
        self.input_image = input_image
        self.domain = domain

    def set_up(self):
        scene = self.get_scene()
        nodes = scene.node_tree.nodes

        # Set the domain color in the node tree.
        domain_color = self.get_domain_color(self.domain)
        nodes["DomainColor"].outputs[0].default_value = domain_color

        image_valid = self.set_image(nodes["InputImage"], self.input_image)
        if not image_valid:
            return "Failed to load image"
