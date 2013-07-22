import socket
class DeviceUnit(object):
    def __init__(self):
        self.host_name = socket.gethostname()
        self.ip        = None

    def get_hostname(self):


