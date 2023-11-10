import configparser

class ServerPramCfg:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(r"./data/cfg/Service.cfg")
        self.serverPramDict = {}
        self.tubePramDict = {}

    def cfg_load(self):
        for i in self.config.items('Server'):
            try:
                self.serverPramDict[i[0]] = int(i[1])
            except:
                self.serverPramDict[i[0]] = str(i[1])
        for i in self.config.items('Tube'):
            try:
                self.tubePramDict[i[0]] = float(i[1])
            except:
                self.tubePramDict[i[0]] = str(i[1])
        return self.serverPramDict, self.tubePramDict