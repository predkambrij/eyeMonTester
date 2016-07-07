from multiprocessing import Process
import matplotlib.pyplot as plt

from common import Common as Cmn

# control flags
debugProcessLogLine = False

class Blackpixels:
    def __init__(self):
        pass

    @staticmethod
    def processLogLine(output, bPixes, lBlinks, rBlinks, jBlinks):
        if output.startswith("debug_bp_log_pix:"):
            flowsInfo = [x for x in output.split(" ") if x != ""]
            if debugProcessLogLine:
                print repr(flowsInfo)
            fn   = int(flowsInfo[flowsInfo.index("F")+1])
            ts   = float(flowsInfo[flowsInfo.index("T")+1])
            lNum, rNum = float(flowsInfo[flowsInfo.index("lNum")+1]), float(flowsInfo[flowsInfo.index("rNum")+1])

            bPixes.append({"fn":fn, "ts":ts, "lNum":lNum, "rNum":rNum})
            Blackpixels.postProcessLogLine(bPixes, lBlinks, rBlinks, jBlinks, False)
        elif output.startswith("exiting"):
            return True
        return False

    @staticmethod
    def postProcessLogLine(bPixes, lBlinks, rBlinks, jBlinks, isEnd):
        if not isEnd:
            window = 600
        else:
            window = 0

        if not isEnd and (len(bPixes) == 0 or len(bPixes) % window != 0):
            return
        #print repr(bPixes)
        if isEnd:
            window = 0
        pltx = [x["fn"] for x in bPixes[-window:]]
        lNum, rNum = [x["lNum"] for x in bPixes[-window:]], [x["rNum"] for x in bPixes[-window:]]

        plt.figure(1)
        plt.plot(pltx, lNum, 'ro-')
        plt.figure(2)
        #plt.subplot(211)
        plt.plot(pltx, rNum, 'bo-')
        #plt.plot(pltx, lNum, 'ro-', pltx, rNum, 'bo-')
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

