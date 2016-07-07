import matplotlib.pyplot as plt

import traceback
from common import Common as Cmn

# control flags
debugProcessLogLine = False

class Templ:
    def __init__(self):
        #self.tCors = []
        pass

    @staticmethod
    def processLogLine(output, annots, tCors, tCorsI, lBlinks, rBlinks, jBlinks):
        if output.startswith("debug_blinks_d1:"):
            corsInfo = output.split(" ")
            if debugProcessLogLine:
                print repr(corsInfo)
            if (corsInfo[1:] == ['blinkMeasureSize', 'is', 'zero']
                or corsInfo[3:7] == ['shortBmSize', 'is', 'less', 'than']
                or corsInfo[3:7] == ['fps', 'of', 'the', 'first']
                or corsInfo[3:-1] == ['shortBmSize', 'is', 'big', 'enough']
                or corsInfo[1:3] == ['updated', 'maxFramesShortList']
                ):
                return False
            fn   = int(corsInfo[corsInfo.index("lastF")+1])
            ts   = float(corsInfo[corsInfo.index("T")+1])
            lcor = float(corsInfo[corsInfo.index("La")+1])
            rcor = float(corsInfo[corsInfo.index("Ra")+1])
            la = float(corsInfo[corsInfo.index("La")+2])
            ra = float(corsInfo[corsInfo.index("Ra")+2])
            lDiff = float(corsInfo[corsInfo.index("La")+3])
            rDiff = float(corsInfo[corsInfo.index("Ra")+3])
            lsd = float(corsInfo[corsInfo.index("lSDft")+1])
            pl1sd = float(corsInfo[corsInfo.index("lSDft")+2])
            ml1sd = float(corsInfo[corsInfo.index("lSDft")+3])
            l2sd = float(corsInfo[corsInfo.index("lSDft")+4])
            rsd = float(corsInfo[corsInfo.index("rSDft")+1])
            pr1sd = float(corsInfo[corsInfo.index("rSDft")+2])
            mr1sd = float(corsInfo[corsInfo.index("rSDft")+3])
            r2sd = float(corsInfo[corsInfo.index("rSDft")+4])
            tCors.append({"fn":fn, "ts":ts, "lcor":lcor, "rcor":rcor, "lDiff":lDiff, "rDiff":rDiff, "la":la, "ra":ra, "lsd":lsd, "pl1sd":pl1sd, "ml1sd":ml1sd, "l2sd":l2sd, "rsd":rsd, "pr1sd":pr1sd, "mr1sd":mr1sd, "r2sd":r2sd})
            tCorsI[fn] = len(tCors)-1
            if annots[0].has_key(fn):
                tCors[-1].update(annots[0][fn])
                tCors[-1]["annotEvent"] = "s"
            if annots[1].has_key(fn):
                tCors[-1].update(annots[1][fn])
                tCors[-1]["annotEvent"] = "e"
            #Templ.postProcessLogLine(tCors, lBlinks, rBlinks, jBlinks, False)
        elif output.startswith("debug_blinks_d4:"):
            blinkInfo = output.split(" ")
            if blinkInfo[1] == "adding_lBlinkChunks":
                lst = lBlinks
                eye = "l"
            elif blinkInfo[1] == "adding_rBlinkChunks":
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
                tCors[tCorsI[fs]][eye+"b"] = "s"
                tCors[tCorsI[fe]][eye+"b"] = "e"
            except:
                # there was an interruption of face tracking
                # blink was detected because we are not excluding if difference between frame is so long, that shortSize is too short
                # fuck it for now, there are not many those
                pass

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
            tCors[tCorsI[fs]]["jb"] = "s"
            tCors[tCorsI[fe]]["jb"] = "e"
        elif output.startswith("exiting"):
            return True
        return False

    @staticmethod
    def postProcessLogLine(tCors, lBlinks, rBlinks, jBlinks, isEnd):
        if not isEnd:
            window = 300
        else:
            window = 0

        if not isEnd and (len(tCors) == 0 or len(tCors) % window != 0):
            return
        #print repr(tCors)
        if isEnd:
            window = 0
        pltx = [x["fn"] for x in tCors[-window:]]
        pltld = [(xm1["lcor"]-x["lcor"]) for xm1, x in zip((tCors[1:-1]), (tCors[0:]))]
        pltasx = [x["fn"] for x in tCors[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
        pltaex = [x["fn"] for x in tCors[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "e"]
        pltas = [1.004 for x in tCors[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
        pltae = [1.004 for x in tCors[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "e"]

        pltlxbs = [x["fn"] for x in tCors[-window:] if  x.has_key("lb") and x["lb"] == "s"]
        pltlxbe = [x["fn"] for x in tCors[-window:] if  x.has_key("lb") and x["lb"] == "e"]
        pltlbs = [1.002 for x in tCors[-window:]  if x.has_key("lb") and x["lb"] == "s"]
        pltlbe = [1.002 for x in tCors[-window:]  if x.has_key("lb") and x["lb"] == "e"]
        pltrxbs = [x["fn"] for x in tCors[-window:] if  x.has_key("rb") and x["rb"] == "s"]
        pltrxbe = [x["fn"] for x in tCors[-window:] if  x.has_key("rb") and x["rb"] == "e"]
        pltrbs = [1.001 for x in tCors[-window:]  if x.has_key("rb") and x["rb"] == "s"]
        pltrbe = [1.001 for x in tCors[-window:]  if x.has_key("rb") and x["rb"] == "e"]
        pltjxbs = [x["fn"] for x in tCors[-window:] if  x.has_key("jb") and x["jb"] == "s"]
        pltjxbe = [x["fn"] for x in tCors[-window:] if  x.has_key("jb") and x["jb"] == "e"]
        pltjbs = [1.003 for x in tCors[-window:]  if x.has_key("jb") and x["jb"] == "s"]
        pltjbe = [1.003 for x in tCors[-window:]  if x.has_key("jb") and x["jb"] == "e"]
        
        lcor, rcor = [x["lcor"] for x in tCors[-window:]], [x["rcor"] for x in tCors[-window:]]
        la, ra = [x["la"] for x in tCors[-window:]], [x["ra"] for x in tCors[-window:]]
        lDiff, rDiff = [x["lDiff"] for x in tCors[-window:]], [x["rDiff"] for x in tCors[-window:]]
        #lsd, rsd = [1-(x["lsd"]*2) for x in tCors[-window:]], [1-(x["rsd"]*2) for x in tCors[-window:]]
        plsd1, prsd1 = [x["pl1sd"] for x in tCors[-window:]], [x["pr1sd"] for x in tCors[-window:]]
        mlsd1, mrsd1 = [x["ml1sd"] for x in tCors[-window:]], [x["mr1sd"] for x in tCors[-window:]]
        lsd2, rsd2 = [1-x["l2sd"] for x in tCors[-window:]], [1-x["r2sd"] for x in tCors[-window:]]

        figs = [4]
        if 4 in figs:
            plt.figure(4)
            #plt.subplot(211)
            plt.plot(
                pltx, [1 for x in xrange(len(pltx))], 'g--', # ones
                pltx, lcor, 'ro-',
                pltx, rcor, 'bo-',
                pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
                pltlxbs, pltlbs, 'ro', pltlxbe, pltlbe, 'r^', # start & end of blinks
                pltrxbs, pltrbs, 'bo', pltrxbe, pltrbe, 'b^', # start & end of blinks
                pltjxbs, pltjbs, 'yo', pltjxbe, pltjbe, 'y^', # start & end of blinks
                pltx, lsd2, 'gs-',
                pltx, rsd2, 'bs-',
                )
            plt.tight_layout()
        if 1 in figs:
            plt.figure(1)
            #plt.subplot(211)
            plt.plot(
                pltx, [1 for x in xrange(len(pltx))], 'g--', # ones
                pltx, lcor, 'ro-',
                #pltx, la, 'ks-',
                pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
                pltlxbs, pltlbs, 'ro', pltlxbe, pltlbe, 'r^', # start & end of blinks
                #pltx, lsd, 'y^-',
                #pltx, lsd1, 'y^-',
                pltx, lsd2, 'gs-',
                )
            plt.tight_layout()

        if 2 in figs:
            plt.figure(2)
            plt.plot(
                pltx, [1 for x in xrange(len(pltx))], 'g--', # ones
                pltx, rcor, 'bo-',
                #pltx, ra, 'ks-',
                pltasx, pltas, 'go', pltaex, pltae, 'g^', # annots of blinks
                pltrxbs, pltrbs, 'bo', pltrxbe, pltrbe, 'b^', # start & end of blinks
                #pltx, rsd, 'y^-',
                #pltx, rsd1, 'y^-',
                pltx, rsd2, 'gs-',
                )
            plt.tight_layout()
        if 3 in figs:
            plt.figure(3)
            plt.plot(
                pltx, lDiff, 'r--',
                pltx, plsd1, 'y^-',
                pltx, mlsd1, 'y^-',
                pltx, rDiff, 'b--',
                pltx, prsd1, 'y^-',
                pltx, mrsd1, 'y^-',
                )
            plt.tight_layout()

        #plt.subplot(212)
        #plt.plot(pltx, pltlYdiff, 'ro-', pltx, pltrYdiff, 'bo-')
        plt.show()
        return


    # generating excel report
    @staticmethod
    def buildFndict(tCors):
        fndict = {}
        for d in tCors:
            fndict[d["fn"]] = {
                "ts":d["ts"], "lcor":d["lcor"], "rcor":d["rcor"], "l1sd":d["l1sd"], "l2sd":d["l2sd"], "r1sd":d["r1sd"], "r2sd":d["r2sd"]
            }
        return fndict

    @staticmethod
    def generateTCSV(vidPrefix, videoAnnot, tCors, lBlinks, rBlinks):
        fndict = Templ.buildFndict(tCors)
        Cmn.addDetectedBlinks(lBlinks, rBlinks, fndict)
        f = file(vidPrefix+videoAnnot)
        Cmn.parseAnnotations(f, fndict)

        # sort by frame num
        fnl = sorted(fndict.items(), key=lambda x:float(x[0]))
        return fndict, fnl

    @staticmethod
    def writeTCSV(path, fnl):
        pref = path+"outputs/"
        f = file(pref+"out.csv","wb")

        for frameNum, data in fnl:
            line = ""
            line += str(frameNum)

            for t in ["lcor", "rcor", "l1sd", "l2sd", "r1sd", "r2sd"]: # "ts", 
                line += "\t%.6f" % data[t]

            for t in ["lbs", "lbe", "rbs", "rbe"]:
                line += "\t"
                if data.has_key(t):
                    line += "%.3f" % data[t]

            for t in ["anots", "anotc", "anote"]:
                line += "\t"
                if data.has_key(t):
                    line += "%.3f" % data[t]

            line += "\n"
            f.write(line)

        f.close()
