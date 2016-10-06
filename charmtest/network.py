import io
import argparse


class Wget(object):

    name = "wget"

    def __init__(self, network):
        self._network = network

    def __call__(self, proc_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("url")
        parser.add_argument("-O", dest="output")
        parser.add_argument("-q", dest="quiet", action="store_true")
        args = parser.parse_args(proc_args["args"][1:])
        content = self._network[args.url]
        result = {}
        if args.output == "-":
            result["stdout"] = io.BytesIO(content)
        else:
            with open(args.output, "wb") as fd:
                fd.write(content)
        return result
