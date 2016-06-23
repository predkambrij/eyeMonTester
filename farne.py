from multiprocessing import Process
import matplotlib.pyplot as plt

from common import Common as Cmn

# control flags
debugProcessLogLine = False

class Farne:
    def __init__(self):
        pass

    @staticmethod
    def processLogLine(output, fFlows, lBlinks, rBlinks):
        if output.startswith("debug_fb_log_flow:"):
            flowsInfo = [x for x in output.split(" ") if x != ""]
            if debugProcessLogLine:
                print repr(flowsInfo)
            fn   = int(flowsInfo[flowsInfo.index("F")+1])
            ts   = float(flowsInfo[flowsInfo.index("T")+1])
            lTotalX, lTotalY = float(flowsInfo[flowsInfo.index("lTotal")+1]), float(flowsInfo[flowsInfo.index("lTotal")+2])
            rTotalX, rTotalY = float(flowsInfo[flowsInfo.index("rTotal")+1]), float(flowsInfo[flowsInfo.index("rTotal")+2])
            lbtotalX, lbtotalY = float(flowsInfo[flowsInfo.index("lbtotal")+1]), float(flowsInfo[flowsInfo.index("lbtotal")+2])
            rbtotalX, rbtotalY = float(flowsInfo[flowsInfo.index("rbtotal")+1]), float(flowsInfo[flowsInfo.index("rbtotal")+2])
            lDiffX, lDiffY = float(flowsInfo[flowsInfo.index("lDiff")+1]), float(flowsInfo[flowsInfo.index("lDiff")+2])
            rDiffX, rDiffY = float(flowsInfo[flowsInfo.index("rDiff")+1]), float(flowsInfo[flowsInfo.index("rDiff")+2])

            fFlows.append({"fn":fn, "ts":ts,
                "lTotalX":lTotalX, "lTotalY":lTotalY, "rTotalX":rTotalX, "rTotalY":rTotalY,
                "lbtotalX":lbtotalX, "lbtotalY":lbtotalY, "rbtotalX":rbtotalX, "rbtotalY":rbtotalY,
                "lDiffX":lDiffX, "lDiffY":lDiffY, "rDiffX":rDiffX, "rDiffY":rDiffY,
            })
            Farne.postProcessLogLine(fFlows, lBlinks, rBlinks, False)
        elif output.startswith("exiting"):
            return True
        return False

    @staticmethod
    def postProcessLogLine(fFlows, lBlinks, rBlinks, isEnd):
        if not isEnd:
            window = 300
        else:
            window = 0

        if not isEnd and (len(fFlows) == 0 or len(fFlows) % window != 0):
            return
        print repr(fFlows)
        if isEnd:
            window = 0
        pltx = [x["fn"] for x in fFlows[-window:]]
        pltlXdiff, pltlYdiff = [x["lDiffX"] for x in fFlows[-window:]], [x["lDiffY"] for x in fFlows[-window:]]
        pltrXdiff, pltrYdiff = [x["rDiffX"] for x in fFlows[-window:]], [x["rDiffY"] for x in fFlows[-window:]]

        plt.figure(1)
        plt.subplot(211)
        plt.plot(pltx, pltlXdiff, 'ro-', pltx, pltrXdiff, 'bo-')

        plt.subplot(212)
        plt.plot(pltx, pltlYdiff, 'ro-', pltx, pltrYdiff, 'bo-')
        plt.show()
        #plt.show(block=False)

        # if len(p) == 0:
        #     p.append(Process(target=plt.show))
        #     p[0].start()
        # else:
        #     p[0].terminate()
        #     p.pop()
        #     p.append(Process(target=plt.show))
        #     p[0].start()

        #plt.plot(pltx, pltlYdiff, 'ro-', pltx, pltrYdiff, 'ro-')
        #plt.show()
        return

