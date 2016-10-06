import argparse


class Dpkg(object):

    name = "dpkg"

    def __init__(self, packages):
        self._packages = packages

    def __call__(self, proc_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", dest="install")
        args = parser.parse_args(proc_args["args"][1:])
        if args.install:
            package = args.install
            actions = self._packages.setdefault(package, [])
            actions.append("install")
        return {}
