from multiprocessing import Process
import matplotlib.pyplot as plt

from common import Common as Cmn

# control flags
debugProcessLogLine = False

class Farne:
    def __init__(self):
        pass

    @staticmethod
    def processLogLine(output, annots, fFlows, fFlowsI, lBlinks, rBlinks):
        # if output.startswith("debug_fb_log_flow:"):
        #     flowsInfo = [x for x in output.split(" ") if x != ""]
        #     if debugProcessLogLine:
        #         print repr(flowsInfo)
        #     fn   = int(flowsInfo[flowsInfo.index("F")+1])
        #     ts   = float(flowsInfo[flowsInfo.index("T")+1])
        #     lTotalX, lTotalY = float(flowsInfo[flowsInfo.index("lTotal")+1]), float(flowsInfo[flowsInfo.index("lTotal")+2])
        #     rTotalX, rTotalY = float(flowsInfo[flowsInfo.index("rTotal")+1]), float(flowsInfo[flowsInfo.index("rTotal")+2])
        #     lbtotalX, lbtotalY = float(flowsInfo[flowsInfo.index("lbtotal")+1]), float(flowsInfo[flowsInfo.index("lbtotal")+2])
        #     rbtotalX, rbtotalY = float(flowsInfo[flowsInfo.index("rbtotal")+1]), float(flowsInfo[flowsInfo.index("rbtotal")+2])
        #     lDiffX, lDiffY = float(flowsInfo[flowsInfo.index("lDiff")+1]), float(flowsInfo[flowsInfo.index("lDiff")+2])
        #     rDiffX, rDiffY = float(flowsInfo[flowsInfo.index("rDiff")+1]), float(flowsInfo[flowsInfo.index("rDiff")+2])

        #     fFlows.append({"fn":fn, "ts":ts,
        #         "lTotalX":lTotalX, "lTotalY":lTotalY, "rTotalX":rTotalX, "rTotalY":rTotalY,
        #         "lbtotalX":lbtotalX, "lbtotalY":lbtotalY, "rbtotalX":rbtotalX, "rbtotalY":rbtotalY,
        #         "lDiffX":lDiffX, "lDiffY":lDiffY, "rDiffX":rDiffX, "rDiffY":rDiffY,
        #     })
        #     #Farne.postProcessLogLine(fFlows, lBlinks, rBlinks, False)
        if output.startswith("debug_blinks_d1:"):
            flowsInfo = [x for x in output.split(" ") if x != ""]
            if debugProcessLogLine:
                print repr(flowsInfo)
            if (flowsInfo[1:] == ['blinkMeasureSize', 'is', 'zero']
                or flowsInfo[3:7] == ['shortBmSize', 'is', 'less', 'than']
                or flowsInfo[3:7] == ['fps', 'of', 'the', 'first']
                or flowsInfo[3:-1] == ['shortBmSize', 'is', 'big', 'enough']
                or flowsInfo[1:3] == ['updated', 'maxFramesShortList']
                ):
                return False
            fn   = int(flowsInfo[flowsInfo.index("F")+1])
            ts   = float(flowsInfo[flowsInfo.index("T")+1])
            logType = flowsInfo[flowsInfo.index("logType")+1]
            if logType == "b":
                lDiff, rDiff = float(flowsInfo[flowsInfo.index("La")+1]), float(flowsInfo[flowsInfo.index("Ra")+1])
                #la, ra = float(flowsInfo[flowsInfo.index("La")+2]), float(flowsInfo[flowsInfo.index("Ra")+2])
                lSD, rSD = float(flowsInfo[flowsInfo.index("lrSD")+1]), float(flowsInfo[flowsInfo.index("lrSD")+2])
                plsd1, prsd1 = float(flowsInfo[flowsInfo.index("plrSD12")+1]), float(flowsInfo[flowsInfo.index("plrSD12")+3])
                plsd2, prsd2 = float(flowsInfo[flowsInfo.index("plrSD12")+2]), float(flowsInfo[flowsInfo.index("plrSD12")+4])
                mlsd1, mrsd1 = float(flowsInfo[flowsInfo.index("mlrSD12")+1]), float(flowsInfo[flowsInfo.index("mlrSD12")+3])
                mlsd2, mrsd2 = float(flowsInfo[flowsInfo.index("mlrSD12")+2]), float(flowsInfo[flowsInfo.index("mlrSD12")+4])

                fFlows.append({"fn":fn, "ts":ts, "type":logType, "lDiff":lDiff, "rDiff":rDiff,
                    "plsd1":plsd1, "prsd1":prsd1, "mlsd1":mlsd1, "mrsd1":mrsd1,
                    "plsd2":plsd2, "prsd2":prsd2, "mlsd2":mlsd2, "mrsd2":mrsd2,
                })
            elif logType == "l":
                lDiff, lSD = float(flowsInfo[flowsInfo.index("La")+1]), float(flowsInfo[flowsInfo.index("lrSD")+1])
                plsd1, plsd2 = float(flowsInfo[flowsInfo.index("plrSD12")+1]), float(flowsInfo[flowsInfo.index("plrSD12")+2])
                mlsd1, mlsd2 = float(flowsInfo[flowsInfo.index("mlrSD12")+1]), float(flowsInfo[flowsInfo.index("mlrSD12")+2])

                fFlows.append({"fn":fn, "ts":ts, "type":logType, "lDiff":lDiff,
                    "plsd1":plsd1, "plsd2":plsd2, "mlsd1":mlsd1, "mlsd2":mlsd2,
                })
            elif logType == "r":
                rDiff, rSD = float(flowsInfo[flowsInfo.index("Ra")+1]), float(flowsInfo[flowsInfo.index("lrSD")+1])
                prsd1, prsd2 = float(flowsInfo[flowsInfo.index("plrSD12")+1]), float(flowsInfo[flowsInfo.index("plrSD12")+2])
                mrsd1, mrsd2 = float(flowsInfo[flowsInfo.index("mlrSD12")+1]), float(flowsInfo[flowsInfo.index("mlrSD12")+2])

                fFlows.append({"fn":fn, "ts":ts, "type":logType, "rDiff":rDiff,
                    "prsd1":prsd1, "prsd2":prsd2, "mrsd1":mrsd1, "mrsd2":mrsd2,
                })
            elif logType == "n":
                fFlows.append({"fn":fn, "ts":ts, "type":logType})
            fFlowsI[fn] = len(fFlows)-1

            if annots[0].has_key(fn):
                fFlows[-1].update(annots[0][fn])
                fFlows[-1]["annotEvent"] = "s"
            if annots[1].has_key(fn):
                fFlows[-1].update(annots[1][fn])
                fFlows[-1]["annotEvent"] = "e"
            Farne.postProcessLogLine(fFlows, lBlinks, rBlinks, False)
        elif output.startswith("debug_blinks_d4:"):
            blinkInfo = output.split(" ")
            if blinkInfo[1] == "adding_lBlinkChunksf":
                lst = lBlinks
                eye = "l"
            elif blinkInfo[1] == "adding_rBlinkChunksf":
                lst = rBlinks
                eye = "r"

            fs = int(blinkInfo[blinkInfo.index("fs")+1])
            fe = int(blinkInfo[blinkInfo.index("fe")+1])
            start     = float(blinkInfo[blinkInfo.index("start")+1])
            end       = float(blinkInfo[blinkInfo.index("end")+1])
            duration  = float(blinkInfo[blinkInfo.index("duration")+1])
            if start > 1000000000:
                start /= 1000.
                end /= 1000.
            #start = datetime.datetime.fromtimestamp(start)
            blinkInfoDict = {"fs":fs, "fe":fe, "start":start, "end":end, "duration":duration}
            lst.append(blinkInfoDict)
            fFlows[fFlowsI[fs]][eye+"b"] = "s"
            fFlows[fFlowsI[fe]][eye+"b"] = "e"
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

        if isEnd:
            window = 0
        pltax = [x["fn"] for x in fFlows[-window:]]
        pltlx = [x["fn"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
        pltrx = [x["fn"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
        pltasx = [x["fn"] for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
        pltaex = [x["fn"] for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "e"]
        pltlbsx = [x["fn"] for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "s"]
        pltlbex = [x["fn"] for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "e"]
        pltrbsx = [x["fn"] for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "s"]
        pltrbex = [x["fn"] for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "e"]
        lDiff, rDiff = [x["lDiff"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["rDiff"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
        plsd1, mlsd1 = [x["plsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["mlsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
        plsd2, mlsd2 = [x["plsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["mlsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
        prsd1, mrsd1 = [x["prsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"], [x["mrsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
        prsd2, mrsd2 = [x["prsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"], [x["mrsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
        pltas = [1 for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
        pltae = [1 for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "e"]
        pltlbs = [1.1 for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "s"]
        pltlbe = [1.1 for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "e"]
        pltrbs = [1.2 for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "s"]
        pltrbe = [1.2 for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "e"]
        plt.figure(1)
        #plt.subplot(211)
        #plt.plot(pltx, pltlXdiff, 'ro-', pltx, pltrXdiff, 'bo-')

        #plt.subplot(212)
        plt.plot(pltlx, lDiff, 'ro-', pltrx, rDiff, 'bo-',
            pltax, [0 for x in xrange(len(pltax))], 'g--',
            pltlx, plsd1, 'r^-', pltlx, mlsd1, 'r^-', pltrx, prsd1, 'b^-', pltrx, mrsd1, 'b^-',
            pltlx, plsd2, 'r^-', pltlx, mlsd2, 'r^-', pltrx, prsd2, 'b^-', pltrx, mrsd2, 'b^-',
            pltasx, pltas, 'go', pltaex, pltae, 'g^',
            pltlbsx, pltlbs, 'ro', pltlbex, pltlbe, 'r^', pltrbsx, pltrbs, 'bo', pltrbex, pltrbe, 'b^'
        )
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

