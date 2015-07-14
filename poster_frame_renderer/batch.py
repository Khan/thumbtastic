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

if __name__ == "__main__":
    import bpy.path
    os.chdir(bpy.path.abspath("//"))


def render_batch(manifest_file):
    """Render a group of images, reading a JSON manifest.

    The manifest should be of the form:

        {
            "input_directory": "path/to/input",
            "output_directory": "path/to/output",
            "entries": [
                {
                    "image": "abc.png",
                    "title_text": "The Beauty\nof Algebra",
                    "has_image": true
                },
                {
                    "image": "def.png",
                    "title_text": "No image here"
                },
                {
                    "image": "ghi.png",
                    "has_image": true
                }
            ]
        }

    The "image" entry is required, and specifies the input and output images
    (in the input and output directories, respectively).
    The "has_image" parameter is optional; the default is false.
    The "title_text" parameter is optional; the default is "".

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
        title_text = entry.get("title_text", "")
        has_image = entry.get("has_image", False)

        input_file = os.path.join(input_directory, image) if has_image else ""
        output_file = os.path.join(output_directory, image)

        if core.render_thumbnail(output_file, title_text, input_file):
            print("Success: %s" % image)
            success_count += 1
        else:
            print("Failure: %s" % image)
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
