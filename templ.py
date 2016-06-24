import matplotlib.pyplot as plt

from common import Common as Cmn

# control flags
debugProcessLogLine = False

class Templ:
    def __init__(self):
        #self.tCors = []
        pass

    @staticmethod
    def processLogLine(output, tCors, lBlinks, rBlinks):
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
            l1sd = float(corsInfo[corsInfo.index("lSD12")+2])
            l2sd = float(corsInfo[corsInfo.index("lSD12")+3])
            r1sd = float(corsInfo[corsInfo.index("rSD12")+2])
            r2sd = float(corsInfo[corsInfo.index("rSD12")+3])
            tCors.append({"fn": fn, "ts" : ts, "lcor" : lcor, "rcor" : rcor, "l1sd" : l1sd, "l2sd" : l2sd, "r1sd" : r1sd, "r2sd" : r2sd})
            Templ.postProcessLogLine(tCors, lBlinks, rBlinks, False)
        elif output.startswith("debug_blinks_d4:"):
            blinkInfo = output.split(" ")
            if blinkInfo[1] == "adding_lBlinkChunks":
                lst = lBlinks
            elif blinkInfo[1] == "adding_rBlinkChunks":
                lst = rBlinks

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
        elif output.startswith("exiting"):
            return True
        return False

    @staticmethod
    def postProcessLogLine(tCors, lBlinks, rBlinks, isEnd):
        if not isEnd:
            window = 300
        else:
            window = 0

        if not isEnd and (len(tCors) == 0 or len(tCors) % window != 0):
            return
        print repr(tCors)
        if isEnd:
            window = 0
        pltx = [x["fn"] for x in tCors[-window:]]
        lcor, rcor = [x["lcor"] for x in tCors[-window:]], [x["rcor"] for x in tCors[-window:]]
        lsd1, rsd1 = [x["l1sd"] for x in tCors[-window:]], [x["r1sd"] for x in tCors[-window:]]
        lsd2, rsd2 = [x["l2sd"] for x in tCors[-window:]], [x["r2sd"] for x in tCors[-window:]]

        plt.figure(1)
        plt.subplot(211)
        plt.plot(pltx, lcor, 'ro-', pltx, rcor, 'bo-',
            pltx, lsd1, 'r^-', pltx, rsd1, 'b^-',
            pltx, lsd2, 'rs-', pltx, rsd2, 'bs-')

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
