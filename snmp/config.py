import yaml

class Configuration(object):
    def load(self,filename):
        f = open(filename)
        try:
            self.config = yaml.load(f.read())
            self.orgnization = Configuration.Orgnization(self.config["orgnization"])
            return self.orgnization
        finally:
            f.close()
    def get_orgnization(self):
        return self.orgnization

    class Group(object):
        def __init__(self,config):
            self.config = config
            self.name = config["name"]

        def get_name(self):
            return self.name

        def __str__(self):
            return self.config


    class Orgnization(object):
        def __init__(self,config):
            self.config = config
            self.name = config["name"]
            self.zk_cluster = config["zk_cluster"]
            self.group = Configuration.Group(config["group"])

        def get_config(self):
            return self.config

        def get_name(self):
            return self.name

        def get_group(self):
            return self.group

        def get_zk_cluster(self):
            return self.zk_cluster

        def __str__(self):
            return str(self.config)


if __name__ == "__main__":
    conf = Configuration()
    org = conf.load("config.yml")
    print conf.get_orgnization()
    print conf.get_orgnization().get_name()
    print conf.get_orgnization().get_zk_cluster()

