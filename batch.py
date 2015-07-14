"""Batch renderer for thumbnails.

If you're reading this as a standalone file...don't.
Open me in blender via the main blendfile.

Reload me with Alt-R if changed (or unsure)! Also reload core.py (at right).
Then, click "Run Script" to change the CWD to the project directory,
and, in the console at the bottom of the screen, execute

    import batch
    batch.render_batch("path/to/manifest.py")
"""

import json
import os.path

import core


def render_batch(render_class, manifest_file):
    """Render a group of images, reading a JSON manifest.

    The render_class parameter should be a subclass of BaseThumbnailRenderer.

    The manifest should be of the form:

        {
            "input_directory": "path/to/input",
            "output_directory": "path/to/output",
            "entries": [
                {
                    "image": "abc.png",
                    ...
                }
            ]
        }

    The "image" attribute is required, and specifies the input and output images
    (in the input and output directories, respectively).

    Any other attribute are optional,
    and will be passed to the renderer's constructor.

    Returns a list of failed images.
    """

    with open(manifest_file, "r") as infile:
        manifest = json.load(infile)

    input_directory = manifest["input_directory"]
    output_directory = manifest["output_directory"]

    success_count = 0
    failures = []

    for entry in manifest["entries"]:
        image = entry["image"]
        input_file = os.path.join(input_directory, image)
        output_file = os.path.join(output_directory, image)

        del entry["image"]
        renderer = render_class(input_image=input_file, **entry)
        error = renderer.render(output_file, chdir=True)

        if not error:
            print("Success: %s" % image)
            success_count += 1
        else:
            print("Failure for %s: %s" % (image, error))
            failures.append(image)

    print("Done. Succeeded: %s. Failed: %s." % (success_count, len(failures)))
    if failures:
        print("The following %s failed to render:" %
              ("image" if len(failures) == 1 else "images"))
        for failure in failures:
            print(" - %s" % failure)
    else:
        print("OK")

    return failures
