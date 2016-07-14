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
            pass # not using it
            # statusInfo = [x for x in output.split(" ") if x != ""]

            # fn     = int(statusInfo[statusInfo.index("F")+1])
            # ts     = float(statusInfo[statusInfo.index("T")+1])
            # if statusInfo.count("status") == 1:
            #     status = statusInfo[statusInfo.index("status")+1]

            #     if status == "start":
            #         if len(tracking["detecting"]) > 0:
            #             if len(tracking["detecting"][-1]) != 2:
            #                 print "error: tracking start: previous entry is not finished yet %s (%s)" % (repr(tracking["detecting"][-1]), statusInfo)
            #         tracking["detecting"].append([(status, fn, ts)])
            #     elif status == "stop":
            #         if len(tracking["detecting"]) > 0:
            #             if len(tracking["detecting"][-1]) == 1:
            #                 tracking["detecting"][-1].append((status, fn, ts))
            #             else:
            #                 print "error: tracking stop: detecting[-1] is not len of 1 %s (%s)" % (repr(tracking["detecting"][-1]), statusInfo)
            #         else:
            #             print "error: tracking stop: len(detecting) is zero (%s)" % statusInfo
            #     else:
            #         print "error: unknown tracking status (%s)" % statusInfo
            # else:
            #     pass
            #     #print statusInfo
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
        elif output.startswith("debug_fb_log_pupil_coverage:"):
            flowsInfo = [x for x in output.split(" ") if x != ""]
            fn   = int(flowsInfo[flowsInfo.index("F")+1])
            ts   = float(flowsInfo[flowsInfo.index("T")+1])
            lDiff, rDiff = int(flowsInfo[flowsInfo.index("L")+1]), int(flowsInfo[flowsInfo.index("R")+1])
            tracking["pupilDisplacement"].append({"fn":fn, "ts":ts, "lDiff":lDiff, "rDiff":rDiff})
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
            try:
                fFlows[fFlowsI[fs]][eye+"b"] = "s"
                fFlows[fFlowsI[fe]][eye+"b"] = "e"
            except:
                print "not graphing blink %s %d-%d" % (eye, fs, fe)
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
            jBlinks.append(blinkInfoDict)
            try:
                fFlows[fFlowsI[fs]]["jb"] = "s"
                fFlows[fFlowsI[fe]]["jb"] = "e"
            except:
                print "not graphing blink j %d-%d" % (fs, fe)
        elif output.startswith("exiting"):
            return True
        return False

    @staticmethod
    def processPupilDisplacement(tracking, dc, annotsl, annots):
        lDiff, rDiff = [x["lDiff"] for x in tracking["pupilDisplacement"]], [x["rDiff"] for x in tracking["pupilDisplacement"]]

        annotsD = Cmn._annotsById(annotsl)
        fnLDiff, fnRDiff = {}, {}
        for e in tracking["pupilDisplacement"]:
            fnLDiff[e["fn"]] = e["lDiff"]
            fnRDiff[e["fn"]] = e["rDiff"]

        lbCaught, rbCaught, lMissed, rMissed = [], [], [], []
        for diff, resList, checkRefs in [(fnLDiff, lbCaught, dc["bCaught"]), (fnRDiff, rbCaught, dc["bCaught"]),
                                        (fnLDiff, lMissed, dc["lMissed"]), (fnRDiff, rMissed, dc["rMissed"]), ]:
            for checkRef in checkRefs:
                bs, be = annotsD[checkRef]["bs"], annotsD[checkRef]["be"]
                s = sum(diff[c] for c in xrange(bs, be+1) if diff.has_key(c))/float(be-bs)
                resList.append((checkRef, s, (bs, be)))

        fpByOnlyL, fpByOnlyR = [], []
        for diff, resList, checkRefs in [(fnLDiff, fpByOnlyL, dc["fpByOnlyL"]), (fnRDiff, fpByOnlyR, dc["fpByOnlyR"]), ]:
            for checkRef in checkRefs:
                bs, be = checkRef[1]["fs"], checkRef[1]["fe"]
                s = sum(diff[c] for c in xrange(bs, be+1) if diff.has_key(c))/float(be-bs)
                resList.append((checkRef, s, (bs, be)))

        fpByBothEyesLR = []
        for resList, checkRefs in [(fpByBothEyesLR, dc["fpByBothEyes"]), ]:
            for checkRef in checkRefs:
                ls, rs = 0, 0
                l, r = checkRef[0], checkRef[1]
                lbs, lbe, rbs, rbe = l[1]["fs"], l[1]["fe"], r[1]["fs"], r[1]["fe"]

                ls = sum(fnLDiff[c] for c in xrange(lbs, lbe+1) if fnLDiff.has_key(c))/float(lbe-lbs)
                rs = sum(fnRDiff[c] for c in xrange(rbs, rbe+1) if fnRDiff.has_key(c))/float(rbe-rbs)
                resList.append((checkRef, ls, rs, (lbs, lbe), (rbs, rbe)))

        lMissedByDisplacement = sorted([x[0] for x in lMissed if x[1] > 13])
        rMissedByDisplacement = sorted([x[0] for x in rMissed if x[1] > 13])
        bMissedByDisplacement = sorted(list(set([x[0] for x in lMissed if x[1] > 13]
                                               +[x[0] for x in rMissed if x[1] > 13])))

        lOnlyFpByDisplacement = sorted([x for x in fpByOnlyL], key=lambda x:x[1])
        rOnlyFpByDisplacement = sorted([x for x in fpByOnlyR], key=lambda x:x[1])
        bothFpByDisplacement = sorted(fpByBothEyesLR, key=lambda y:(y[1]+y[2]))

        lOutliers = [(x["fn"], x["lDiff"]) for x in tracking["pupilDisplacement"] if x["lDiff"] > 12]
        rOutliers = [(x["fn"], x["rDiff"]) for x in tracking["pupilDisplacement"] if x["rDiff"] > 12]
        lPercent = len(lOutliers)/float(len(tracking["pupilDisplacement"]))*100
        rPercent = len(rOutliers)/float(len(tracking["pupilDisplacement"]))*100

        return {
            "lMissed":lMissed, "rMissed":rMissed,

            "lMissedByDisplacement":lMissedByDisplacement, "rMissedByDisplacement":rMissedByDisplacement,
                "bMissedByDisplacement":bMissedByDisplacement,

            "lOnlyFpByDisplacement":lOnlyFpByDisplacement, "rOnlyFpByDisplacement":rOnlyFpByDisplacement,
            "bothFpByDisplacement":bothFpByDisplacement,

            "lOutliers":lOutliers, "rOutliers":rOutliers, "lPercent":lPercent, "rPercent":rPercent,
        }
    @staticmethod
    def displayPupilDisplacement(ppd):
        d = [
            "percent",
            "missed",
            "missedByDisplacement",
            "fps"
        ]
        if "percent" in d:
            print "lPercent %.2f rPercent %.2f" % (ppd["lPercent"], ppd["rPercent"])
        if "missed" in d:
            # bID, displacementPerFrame, (fs, fe)
            print "lMissed"
            print "\n".join(["%d %.2f (%d, %d)" % (x[0], x[1], x[2][0], x[2][1]) for x in sorted(ppd["lMissed"], key=lambda x:x[1])])
            print "rMissed"
            print "\n".join(["%d %.2f (%d, %d)" % (x[0], x[1], x[2][0], x[2][1]) for x in sorted(ppd["rMissed"], key=lambda x:x[1])])
        if "missedByDisplacement" in d:
            print "lMissedByDisplacement: %d %s" % (len(ppd["lMissedByDisplacement"]), ppd["lMissedByDisplacement"])
            print "rMissedByDisplacement: %d %s" % (len(ppd["rMissedByDisplacement"]), ppd["rMissedByDisplacement"])
            print "bMissedByDisplacement: %d %s" % (len(ppd["bMissedByDisplacement"]), ppd["bMissedByDisplacement"])
        if "fps" in d:
            print "lOnlyFpByDisplacement"
            print "\n".join(["%.2f (%d, %d)" % (x[1], x[2][0], x[2][1]) for x in ppd["lOnlyFpByDisplacement"]])
            print "rOnlyFpByDisplacement"
            print "\n".join(["%.2f (%d, %d)" % (x[1], x[2][0], x[2][1]) for x in ppd["rOnlyFpByDisplacement"]])
            print "bothFpByDisplacement"
            print "\n".join(["%.2f %.2f (%d, %d) (%d, %d)" % (x[1], x[2], x[3][0], x[3][1], x[4][0], x[4][1]) for x in ppd["bothFpByDisplacement"]])
        return

    @staticmethod
    def postProcessTracking(tracking, fFlows, dc):
        lm, rm = dc["lMissed"], dc["rMissed"]
        pltx = [x["fn"] for x in tracking["pupilDisplacement"]]
        pltasx = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s"]
        pltaex = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e"]
        pltas = [70 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
        pltae = [70 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "e"]
        pltasxlm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in lm]
        pltaexlm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in lm]
        pltaslm = [67 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in lm]
        pltaelm = [67 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in lm]
        pltasxrm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in rm]
        pltaexrm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in rm]
        pltasrm = [65 for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in rm]
        pltaerm = [65 for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in rm]
        lDiff, rDiff = [x["lDiff"] for x in tracking["pupilDisplacement"]], [x["rDiff"] for x in tracking["pupilDisplacement"]]
        plt.plot(
            pltx, lDiff, 'ro-', pltx, rDiff, 'bo-',
            pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
            pltasxlm, pltaslm, 'ro', pltaexlm, pltaelm, 'r^', # left missed
            pltasxrm, pltasrm, 'bo', pltaexrm, pltaerm, 'b^', # right missed
        )
        plt.tight_layout()
        plt.show()
        return
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
        pltjbsx = [x["fn"] for x in fFlows[-window:] if  x.has_key("jb") and x["jb"] == "s"]
        pltjbex = [x["fn"] for x in fFlows[-window:] if  x.has_key("jb") and x["jb"] == "e"]
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
        pltas = [1.4 for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
        pltae = [1.4 for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "e"]
        pltjbs = [1.3 for x in fFlows[-window:]  if x.has_key("jb") and x["jb"] == "s"]
        pltjbe = [1.3 for x in fFlows[-window:]  if x.has_key("jb") and x["jb"] == "e"]
        pltlbs = [1.2 for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "s"]
        pltlbe = [1.2 for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "e"]
        pltrbs = [1.1 for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "s"]
        pltrbe = [1.1 for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "e"]
        #plt.subplot(211)
        #plt.plot(pltx, pltlXdiff, 'ro-', pltx, pltrXdiff, 'bo-')
        fig = [3]
        #plt.subplot(212)
        if 3 in fig:
            plt.plot(
                pltlx, lDiff, 'ro-', pltrx, rDiff, 'bo-',
                pltax, [0 for x in xrange(len(pltax))], 'g--', # zero
                #pltlx, la, 'r--', pltrx, ra, 'b--', # average
                #pltlx, plsd1, 'r^-', pltlx, mlsd1, 'r^-', pltrx, prsd1, 'b^-', pltrx, mrsd1, 'b^-',
                #pltlx, plsd2, 'r^-', pltlx, mlsd2, 'r^-', pltrx, prsd2, 'b^-', pltrx, mrsd2, 'b^-',
                pltlx, plsdt, 'ro-', pltlx, mlsdt, 'ro-', pltrx, prsdt, 'bo-', pltrx, mrsdt, 'bo-', # t SD
                pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
                pltlbsx, pltlbs, 'ro', pltlbex, pltlbe, 'r^', # start & end of lBlinks
                pltrbsx, pltrbs, 'bo', pltrbex, pltrbe, 'b^', # start & end of rBlinks
                pltjbsx, pltjbs, 'yo', pltjbex, pltjbe, 'y^', # start & end of jBlinks
            )
            plt.tight_layout()
        if 1 in fig:
            plt.figure(1)
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
        if 2 in fig:
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

