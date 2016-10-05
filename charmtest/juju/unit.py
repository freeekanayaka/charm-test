class Unit(object):

    def __init__(self, application, number):
        self.log = []
        self.ports = {}
        self.number = number
        self._application = application

    @property
    def name(self):
        return "{}/{}".format(self._application.name, self.number)
