import os


def find_code_dir():
    directory = os.getcwd()
    while directory != "/":
        if os.path.exists(os.path.join(directory, "metadata.yaml")):
            return directory
        directory = os.path.dirname(directory)  # pragma: no cover
    else:  # pragma: no cover
        raise RuntimeError("This doesn't seem to be a charm code tree")
