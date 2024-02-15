import sys
sys.path.append("./")
from utils.GetCfg import ServerPramCfg, offsetPramCfg, calibrationOPPramCfg
import math

def distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def offset_replace(offsetcfg, calibrationOPValue, pxTomm, angle, distanceByPixel ,mode):
    biasValue = calibrationOPValue / float(pxTomm) - distanceByPixel
    if mode == 'T':
        offsetcfg.config.set('Offset', 'thickness_{}'.format(angle), str(float(biasValue)))
        offsetcfg.config.set('Raw Pixel', 'thickness_{}'.format(angle), str(distanceByPixel))
    else:
        offsetcfg.config.set('Offset', 'diameter_{}'.format(angle), str(float(biasValue)))
        offsetcfg.config.set('Raw Pixel', 'diameter_{}'.format(angle), str(distanceByPixel))
    with open(offsetcfg.cfgFile, 'w', encoding='utf-8') as configfile:
        offsetcfg.config.write(configfile)

def correction_replace(detectAngle, spec, pxTomm, firstTube = False, outerAngle = None, inngerAngle = None):
    finishAngle = set()
    offsetcfg = offsetPramCfg(spec)
    calibrationOPPramDict = calibrationOPPramCfg(spec).cfg_load()
    for angle in detectAngle:
        thicknessByCalOP = float(calibrationOPPramDict['quadrant_{}'.format(angle // 90 + 1)])
        if firstTube:
            thicknessByPixel = distance_between_points(inngerAngle[angle], outerAngle[angle])
        else:
            thicknessByPixel = float(calibrationOPPramDict['rp_t_{}'.format(angle)])
        offset_replace(offsetcfg, thicknessByCalOP, pxTomm, angle, thicknessByPixel, 'T')
        if angle not in finishAngle:
            diameterByCalOP = float(calibrationOPPramDict['d_{}'.format(angle)])
            if firstTube:
                diameterByPixel = distance_between_points(outerAngle[angle], outerAngle[(angle + 180) % 360])
            else:
                diameterByPixel = float(calibrationOPPramDict['rp_d_{}'.format(angle)])
            offset_replace(offsetcfg, diameterByCalOP, pxTomm, angle, diameterByPixel, 'D')
            finishAngle.add(angle)
            finishAngle.add((angle + 180) % 360)

if __name__ == '__main__':
    inngerAngle = {90.0: (1953, 881), 113.0: (1898, 1165), 135.0: (1745, 1396), 158.0: (1503, 1558), 180.0: (1229, 1609), 203.0: (945, 1550), 225.0: (715, 1395), 248.0: (556, 1153),
 270.0: (504, 881), 293.0: (561, 597), 315.0: (715, 367), 338.0: (956, 206), 0.0: (1229, 153), 23.0: (1514, 211), 45.0: (1743, 367), 68.0: (1901, 609)}
    outerAngle = {90.0: (2003, 881), 113.0: (1946, 1185), 135.0: (1783, 1435), 158.0: (1524, 1610), 180.0: (1229, 1669), 203.0: (922, 1605), 225.0: (675, 1435), 248.0: (507, 1173),
 270.0: (455, 881), 293.0: (520, 580), 315.0: (686, 338), 338.0: (942, 171), 0.0: (1229, 116), 23.0: (1528, 176), 45.0: (1772, 338), 68.0: (1943, 592)}
    spec = '灰-E-150'
    severParmDict, tubePramDict  = ServerPramCfg().cfg_load()
    quadrantValues = ([0, 23, 45, 68], [90, 113, 135, 158], [180, 203, 225, 248], [270, 293, 315, 338])
    quadrant1, quadrant2, quadrant3, quadrant4 = (quadrantValues if severParmDict['mode'] == 'env' else ([q[0]] for q in quadrantValues))   
    detectQUAD = (quadrant1, quadrant2, quadrant3, quadrant4)
    detectAngle = quadrant1 + quadrant2 + quadrant3 + quadrant4
    # correction_replace(detectAngle, spec, severParmDict['pxtomm'])
    correction_replace(detectAngle, spec, severParmDict['pxtomm'], firstTube=True, inngerAngle=inngerAngle, outerAngle=outerAngle)