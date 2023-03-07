import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


class Curve:
    def moving_average(X, Y):
        """
        曲線平滑化卷積
        """
        if len(X) < 10:
            kernal = 1
        else:
            kernal = 10
        window = np.ones(int(kernal)) / float(kernal)
        return np.convolve(Y, window, "same")

    def draw_cruve(device, YAverage, X, xCount, Y, NGThr, pxlTomm):
        """
        繪製翹曲曲線(已出板)
        """
        try:
            if len(YAverage) != 0:
                zs = savgol_filter(Y[:-1], 9, 3)
                plt.plot(X[:-1], zs, "g-", linewidth=1.0)
                plt.hlines(0, 0, xCount, color="blue")
                plt.hlines((NGThr) / pxlTomm, 0, xCount, color="red", linestyles="--")
                plt.ylim(-200, 800)
                plt.annotate("{}mm".format(NGThr), xy=(0, (NGThr) / pxlTomm + 10), color="red", size=15)
                plt.annotate("Baseline", xy=(0, -60), color="blue", size=12)
                plt.savefig("Substrate curve_{}.png".format(device))  ### 基板曲線影像
                plt.clf()
                YAverage = []
            result = False
            return YAverage, result
        except:
            print("Draw cruve error!")
            return YAverage, result
