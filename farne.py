from multiprocessing import Process
import matplotlib.pyplot as plt

from common import Common as Cmn

# control flags
debugProcessLogLine = False

class Farne:
    def __init__(self):
        pass

    @staticmethod
    def processLogLine(output, annots, fFlows, fFlowsI, tracking, lBlinks, rBlinks, jBlinks):
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
        #     #Farne.postProcessLogLine(fFlows, lBlinks, rBlinks, jBlinks, False)
        if output.startswith("debug_fb_log_reinit:") or output.startswith("debug_fb_log_repupil:"):
            pass
            #print output
        elif output.startswith("debug_fb_log_tracking:"):
            statusInfo = [x for x in output.split(" ") if x != ""]

            fn     = int(statusInfo[statusInfo.index("F")+1])
            ts     = float(statusInfo[statusInfo.index("T")+1])
            if statusInfo.count("status") == 1:
                status = statusInfo[statusInfo.index("status")+1]

                if status == "start":
                    if len(tracking["detecting"]) > 0:
                        if len(tracking["detecting"][-1]) != 2:
                            print "error: tracking start: previous entry is not finished yet %s (%s)" % (repr(tracking["detecting"][-1]), statusInfo)
                    tracking["detecting"].append([(status, fn, ts)])
                elif status == "stop":
                    if len(tracking["detecting"]) > 0:
                        if len(tracking["detecting"][-1]) == 1:
                            tracking["detecting"][-1].append((status, fn, ts))
                        else:
                            print "error: tracking stop: detecting[-1] is not len of 1 %s (%s)" % (repr(tracking["detecting"][-1]), statusInfo)
                    else:
                        print "error: tracking stop: len(detecting) is zero (%s)" % statusInfo
                else:
                    print "error: unknown tracking status (%s)" % statusInfo
            else:
                pass
                #print statusInfo
        elif output.startswith("debug_blinks_d1:"):
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
                la, ra = float(flowsInfo[flowsInfo.index("La")+2]), float(flowsInfo[flowsInfo.index("Ra")+2])
                lSD, rSD = float(flowsInfo[flowsInfo.index("lrSD")+1]), float(flowsInfo[flowsInfo.index("lrSD")+2])
                plsd1, prsd1 = float(flowsInfo[flowsInfo.index("plrSD12t")+1]), float(flowsInfo[flowsInfo.index("plrSD12t")+4])
                plsd2, prsd2 = float(flowsInfo[flowsInfo.index("plrSD12t")+2]), float(flowsInfo[flowsInfo.index("plrSD12t")+5])
                plsdt, prsdt = float(flowsInfo[flowsInfo.index("plrSD12t")+3]), float(flowsInfo[flowsInfo.index("plrSD12t")+6])
                mlsd1, mrsd1 = float(flowsInfo[flowsInfo.index("mlrSD12t")+1]), float(flowsInfo[flowsInfo.index("mlrSD12t")+4])
                mlsd2, mrsd2 = float(flowsInfo[flowsInfo.index("mlrSD12t")+2]), float(flowsInfo[flowsInfo.index("mlrSD12t")+5])
                mlsdt, mrsdt = float(flowsInfo[flowsInfo.index("mlrSD12t")+3]), float(flowsInfo[flowsInfo.index("mlrSD12t")+6])

                fFlows.append({"fn":fn, "ts":ts, "type":logType, "lDiff":lDiff, "rDiff":rDiff, "la":la, "ra":ra,
                    "plsd1":plsd1, "prsd1":prsd1, "mlsd1":mlsd1, "mrsd1":mrsd1,
                    "plsd2":plsd2, "prsd2":prsd2, "mlsd2":mlsd2, "mrsd2":mrsd2,
                    "plsdt":plsdt, "prsdt":prsdt, "mlsdt":mlsdt, "mrsdt":mrsdt,
                })
            elif logType == "l":
                lDiff, lSD = float(flowsInfo[flowsInfo.index("La")+1]), float(flowsInfo[flowsInfo.index("lrSD")+1])
                la = float(flowsInfo[flowsInfo.index("La")+2])
                plsd1, plsd2, plsdt = float(flowsInfo[flowsInfo.index("plrSD12t")+1]), float(flowsInfo[flowsInfo.index("plrSD12t")+2]), float(flowsInfo[flowsInfo.index("plrSD12t")+3])
                mlsd1, mlsd2, mlsdt = float(flowsInfo[flowsInfo.index("mlrSD12t")+1]), float(flowsInfo[flowsInfo.index("mlrSD12t")+2]), float(flowsInfo[flowsInfo.index("mlrSD12t")+3])

                fFlows.append({"fn":fn, "ts":ts, "type":logType, "lDiff":lDiff, "la":la,
                    "plsd1":plsd1, "plsd2":plsd2, "plsdt":plsdt, "mlsd1":mlsd1, "mlsd2":mlsd2, "mlsdt":mlsdt,
                })
            elif logType == "r":
                rDiff, rSD = float(flowsInfo[flowsInfo.index("Ra")+1]), float(flowsInfo[flowsInfo.index("lrSD")+1])
                ra = float(flowsInfo[flowsInfo.index("Ra")+2])
                prsd1, prsd2, prsdt = float(flowsInfo[flowsInfo.index("plrSD12t")+1]), float(flowsInfo[flowsInfo.index("plrSD12t")+2]), float(flowsInfo[flowsInfo.index("plrSD12t")+3])
                mrsd1, mrsd2, mrsdt = float(flowsInfo[flowsInfo.index("mlrSD12t")+1]), float(flowsInfo[flowsInfo.index("mlrSD12t")+2]), float(flowsInfo[flowsInfo.index("mlrSD12t")+3])

                fFlows.append({"fn":fn, "ts":ts, "type":logType, "rDiff":rDiff, "ra":ra,
                    "prsd1":prsd1, "prsd2":prsd2, "prsdt":prsdt, "mrsd1":mrsd1, "mrsd2":mrsd2, "mrsdt":mrsdt,
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
            #Farne.postProcessLogLine(fFlows, lBlinks, rBlinks, jBlinks, False)
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
        elif output.startswith("debug_blinks_d5:"):
            blinkInfo = output.split(" ")
            fs = int(blinkInfo[blinkInfo.index("fs")+1])
            fe = int(blinkInfo[blinkInfo.index("fe")+1])
            start     = float(blinkInfo[blinkInfo.index("start")+1])
            end       = float(blinkInfo[blinkInfo.index("end")+1])
            duration  = float(blinkInfo[blinkInfo.index("duration")+1])
            if start > 1000000000:
                start /= 1000.
                end /= 1000.

            blinkInfoDict = {"fs":fs, "fe":fe, "start":start, "end":end, "duration":duration}
            print "adding %s" % repr(blinkInfoDict)
            jBlinks.append(blinkInfoDict)
            fFlows[fFlowsI[fs]]["jb"] = "s"
            fFlows[fFlowsI[fe]]["jb"] = "e"
        elif output.startswith("exiting"):
            return True
        return False

    @staticmethod
    def postProcessLogLine(fFlows, lBlinks, rBlinks, jBlinks, isEnd):
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
        la, ra = [x["la"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["ra"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
        plsd1, mlsd1 = [x["plsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["mlsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
        plsd2, mlsd2 = [x["plsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["mlsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
        plsdt, mlsdt = [x["plsdt"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["mlsdt"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
        prsd1, mrsd1 = [x["prsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"], [x["mrsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
        prsd2, mrsd2 = [x["prsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"], [x["mrsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
        prsdt, mrsdt = [x["prsdt"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"], [x["mrsdt"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
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
        #plt.plot(pltlx, lDiff, 'ro-', pltrx, rDiff, 'bo-',
        #    pltax, [0 for x in xrange(len(pltax))], 'g--', # zero
        #    pltlx, la, 'r--', pltrx, ra, 'b--', # average
        #    #pltlx, plsd1, 'r^-', pltlx, mlsd1, 'r^-', pltrx, prsd1, 'b^-', pltrx, mrsd1, 'b^-',
        #    #pltlx, plsd2, 'r^-', pltlx, mlsd2, 'r^-', pltrx, prsd2, 'b^-', pltrx, mrsd2, 'b^-',
        #    pltlx, plsdt, 'ro-', pltlx, mlsdt, 'ro-', pltrx, prsdt, 'bo-', pltrx, mrsdt, 'bo-', # t SD
        #    pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
        #    pltlbsx, pltlbs, 'ro', pltlbex, pltlbe, 'r^', pltrbsx, pltrbs, 'bo', pltrbex, pltrbe, 'b^' # start & end of blinks
        #)
        plt.plot(pltlx, lDiff, 'ro-',
            pltax, [0 for x in xrange(len(pltax))], 'g--', # zero
            pltlx, la, 'r--', # average
            #pltlx, plsd1, 'r^-', pltlx, mlsd1, 'r^-', pltrx, prsd1, 'b^-', pltrx, mrsd1, 'b^-',
            #pltlx, plsd2, 'r^-', pltlx, mlsd2, 'r^-', pltrx, prsd2, 'b^-', pltrx, mrsd2, 'b^-',
            pltlx, plsdt, 'yo-', pltlx, mlsdt, 'yo-', # t SD
            pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
            pltlbsx, pltlbs, 'ro', pltlbex, pltlbe, 'r^', # start & end of blinks
        )
        plt.tight_layout()
        plt.figure(2)
        plt.plot(pltrx, rDiff, 'bo-',
            pltax, [0 for x in xrange(len(pltax))], 'g--', # zero
            pltrx, ra, 'b--', # average
            #pltlx, plsd1, 'r^-', pltlx, mlsd1, 'r^-', pltrx, prsd1, 'b^-', pltrx, mrsd1, 'b^-',
            #pltlx, plsd2, 'r^-', pltlx, mlsd2, 'r^-', pltrx, prsd2, 'b^-', pltrx, mrsd2, 'b^-',
            pltrx, prsdt, 'yo-', pltrx, mrsdt, 'yo-', # t SD
            pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
            pltrbsx, pltrbs, 'bo', pltrbex, pltrbe, 'b^' # start & end of blinks
        )
        plt.tight_layout()
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

