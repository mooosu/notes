import os
from kazoo.client import KazooClient

class Store(object):
    def __init__(self,**kwargs):
        self.config = kwargs
        self.client = None

    def get_client(self):
        return self.client

    def open(self):
        self.client = KazooClient(**self.config)
        self.client.add_listener
        self.client.start()

    def close(self):
        self.client.stop()

    def read(self,path):
        return self.client.get(path)

    def write(self,path,value):
        base_path = os.path.dirname(path)
        self.client.ensure_path(base_path)
        self.client.create(path,value)

    def overwrite(self,path,value):
        self.client.set(path,value)

    def exists(self,path):
        return self.client.exists(path)

if __name__ == "__main__":
    store = Store(hosts="127.0.0.1:2181")
    store.open()
    path = "/a/b/c4"
    store.overwrite(path,"my data123")
    print store.read(path)
