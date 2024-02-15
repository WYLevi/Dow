import configparser

class ServerPramCfg:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(r"./data/cfg/Service.cfg")
        self.serverPramDict = {}
        self.tubePramDict = {}
        self.offsetPramDict = {}

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
    
class CamPramCfg:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(r"./data/cfg/CamSet.cfg")
        self.colorList  = ["Orange", "Blue", "Gray"]
        self.specList = [80, 90, 100, 125, 150, 200]
        self.camPramDict = {}

    def cfg_load(self):
        self.camPramDict["Trigger_Activation"]= self.config.get("Trigger", "Activation")
        self.camPramDict["Calibration_exposuretime"]= self.config.getint("Calibration", "exposuretime")
        self.camPramDict["Calibration_gain"]= self.config.getfloat("Calibration", "gain")
        self.camPramDict["Calibration_gamma"]= self.config.getfloat("Calibration", "gamma")
        self.camPramDict["Calibration_BlackLevel"]= self.config.getfloat("Calibration", "BlackLevel")
        self.camPramDict["Calibration_DigitalShift"]= self.config.getint("Calibration", "DigitalShift")
        self.camPramDict["Calibration_L1"]= self.config.getint("Calibration", "L1")
        self.camPramDict["Calibration_L2"]= self.config.getint("Calibration", "L2")
        self.camPramDict["Calibration_L3"]= self.config.getint("Calibration", "L3") 
        for color in self.colorList:
            for spec in self.specList:
                self.camPramDict["{}_{}_exposuretime".format(color, spec)]= self.config.getint("{}_{}".format(color, spec), "exposuretime")
                self.camPramDict["{}_{}_gain".format(color, spec)]= self.config.getfloat("{}_{}".format(color, spec), "gain")
                self.camPramDict["{}_{}_gamma".format(color, spec)]= self.config.getfloat("{}_{}".format(color, spec), "gamma")
                self.camPramDict["{}_{}_BlackLevel".format(color, spec)]= self.config.getfloat("{}_{}".format(color, spec), "BlackLevel")
                self.camPramDict["{}_{}_DigitalShift".format(color, spec)]= self.config.getint("{}_{}".format(color, spec), "DigitalShift")
                self.camPramDict["{}_{}_L1".format(color, spec)]= self.config.getint("{}_{}".format(color, spec), "L1")
                self.camPramDict["{}_{}_L2".format(color, spec)]= self.config.getint("{}_{}".format(color, spec), "L2")
                self.camPramDict["{}_{}_L3".format(color, spec)]= self.config.getint("{}_{}".format(color, spec), "L3")           
        return self.camPramDict
    
class offsetPramCfg:
    def __init__(self, tubeSpec):
        self.cfgFile = "./data/cfg/manual measurement/{}.cfg".format(tubeSpec)
        self.config = configparser.ConfigParser()
        self.config.read(self.cfgFile)
        self.offsetPramDict = {}

    def cfg_load(self):
        self.offsetPramDict["triggerpoint"]= self.config.getfloat("Offset", "triggerpoint")
        self.offsetPramDict["d_0"]= self.config.getfloat("Offset", "diameter_0")
        self.offsetPramDict["d_23"]= self.config.getfloat("Offset", "diameter_23")
        self.offsetPramDict["d_45"]= self.config.getfloat("Offset", "diameter_45")
        self.offsetPramDict["d_68"]= self.config.getfloat("Offset", "diameter_68")
        self.offsetPramDict["d_90"]= self.config.getfloat("Offset", "diameter_90")
        self.offsetPramDict["d_113"]= self.config.getfloat("Offset", "diameter_113")
        self.offsetPramDict["d_135"]= self.config.getfloat("Offset", "diameter_135")
        self.offsetPramDict["d_158"]= self.config.getfloat("Offset", "diameter_158")
        self.offsetPramDict["t_0"]= self.config.getfloat("Offset", "thickness_0")
        self.offsetPramDict["t_23"]= self.config.getfloat("Offset", "thickness_23") 
        self.offsetPramDict["t_45"]= self.config.getfloat("Offset", "thickness_45") 
        self.offsetPramDict["t_68"]= self.config.getfloat("Offset", "thickness_68") 
        self.offsetPramDict["t_90"]= self.config.getfloat("Offset", "thickness_90") 
        self.offsetPramDict["t_113"]= self.config.getfloat("Offset", "thickness_113") 
        self.offsetPramDict["t_135"]= self.config.getfloat("Offset", "thickness_135") 
        self.offsetPramDict["t_158"]= self.config.getfloat("Offset", "thickness_158") 
        self.offsetPramDict["t_180"]= self.config.getfloat("Offset", "thickness_180") 
        self.offsetPramDict["t_203"]= self.config.getfloat("Offset", "thickness_203") 
        self.offsetPramDict["t_225"]= self.config.getfloat("Offset", "thickness_225") 
        self.offsetPramDict["t_248"]= self.config.getfloat("Offset", "thickness_248") 
        self.offsetPramDict["t_270"]= self.config.getfloat("Offset", "thickness_270") 
        self.offsetPramDict["t_293"]= self.config.getfloat("Offset", "thickness_293") 
        self.offsetPramDict["t_315"]= self.config.getfloat("Offset", "thickness_315") 
        self.offsetPramDict["t_338"]= self.config.getfloat("Offset", "thickness_338")         
        return self.offsetPramDict
    
class calibrationOPPramCfg:
    def __init__(self, tubeSpec):
        self.cfgFile = "./data/cfg/manual measurement/{}.cfg".format(tubeSpec)
        self.config = configparser.ConfigParser()
        self.config.read(self.cfgFile)
        self.calibrationOPPramDict = {}

    def cfg_load(self):
        self.calibrationOPPramDict["quadrant_1"]= self.config.getfloat("Thickness", "quadrant_1")
        self.calibrationOPPramDict["quadrant_2"]= self.config.getfloat("Thickness", "quadrant_2")
        self.calibrationOPPramDict["quadrant_3"]= self.config.getfloat("Thickness", "quadrant_3")
        self.calibrationOPPramDict["quadrant_4"]= self.config.getfloat("Thickness", "quadrant_4")
        self.calibrationOPPramDict["d_0"]= self.config.getfloat("Diameter", "diameter_0")
        self.calibrationOPPramDict["d_23"]= self.config.getfloat("Diameter", "diameter_23")
        self.calibrationOPPramDict["d_45"]= self.config.getfloat("Diameter", "diameter_45")
        self.calibrationOPPramDict["d_68"]= self.config.getfloat("Diameter", "diameter_68")
        self.calibrationOPPramDict["d_90"]= self.config.getfloat("Diameter", "diameter_90")
        self.calibrationOPPramDict["d_113"]= self.config.getfloat("Diameter", "diameter_113")
        self.calibrationOPPramDict["d_135"]= self.config.getfloat("Diameter", "diameter_135")
        self.calibrationOPPramDict["d_158"]= self.config.getfloat("Diameter", "diameter_158")
        self.calibrationOPPramDict["rp_t_0"]= self.config.getfloat("Raw Pixel", "thickness_0")
        self.calibrationOPPramDict["rp_t_23"]= self.config.getfloat("Raw Pixel", "thickness_23") 
        self.calibrationOPPramDict["rp_t_45"]= self.config.getfloat("Raw Pixel", "thickness_45") 
        self.calibrationOPPramDict["rp_t_68"]= self.config.getfloat("Raw Pixel", "thickness_68") 
        self.calibrationOPPramDict["rp_t_90"]= self.config.getfloat("Raw Pixel", "thickness_90") 
        self.calibrationOPPramDict["rp_t_113"]= self.config.getfloat("Raw Pixel", "thickness_113") 
        self.calibrationOPPramDict["rp_t_135"]= self.config.getfloat("Raw Pixel", "thickness_135") 
        self.calibrationOPPramDict["rp_t_158"]= self.config.getfloat("Raw Pixel", "thickness_158") 
        self.calibrationOPPramDict["rp_t_180"]= self.config.getfloat("Raw Pixel", "thickness_180") 
        self.calibrationOPPramDict["rp_t_203"]= self.config.getfloat("Raw Pixel", "thickness_203") 
        self.calibrationOPPramDict["rp_t_225"]= self.config.getfloat("Raw Pixel", "thickness_225") 
        self.calibrationOPPramDict["rp_t_248"]= self.config.getfloat("Raw Pixel", "thickness_248") 
        self.calibrationOPPramDict["rp_t_270"]= self.config.getfloat("Raw Pixel", "thickness_270") 
        self.calibrationOPPramDict["rp_t_293"]= self.config.getfloat("Raw Pixel", "thickness_293") 
        self.calibrationOPPramDict["rp_t_315"]= self.config.getfloat("Raw Pixel", "thickness_315") 
        self.calibrationOPPramDict["rp_t_338"]= self.config.getfloat("Raw Pixel", "thickness_338")
        self.calibrationOPPramDict["rp_d_0"]= self.config.getfloat("Raw Pixel", "diameter_0")
        self.calibrationOPPramDict["rp_d_23"]= self.config.getfloat("Raw Pixel", "diameter_23")
        self.calibrationOPPramDict["rp_d_45"]= self.config.getfloat("Raw Pixel", "diameter_45")
        self.calibrationOPPramDict["rp_d_68"]= self.config.getfloat("Raw Pixel", "diameter_68")
        self.calibrationOPPramDict["rp_d_90"]= self.config.getfloat("Raw Pixel", "diameter_90")
        self.calibrationOPPramDict["rp_d_113"]= self.config.getfloat("Raw Pixel", "diameter_113")
        self.calibrationOPPramDict["rp_d_135"]= self.config.getfloat("Raw Pixel", "diameter_135")
        self.calibrationOPPramDict["rp_d_158"]= self.config.getfloat("Raw Pixel", "diameter_158")

        return self.calibrationOPPramDict