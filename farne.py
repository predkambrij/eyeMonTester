from multiprocessing import Process

import matplotlib
font = {
    #'family' : 'normal',
    #'weight' : 'bold',
    'size'   : 26,
}
matplotlib.rc('font', **font)
#matplotlib.rcParams['xtick.major.pad']='80'
#matplotlib.rcParams['ytick.major.pad']='80'
#print matplotlib.rcParams.keys()
#matplotlib.rcParams['savefig.pad_inches']='800'
#matplotlib.rcParams['ytick.major.pad']='80'
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
            Farne.postProcessLogLine(fFlows, lBlinks, rBlinks, jBlinks, False)
        elif output.startswith("debug_fb_log_pupil_coverage:"):
            flowsInfo = [x for x in output.split(" ") if x != ""]
            fn   = int(flowsInfo[flowsInfo.index("F")+1])
            ts   = float(flowsInfo[flowsInfo.index("T")+1])
            lDiff, rDiff = int(flowsInfo[flowsInfo.index("L")+1]), int(flowsInfo[flowsInfo.index("R")+1])
            tracking["pupilDisplacement"].append({"fn":fn, "ts":ts, "lDiff":lDiff, "rDiff":rDiff})
        elif output.startswith("debug_fb_log_upperlowerdiff:"):
            flowsInfo = [x for x in output.split(" ") if x != ""]
            fn   = int(flowsInfo[flowsInfo.index("F")+1])
            ts   = float(flowsInfo[flowsInfo.index("T")+1])

            if flowsInfo.count("L") == 1:
                l = float(flowsInfo[flowsInfo.index("L")+1])
                tracking["upperLowerL"].append({"fn":fn, "ts":ts, "l":l})
            if flowsInfo.count("R") == 1:
                r = float(flowsInfo[flowsInfo.index("R")+1])
                tracking["upperLowerR"].append({"fn":fn, "ts":ts, "r":r})
        elif output.startswith("debug_notifications_n1_log1:"):
            # debug_notifications_n1_log1: min ratio:%.2f curRatio %.2f
            #print output
            words = output.split(" ")
            if len(words) < 4 or words[3] != "minRatio":
                return False
            fn       = int(words[words.index("fn")+1])
            curRatio = float(words[words.index("curRatio")+1])
            bLen = float(words[words.index("bLen")+1])
            try:
                fFlows[fFlowsI[fn-1]]["cr"] = curRatio
            except:
                print "not graphing curRatio %d" % fn
            try:
                fFlows[fFlowsI[fn-1]]["bLen"] = bLen
            except:
                print "not graphing bLen %d" % fn
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
                s = sum(diff[c] for c in xrange(bs, be+1) if diff.has_key(c))/(float(be-bs) if (be-bs) > 0 else 1)
                resList.append((checkRef, s, (bs, be)))

        fpByOnlyL, fpByOnlyR = [], []
        for diff, resList, checkRefs in [(fnLDiff, fpByOnlyL, dc["fpByOnlyL"]), (fnRDiff, fpByOnlyR, dc["fpByOnlyR"]), ]:
            for checkRef in checkRefs:
                bs, be = checkRef[1]["fs"], checkRef[1]["fe"]
                s = sum(diff[c] for c in xrange(bs, be+1) if diff.has_key(c))/(float(be-bs) if (be-bs) > 0 else 1)
                resList.append((checkRef, s, (bs, be)))

        fpByBothEyesLR = []
        for resList, checkRefs in [(fpByBothEyesLR, dc["fpByBothEyes"]), ]:
            for checkRef in checkRefs:
                ls, rs = 0, 0
                l, r = checkRef[0], checkRef[1]
                lbs, lbe, rbs, rbe = l[1]["fs"], l[1]["fe"], r[1]["fs"], r[1]["fe"]

                ls = sum(fnLDiff[c] for c in xrange(lbs, lbe+1) if fnLDiff.has_key(c))/(float(lbe-lbs) if (lbe-lbs) > 0 else 1)
                rs = sum(fnRDiff[c] for c in xrange(rbs, rbe+1) if fnRDiff.has_key(c))/(float(rbe-rbs) if (rbe-rbs) > 0 else 1)
                resList.append((checkRef, ls, rs, (lbs, lbe), (rbs, rbe)))

        lMissedByDisplacement = sorted([x[0] for x in lMissed if x[1] > 13])
        rMissedByDisplacement = sorted([x[0] for x in rMissed if x[1] > 13])
        aMissedByDisplacement = sorted(list(set([x[0] for x in lMissed if x[1] > 13]+[x[0] for x in rMissed if x[1] > 13])))
        bMissedByDisplacement = sorted(list(set.intersection(*[set([x[0] for x in lMissed if x[1] > 13]), set([x[0] for x in rMissed if x[1] > 13])])))
        loMissedByDisplacement = [x for x in lMissedByDisplacement if x not in bMissedByDisplacement]
        roMissedByDisplacement = [x for x in rMissedByDisplacement if x not in bMissedByDisplacement]

        lOnlyFpByDisplacement = sorted([x for x in fpByOnlyL], key=lambda x:x[1])
        rOnlyFpByDisplacement = sorted([x for x in fpByOnlyR], key=lambda x:x[1])
        bothFpByDisplacement = sorted(fpByBothEyesLR, key=lambda y:(y[1]+y[2]))

        lOutliers = [(x["fn"], x["lDiff"]) for x in tracking["pupilDisplacement"] if x["lDiff"] > 12]
        rOutliers = [(x["fn"], x["rDiff"]) for x in tracking["pupilDisplacement"] if x["rDiff"] > 12]

        lPercent = (len(lOutliers)/float(len(tracking["pupilDisplacement"]))*100) if len(tracking["pupilDisplacement"]) >0 else -1
        rPercent = (len(rOutliers)/float(len(tracking["pupilDisplacement"]))*100) if len(tracking["pupilDisplacement"]) >0 else -1

        return {
            "lMissed":lMissed, "rMissed":rMissed,

            "lMissedByDisplacement":lMissedByDisplacement, "rMissedByDisplacement":rMissedByDisplacement,
            "loMissedByDisplacement":loMissedByDisplacement, "roMissedByDisplacement":roMissedByDisplacement,
            "bMissedByDisplacement":bMissedByDisplacement, "aMissedByDisplacement":aMissedByDisplacement,

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
            print "loMissedByDisplacement: %d %s" % (len(ppd["loMissedByDisplacement"]), ppd["loMissedByDisplacement"])
            print "roMissedByDisplacement: %d %s" % (len(ppd["roMissedByDisplacement"]), ppd["roMissedByDisplacement"])
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
    def postProcessLogLine(fFlows, lBlinks, rBlinks, jBlinks, isEnd, dc=None, tracking=None, videoName=None, figparms=None):
        #print videoName
        #print repr(figparms)
        #figsize = (5.314961, 5.314961)
        cm13_5 = 5.314961
        figsizeW = cm13_5*4
        figsizeH = figsizeW/2.
        imgDpi = 150
        tightLayoutPad = 0.2
        figsize = (figsizeW, figsizeH)
        if not isEnd:
            window = 1000
        else:
            window = 0

        if not isEnd and (len(fFlows) == 0 or len(fFlows) % window != 0):
            return

        if isEnd:
            window = 0

        showLegend = True
        if figparms != None and figparms.has_key('disableLegend') == True and figparms['disableLegend'] == True:
            showLegend = False
        if figparms != None and figparms.has_key('graphs') == True:
            options = figparms['graphs']
        else:
            options = [
                "postProcessBlinkRate",
                #"postProcessUpperLower",
                #"postProcessTracking",
                #"postProcessLogLine",
            ]
        if "postProcessBlinkRate" in options and isEnd == True:
            blinkRatioX = [x["fn"] for x in fFlows[-window:] if x.has_key("cr")]
            blinkRatio = [x["cr"] for x in fFlows[-window:] if x.has_key("cr")]
            bLen = [x["bLen"] for x in fFlows[-window:] if x.has_key("bLen")]

            plt.figure(22, figsize=figsize)
            plt.plot(blinkRatioX, blinkRatio, 'ro-', label=u"Frekvenca me\u017eikanja", markeredgecolor='none')
            plt.tight_layout(pad=tightLayoutPad)
            plt.figure(23, figsize=figsize)
            plt.plot(blinkRatioX, bLen, 'ro-', label=u"Dol\u017eina me\u017eikov", markeredgecolor='none')
            plt.tight_layout(pad=tightLayoutPad)

        elif "postProcessUpperLower" in options and isEnd == True:
            # missed
            lm, rm = dc["lMissed"], dc["rMissed"]
            lfpfs, lfpfe = [x[1]["fs"] for x in dc["lFp"]], [x[1]["fe"] for x in dc["lFp"]]
            rfpfs, rfpfe = [x[1]["fs"] for x in dc["rFp"]], [x[1]["fe"] for x in dc["rFp"]]
            bfpfs, bfpfe = [min(x[0][1]["fs"], x[1][1]["fs"]) for x in dc["fpByBothEyes"]], [max(x[0][1]["fe"], x[1][1]["fe"]) for x in dc["fpByBothEyes"]]

            pltasxlm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in lm]
            pltaexlm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in lm]
            pltaslm = [1.88 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in lm]
            pltaelm = [1.88 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in lm]
            pltasxrm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in rm]
            pltaexrm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in rm]
            pltasrm = [1.8 for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in rm]
            pltaerm = [1.8 for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in rm]

            #fps
            lfpfs, lfpfe = [x[1]["fs"] for x in dc["lFp"]], [x[1]["fe"] for x in dc["lFp"]]
            rfpfs, rfpfe = [x[1]["fs"] for x in dc["rFp"]], [x[1]["fe"] for x in dc["rFp"]]
            bfpfs, bfpfe = [min(x[0][1]["fs"], x[1][1]["fs"]) for x in dc["fpByBothEyes"]], [max(x[0][1]["fe"], x[1][1]["fe"]) for x in dc["fpByBothEyes"]]

            pltjbsx = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "s" and x["fn"] in bfpfs]
            pltjbex = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "e" and x["fn"] in bfpfe]
            pltlbsx = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "s" and x["fn"] in lfpfs]
            pltlbex = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "e" and x["fn"] in lfpfe]
            pltrbsx = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "s" and x["fn"] in rfpfs]
            pltrbex = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "e" and x["fn"] in rfpfe]
            pltjbs = [2.3 for x in fFlows if x.has_key("jb") and x["jb"] == "s" and x["fn"] in bfpfs]
            pltjbe = [2.3 for x in fFlows if x.has_key("jb") and x["jb"] == "e" and x["fn"] in bfpfe]
            pltlbs = [2.22 for x in fFlows if x.has_key("lb") and x["lb"] == "s" and x["fn"] in lfpfs]
            pltlbe = [2.22 for x in fFlows if x.has_key("lb") and x["lb"] == "e" and x["fn"] in lfpfe]
            pltrbs = [2.14 for x in fFlows if x.has_key("rb") and x["rb"] == "s" and x["fn"] in rfpfs]
            pltrbe = [2.14 for x in fFlows if x.has_key("rb") and x["rb"] == "e" and x["fn"] in rfpfe]
            # not fps
            # pltjbsxn = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "s" and (not x["fn"] in bfpfs)]
            # pltjbexn = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "e" and (not x["fn"] in bfpfe)]
            # pltlbsxn = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "s" and (not x["fn"] in lfpfs)]
            # pltlbexn = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "e" and (not x["fn"] in lfpfe)]
            # pltrbsxn = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "s" and (not x["fn"] in rfpfs)]
            # pltrbexn = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "e" and (not x["fn"] in rfpfe)]
            # pltjbsn = [1.3 for x in fFlows if x.has_key("jb") and x["jb"] == "s" and (not x["fn"] in bfpfs)]
            # pltjben = [1.3 for x in fFlows if x.has_key("jb") and x["jb"] == "e" and (not x["fn"] in bfpfe)]
            # pltlbsn = [1.25 for x in fFlows if x.has_key("lb") and x["lb"] == "s" and (not x["fn"] in lfpfs)]
            # pltlben = [1.25 for x in fFlows if x.has_key("lb") and x["lb"] == "e" and (not x["fn"] in lfpfe)]
            # pltrbsn = [1.2 for x in fFlows if x.has_key("rb") and x["rb"] == "s" and (not x["fn"] in rfpfs)]
            # pltrben = [1.2 for x in fFlows if x.has_key("rb") and x["rb"] == "e" and (not x["fn"] in rfpfe)]
            # annots
            pltasx = [x["fn"] for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
            pltaex = [x["fn"] for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "e"]
            pltas = [2.4 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
            pltae = [2.4 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "e"]

            pltlx, pltrx = [x["fn"] for x in tracking["upperLowerL"]], [x["fn"] for x in tracking["upperLowerR"]]
            pltl, pltr = [abs(x["l"]) for x in tracking["upperLowerL"]], [abs(x["r"]) for x in tracking["upperLowerR"]]

            fig = plt.figure(1, figsize=figsize)
            plt.plot(pltlx, pltl, 'ro-', pltrx, pltr, 'bo-', markeredgecolor='none')

            anots1 = plt.plot(pltasx, pltas, 'go', markersize=15.0)
            anots2 = plt.plot(pltaex, pltae, 'g^', markersize=15.0) # annots of blinks

            left1   = plt.plot(pltlbsx, pltlbs, 'ro', markersize=15.0)
            left2   = plt.plot(pltlbex, pltlbe, 'r^', markersize=15.0) # start & end of lBlinks not fp
            right1  = plt.plot(pltrbsx, pltrbs, 'bo', markersize=15.0)
            right2  = plt.plot(pltrbex, pltrbe, 'b^', markersize=15.0) # start & end of rBlinks not fp
            both1   = plt.plot(pltjbsx, pltjbs, 'yo', markersize=15.0)
            both2   = plt.plot(pltjbex, pltjbe, 'y^', markersize=15.0) # start & end of jBlinks not fp
            mleft1  = plt.plot(pltasxlm, pltaslm, 'ro', markersize=15.0)
            mleft2  = plt.plot(pltaexlm, pltaelm, 'r^', markersize=15.0) # left missed
            mright1 = plt.plot(pltasxrm, pltasrm, 'bo', markersize=15.0)
            mright2 = plt.plot(pltaexrm, pltaerm, 'b^', markersize=15.0) # right missed
                #pltlbsxn, pltlbsn, 'ro', pltlbexn, pltlben, 'r^', # start & end of lBlinks fp
                #pltrbsxn, pltrbsn, 'bo', pltrbexn, pltrben, 'b^', # start & end of rBlinks fp
                #pltjbsxn, pltjbsn, 'yo', pltjbexn, pltjben, 'y^', # start & end of jBlinks fp


            if figparms != None and figparms.has_key('axis') == True:
                plt.axis(
                    xmin=figparms['axis']['xmin'], xmax=figparms['axis']['xmax'],
                    ymin=figparms['axis']['ymin'], ymax=figparms['axis']['ymax']
                )

            ls = [anots1, both1, left1, right1, anots2, both2, left2, right2]
            labs = ["", "", "", "",
                u"anotirani me\u017eiki",
                u"obe o\u010desi: napa\u010dno zaznani (nad 2)",
                u"levo oko:    napa\u010dno zaznani (nad 2) / zgre\u0161eni (pod 2)",
                u"desno oko: napa\u010dno zaznani (nad 2) / zgre\u0161eni (pod 2)",
            ]
            if showLegend == True:
                first_legend = plt.legend(ls, labs, ncol=2, numpoints=1, loc=figparms['legBpos'])
                plt.gca().add_artist(first_legend)
                plt.legend(['levo oko', 'desno oko'], loc=figparms['legLpos'])

            plt.xlabel(u'sli\u010dice', fontsize=30)
            plt.ylabel(u'razlika med zg. in sp. delom obmo\u010dja o\u010di', fontsize=30)
            plt.tight_layout(pad=tightLayoutPad)
            if figparms != None and figparms.has_key('figName') == True:
                plt.savefig('/home/developer/other/notes/m/%s.png' % figparms['figName'], dpi=imgDpi, pad_inches=1)

        if "postProcessTracking" in options and isEnd == True:
            #print [x[1] for x in dc["fpByBothEyes"]]
            #return
            lm, rm = dc["lMissed"], dc["rMissed"]
            #lfp, rfp = dc["lFp"], dc["rFp"]
            lfpfs, lfpfe = [x[1]["fs"] for x in dc["lFp"]], [x[1]["fe"] for x in dc["lFp"]]
            rfpfs, rfpfe = [x[1]["fs"] for x in dc["rFp"]], [x[1]["fe"] for x in dc["rFp"]]
            bfpfs, bfpfe = [min(x[0][1]["fs"], x[1][1]["fs"]) for x in dc["fpByBothEyes"]], [max(x[0][1]["fe"], x[1][1]["fe"]) for x in dc["fpByBothEyes"]]
            #print [x[1]["fs"] for x in dc["lFp"]]
            #return
            #print  [x for x in fFlows if x.has_key("rb") and x["rb"] == "e"]
            #return
            # annots
            pltasx = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s"]
            pltaex = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e"]
            pltas = [74 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
            pltae = [74 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "e"]
            # missed
            pltasxlm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in lm]
            pltaexlm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in lm]
            pltaslm = [70 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in lm]
            pltaelm = [70 for x in fFlows  if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in lm]
            pltasxrm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in rm]
            pltaexrm = [x["fn"] for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in rm]
            pltasrm = [66 for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "s" and x["bi"] in rm]
            pltaerm = [66 for x in fFlows if x.has_key("annotEvent") and x["annotEvent"] == "e" and x["bi"] in rm]
            #fps
            pltjbsx = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "s" and x["fn"] in bfpfs]
            pltjbex = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "e" and x["fn"] in bfpfe]
            pltlbsx = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "s" and x["fn"] in lfpfs]
            pltlbex = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "e" and x["fn"] in lfpfe]
            pltrbsx = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "s" and x["fn"] in rfpfs]
            pltrbex = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "e" and x["fn"] in rfpfe]
            pltjbs = [34 for x in fFlows if x.has_key("jb") and x["jb"] == "s" and x["fn"] in bfpfs]
            pltjbe = [34 for x in fFlows if x.has_key("jb") and x["jb"] == "e" and x["fn"] in bfpfe]
            pltlbs = [30 for x in fFlows if x.has_key("lb") and x["lb"] == "s" and x["fn"] in lfpfs]
            pltlbe = [30 for x in fFlows if x.has_key("lb") and x["lb"] == "e" and x["fn"] in lfpfe]
            pltrbs = [26 for x in fFlows if x.has_key("rb") and x["rb"] == "s" and x["fn"] in rfpfs]
            pltrbe = [26 for x in fFlows if x.has_key("rb") and x["rb"] == "e" and x["fn"] in rfpfe]

            pltx = [x["fn"] for x in tracking["pupilDisplacement"]]
            lDiff, rDiff = [x["lDiff"] for x in tracking["pupilDisplacement"]], [x["rDiff"] for x in tracking["pupilDisplacement"]]


            plt.figure(2, figsize=figsize)
            plt.plot(pltx, lDiff, 'ro-', pltx, rDiff, 'bo-', markeredgecolor='none')
            anots1 = plt.plot(pltasx, pltas, 'go', markersize=15.0) # annots of blinks
            anots2 = plt.plot(pltaex, pltae, 'g^', markersize=15.0) # annots of blinks
            mleft1 = plt.plot(pltasxlm, pltaslm, 'ro', markersize=15.0) # left missed
            mleft2 = plt.plot(pltaexlm, pltaelm, 'r^', markersize=15.0) # left missed
            mright1 = plt.plot(pltasxrm, pltasrm, 'bo', markersize=15.0) # right missed
            mright2 = plt.plot(pltaexrm, pltaerm, 'b^', markersize=15.0) # right missed
            fboth1 = plt.plot(pltjbsx, pltjbs, 'yo', markersize=15.0) # both fp
            fboth2 = plt.plot(pltjbex, pltjbe, 'y^', markersize=15.0) # both fp
            fleft1 = plt.plot(pltlbsx, pltlbs, 'ro', markersize=15.0) # left fp
            fleft2 = plt.plot(pltlbex, pltlbe, 'r^', markersize=15.0) # left fp
            fright1 = plt.plot(pltrbsx, pltrbs, 'bo', markersize=15.0) # right fp
            fright2 = plt.plot(pltrbex, pltrbe, 'b^', markersize=15.0) # right fp

            if figparms != None and figparms.has_key('axis') == True:
                plt.axis(
                    xmin=figparms['axis']['xmin'], xmax=figparms['axis']['xmax'],
                    ymin=figparms['axis']['ymin'], ymax=figparms['axis']['ymax']
                )

            plt.xlabel(u'sli\u010dice', fontsize=30)
            plt.ylabel(u'razlika lokacije zenice od dejanske', fontsize=30)
            ls = [anots1, mleft1, mright1, fboth1, anots2, mleft2, mright2, fboth2]
            labs = ["", "", "", "",
                u"anotirani me\u017eiki",
                u"levo oko:    napa\u010dno zaznani (okrog 30) / zgre\u0161eni (okrog 70)",
                u"desno oko: napa\u010dno zaznani (okrog 30) / zgre\u0161eni (okrog 70)",
                u"obe o\u010desi: napa\u010dno zaznani (okrog 30)"
            ]
            if showLegend == True:
                first_legend = plt.legend(ls, labs, ncol=2, numpoints=1, loc=figparms['legBpos'])
                plt.gca().add_artist(first_legend)
                plt.legend(['levo oko', 'desno oko'], loc=figparms['legLpos'])

            plt.tight_layout(pad=tightLayoutPad)

            if figparms != None and figparms.has_key('figName') == True:
                plt.savefig('/home/developer/other/notes/m/%s.png' % figparms['figName'], dpi=imgDpi, pad_inches=1)

        if "postProcessLogLine" in options:
            aVals = 1.4 if not figparms.has_key('aVals') else figparms['aVals']
            jVals = 1.3 if not figparms.has_key('jVals') else figparms['jVals']
            lVals = 1.25 if not figparms.has_key('lVals') else figparms['lVals']
            rVals = 1.2 if not figparms.has_key('rVals') else figparms['rVals']
            if dc != None:
                lfpfs, lfpfe = [x[1]["fs"] for x in dc["lFp"]], [x[1]["fe"] for x in dc["lFp"]]
                rfpfs, rfpfe = [x[1]["fs"] for x in dc["rFp"]], [x[1]["fe"] for x in dc["rFp"]]
                bfpfs, bfpfe = [min(x[0][1]["fs"], x[1][1]["fs"]) for x in dc["fpByBothEyes"]], [max(x[0][1]["fe"], x[1][1]["fe"]) for x in dc["fpByBothEyes"]]
                #fps
                pltjbsx = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "s" and x["fn"] in bfpfs]
                pltjbex = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "e" and x["fn"] in bfpfe]
                pltlbsx = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "s" and x["fn"] in lfpfs]
                pltlbex = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "e" and x["fn"] in lfpfe]
                pltrbsx = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "s" and x["fn"] in rfpfs]
                pltrbex = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "e" and x["fn"] in rfpfe]
                pltjbs = [1.15 for x in fFlows if x.has_key("jb") and x["jb"] == "s" and x["fn"] in bfpfs]
                pltjbe = [1.15 for x in fFlows if x.has_key("jb") and x["jb"] == "e" and x["fn"] in bfpfe]
                pltlbs = [1.10 for x in fFlows if x.has_key("lb") and x["lb"] == "s" and x["fn"] in lfpfs]
                pltlbe = [1.10 for x in fFlows if x.has_key("lb") and x["lb"] == "e" and x["fn"] in lfpfe]
                pltrbs = [1.05 for x in fFlows if x.has_key("rb") and x["rb"] == "s" and x["fn"] in rfpfs]
                pltrbe = [1.05 for x in fFlows if x.has_key("rb") and x["rb"] == "e" and x["fn"] in rfpfe]
                # not fps
                pltjbsxn = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "s" and (not x["fn"] in bfpfs)]
                pltjbexn = [x["fn"] for x in fFlows if  x.has_key("jb") and x["jb"] == "e" and (not x["fn"] in bfpfe)]
                pltlbsxn = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "s" and (not x["fn"] in lfpfs)]
                pltlbexn = [x["fn"] for x in fFlows if x.has_key("lb") and x["lb"] == "e" and (not x["fn"] in lfpfe)]
                pltrbsxn = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "s" and (not x["fn"] in rfpfs)]
                pltrbexn = [x["fn"] for x in fFlows if x.has_key("rb") and x["rb"] == "e" and (not x["fn"] in rfpfe)]
                pltjbsn = [jVals for x in fFlows if x.has_key("jb") and x["jb"] == "s" and (not x["fn"] in bfpfs)]
                pltjben = [jVals for x in fFlows if x.has_key("jb") and x["jb"] == "e" and (not x["fn"] in bfpfe)]
                pltlbsn = [lVals for x in fFlows if x.has_key("lb") and x["lb"] == "s" and (not x["fn"] in lfpfs)]
                pltlben = [lVals for x in fFlows if x.has_key("lb") and x["lb"] == "e" and (not x["fn"] in lfpfe)]
                pltrbsn = [rVals for x in fFlows if x.has_key("rb") and x["rb"] == "s" and (not x["fn"] in rfpfs)]
                pltrben = [rVals for x in fFlows if x.has_key("rb") and x["rb"] == "e" and (not x["fn"] in rfpfe)]

            pltax = [x["fn"] for x in fFlows[-window:]]
            pltlx = [x["fn"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
            pltrx = [x["fn"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
            lDiff, rDiff = [x["lDiff"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["rDiff"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
            la, ra = [x["la"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["ra"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
            plsd1, mlsd1 = [x["plsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["mlsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
            plsd2, mlsd2 = [x["plsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["mlsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
            plsdt, mlsdt = [x["plsdt"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"], [x["mlsdt"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "l"]
            prsd1, mrsd1 = [x["prsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"], [x["mrsd1"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
            prsd2, mrsd2 = [x["prsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"], [x["mrsd2"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
            prsdt, mrsdt = [x["prsdt"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"], [x["mrsdt"] for x in fFlows[-window:] if x["type"] == "b" or x["type"] == "r"]
            pltasx = [x["fn"] for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
            pltaex = [x["fn"] for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "e"]
            pltas = [aVals for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
            pltae = [aVals for x in fFlows[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "e"]

            if dc == None:
                pltjbsx = [x["fn"] for x in fFlows[-window:] if  x.has_key("jb") and x["jb"] == "s"]
                pltjbex = [x["fn"] for x in fFlows[-window:] if  x.has_key("jb") and x["jb"] == "e"]
                pltlbsx = [x["fn"] for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "s"]
                pltlbex = [x["fn"] for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "e"]
                pltrbsx = [x["fn"] for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "s"]
                pltrbex = [x["fn"] for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "e"]
                pltjbs = [1.3 for x in fFlows[-window:]  if x.has_key("jb") and x["jb"] == "s"]
                pltjbe = [1.3 for x in fFlows[-window:]  if x.has_key("jb") and x["jb"] == "e"]
                pltlbs = [1.2 for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "s"]
                pltlbe = [1.2 for x in fFlows[-window:]  if x.has_key("lb") and x["lb"] == "e"]
                pltrbs = [1.1 for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "s"]
                pltrbe = [1.1 for x in fFlows[-window:]  if x.has_key("rb") and x["rb"] == "e"]
            #plt.subplot(211)
            #plt.plot(pltx, pltlXdiff, 'ro-', pltx, pltrXdiff, 'bo-')
            if figparms != None and figparms.has_key('figNums') == True:
                fig = figparms['figNums']
            else:
                fig = [3]
            #plt.subplot(212)
            if 3 in fig:
                plt.figure(10, figsize=figsize)
                if dc == None:
                    plt.plot(pltlx, lDiff, 'ro-', pltrx, rDiff, 'bo-')
                    plt.plot(pltax, [0 for x in xrange(len(pltax))], 'g--') # zero
                        #pltlx, la, 'r--', pltrx, ra, 'b--', # average
                        #pltlx, plsd1, 'r^-', pltlx, mlsd1, 'r^-', pltrx, prsd1, 'b^-', pltrx, mrsd1, 'b^-',
                        #pltlx, plsd2, 'r^-', pltlx, mlsd2, 'r^-', pltrx, prsd2, 'b^-', pltrx, mrsd2, 'b^-',
                    plt.plot(pltlx, plsdt, 'ro-', pltlx, mlsdt, 'ro-', pltrx, prsdt, 'bo-', pltrx, mrsdt, 'bo-', markeredgecolor='none') # t SD
                    plt.plot(pltasx, pltas, 'go', pltaex, pltae, 'g^', markersize=15.0) # annots of blinks
                    plt.plot(pltlbsx, pltlbs, 'ro', pltlbex, pltlbe, 'r^', markersize=15.0) # start & end of lBlinks
                    plt.plot(pltrbsx, pltrbs, 'bo', pltrbex, pltrbe, 'b^', markersize=15.0) # start & end of rBlinks
                    plt.plot(pltjbsx, pltjbs, 'yo', pltjbex, pltjbe, 'y^', markersize=15.0) # start & end of jBlinks

                    plt.tight_layout(pad=tightLayoutPad)
                    plt.xlabel('xlabel', fontsize=30)
                    plt.ylabel('ylabel', fontsize=30)
                else:
                    lline = plt.plot(pltlx, lDiff, 'ro-', markeredgecolor='none')
                    rline = plt.plot(pltrx, rDiff, 'bo-', markeredgecolor='none')
                    plt.plot(pltax, [0 for x in xrange(len(pltax))], 'g--') # zero
                        #pltlx, la, 'r--', pltrx, ra, 'b--', # average
                        #pltlx, plsd1, 'r^-', pltlx, mlsd1, 'r^-', pltrx, prsd1, 'b^-', pltrx, mrsd1, 'b^-',
                        #pltlx, plsd2, 'r^-', pltlx, mlsd2, 'r^-', pltrx, prsd2, 'b^-', pltrx, mrsd2, 'b^-',
                    lsd = plt.plot(pltlx, plsdt, 'ro-', markeredgecolor='none') # t SD
                    plt.plot(pltlx, mlsdt, 'ro-', markeredgecolor='none') # t SD
                    rsd = plt.plot(pltrx, prsdt, 'bo-', markeredgecolor='none') # t SD
                    plt.plot(pltrx, mrsdt, 'bo-', markeredgecolor='none') # t SD

                    anots1 = plt.plot(pltasx, pltas, 'go', markersize=15.0) # annots of blinks
                    anots2 = plt.plot(pltaex, pltae, 'g^', markersize=15.0) # annots of blinks

                    # fps
                    fleft1  = plt.plot(pltlbsx, pltlbs, 'ro', markersize=15.0) # start & end of lBlinks
                    fleft2  = plt.plot(pltlbex, pltlbe, 'r^', markersize=15.0) # start & end of lBlinks
                    fright1 = plt.plot(pltrbsx, pltrbs, 'bo', markersize=15.0) # start & end of rBlinks
                    fright2 = plt.plot(pltrbex, pltrbe, 'b^', markersize=15.0) # start & end of rBlinks
                    fboth1  = plt.plot(pltjbsx, pltjbs, 'yo', markersize=15.0) # start & end of jBlinks
                    fboth2  = plt.plot(pltjbex, pltjbe, 'y^', markersize=15.0) # start & end of jBlinks

                    # not fps
                    left1  = plt.plot(pltlbsxn, pltlbsn, 'ro', markersize=15.0) # start & end of lBlinks
                    left2  = plt.plot(pltlbexn, pltlben, 'r^', markersize=15.0) # start & end of lBlinks
                    right1  = plt.plot(pltrbsxn, pltrbsn, 'bo', markersize=15.0) # start & end of lBlinks
                    right2  = plt.plot(pltrbexn, pltrben, 'b^', markersize=15.0) # start & end of rBlinks
                    both1  = plt.plot(pltjbsxn, pltjbsn, 'yo', markersize=15.0) # start & end of lBlinks
                    both2  = plt.plot(pltjbexn, pltjben, 'y^', markersize=15.0) # start & end of jBlinks

                    if figparms != None and figparms.has_key('axis') == True:
                        plt.axis(
                            xmin=figparms['axis']['xmin'], xmax=figparms['axis']['xmax'],
                            ymin=figparms['axis']['ymin'], ymax=figparms['axis']['ymax']
                        )
                    plt.xlabel(u'sli\u010dice', fontsize=30)
                    plt.ylabel(u'razlika vsote premikov na obmo\u010dju o\u010di', fontsize=30)
                    plt.tight_layout(pad=tightLayoutPad)

                    ls = [anots1, both1, left1, right1, anots2, both2, left2, right2]
                    labs = ["", "", "", "",
                        u"anotirani me\u017eiki", u"zaznani: obe o\u010desi", u"zaznani: levo oko", u"zaznani: desno oko"
                    ]
                    if showLegend == True:
                        first_legend = plt.legend(ls, labs, ncol=2, numpoints=1, loc=figparms['legBpos'])
                        plt.gca().add_artist(first_legend)
                        plt.legend([lline, rline, lsd, rsd], ['levo oko', 'desno oko', 'st. odk.', 'st. odk.'], loc=figparms['legLpos'])

                    if figparms != None and figparms.has_key('figName') == True:
                        plt.savefig('/home/developer/other/notes/m/%s.png' % figparms['figName'], dpi=imgDpi, pad_inches=1)
            if 1 in fig:
                plt.figure(11, figsize=figsize)
                plt.plot(pltlx, lDiff, 'ro-',
                    pltax, [0 for x in xrange(len(pltax))], 'g--', # zero
                    pltlx, la, 'r--', # average
                    #pltlx, plsd1, 'r^-', pltlx, mlsd1, 'r^-', pltrx, prsd1, 'b^-', pltrx, mrsd1, 'b^-',
                    #pltlx, plsd2, 'r^-', pltlx, mlsd2, 'r^-', pltrx, prsd2, 'b^-', pltrx, mrsd2, 'b^-',
                    pltlx, plsdt, 'yo-', pltlx, mlsdt, 'yo-', # t SD
                    pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
                    pltlbsx, pltlbs, 'ro', pltlbex, pltlbe, 'r^', # start & end of blinks
                )
                plt.tight_layout(pad=tightLayoutPad)
                plt.xlabel('xlabel', fontsize=30)
                plt.ylabel('ylabel', fontsize=30)
            if 2 in fig:
                plt.figure(12, figsize=figsize)
                plt.plot(pltrx, rDiff, 'bo-',
                    pltax, [0 for x in xrange(len(pltax))], 'g--', # zero
                    pltrx, ra, 'b--', # average
                    #pltlx, plsd1, 'r^-', pltlx, mlsd1, 'r^-', pltrx, prsd1, 'b^-', pltrx, mrsd1, 'b^-',
                    #pltlx, plsd2, 'r^-', pltlx, mlsd2, 'r^-', pltrx, prsd2, 'b^-', pltrx, mrsd2, 'b^-',
                    pltrx, prsdt, 'yo-', pltrx, mrsdt, 'yo-', # t SD
                    pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
                    pltrbsx, pltrbs, 'bo', pltrbex, pltrbe, 'b^' # start & end of blinks
                )
                plt.tight_layout(pad=tightLayoutPad)
                plt.xlabel('xlabel', fontsize=30)
                plt.ylabel('ylabel', fontsize=30)

        if figparms != None and figparms.has_key('show') == True and figparms['show'] == False:
            pass
        else:
            plt.show()
        return

