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
                or corsInfo[3:5] == ['updated', 'maxFramesShortList']
                ):
                return False
            fn    = int(corsInfo[corsInfo.index("lastF")+1])
            ts    = float(corsInfo[corsInfo.index("T")+1])
            lcor  = float(corsInfo[corsInfo.index("La")+1])
            rcor  = float(corsInfo[corsInfo.index("Ra")+1])
            la    = float(corsInfo[corsInfo.index("La")+2])
            ra    = float(corsInfo[corsInfo.index("Ra")+2])
            lDiff = float(corsInfo[corsInfo.index("La")+3])
            rDiff = float(corsInfo[corsInfo.index("Ra")+3])
            lsd   = float(corsInfo[corsInfo.index("lSDft")+1])
            pl1sd = float(corsInfo[corsInfo.index("lSDft")+2])
            ml1sd = float(corsInfo[corsInfo.index("lSDft")+3])
            l2sd  = float(corsInfo[corsInfo.index("lSDft")+4])
            rsd   = float(corsInfo[corsInfo.index("rSDft")+1])
            pr1sd = float(corsInfo[corsInfo.index("rSDft")+2])
            mr1sd = float(corsInfo[corsInfo.index("rSDft")+3])
            r2sd  = float(corsInfo[corsInfo.index("rSDft")+4])
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
                tCors[tCorsI[fs]]["jb"] = "s"
                tCors[tCorsI[fe]]["jb"] = "e"
            except:
                print "not graphing blink j %d-%d" % (eye, fs, fe)
        elif output.startswith("exiting"):
            return True
        return False

    @staticmethod
    def postProcessLogLine(tCors, lBlinks, rBlinks, jBlinks, isEnd, videoName=None, figparms=None):
        cm13_5 = 5.314961
        imgDpi = 150
        tightLayoutPad = 0.2
        figsize = (cm13_5*4, cm13_5*2)
        if not isEnd:
            window = 600
        else:
            window = 0

        if not isEnd and (len(tCors) == 0 or len(tCors) % window != 0):
            return
        #print repr(tCors)
        if isEnd:
            window = 0
        aVals = 1.007 if not figparms.has_key('aVals') else figparms['aVals']
        jVals = 1.005 if not figparms.has_key('jVals') else figparms['jVals']
        lVals = 1.003 if not figparms.has_key('lVals') else figparms['lVals']
        rVals = 1.001 if not figparms.has_key('rVals') else figparms['rVals']
        pltx = [x["fn"] for x in tCors[-window:]]
        pltld = [(xm1["lcor"]-x["lcor"]) for xm1, x in zip((tCors[1:-1]), (tCors[0:]))]
        pltasx = [x["fn"] for x in tCors[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
        pltaex = [x["fn"] for x in tCors[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "e"]
        pltas = [aVals for x in tCors[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "s"]
        pltae = [aVals for x in tCors[-window:]  if x.has_key("annotEvent") and x["annotEvent"] == "e"]

        pltlxbs = [x["fn"] for x in tCors[-window:] if  x.has_key("lb") and x["lb"] == "s"]
        pltlxbe = [x["fn"] for x in tCors[-window:] if  x.has_key("lb") and x["lb"] == "e"]
        pltlbs = [lVals for x in tCors[-window:]  if x.has_key("lb") and x["lb"] == "s"]
        pltlbe = [lVals for x in tCors[-window:]  if x.has_key("lb") and x["lb"] == "e"]
        pltrxbs = [x["fn"] for x in tCors[-window:] if  x.has_key("rb") and x["rb"] == "s"]
        pltrxbe = [x["fn"] for x in tCors[-window:] if  x.has_key("rb") and x["rb"] == "e"]
        pltrbs = [rVals for x in tCors[-window:]  if x.has_key("rb") and x["rb"] == "s"]
        pltrbe = [rVals for x in tCors[-window:]  if x.has_key("rb") and x["rb"] == "e"]
        pltjxbs = [x["fn"] for x in tCors[-window:] if  x.has_key("jb") and x["jb"] == "s"]
        pltjxbe = [x["fn"] for x in tCors[-window:] if  x.has_key("jb") and x["jb"] == "e"]
        pltjbs = [jVals for x in tCors[-window:]  if x.has_key("jb") and x["jb"] == "s"]
        pltjbe = [jVals for x in tCors[-window:]  if x.has_key("jb") and x["jb"] == "e"]
        
        lcor, rcor = [x["lcor"] for x in tCors[-window:]], [x["rcor"] for x in tCors[-window:]]
        la, ra = [x["la"] for x in tCors[-window:]], [x["ra"] for x in tCors[-window:]]
        lDiff, rDiff = [x["lDiff"] for x in tCors[-window:]], [x["rDiff"] for x in tCors[-window:]]
        #lsd, rsd = [1-(x["lsd"]*2) for x in tCors[-window:]], [1-(x["rsd"]*2) for x in tCors[-window:]]
        plsd1, prsd1 = [x["pl1sd"] for x in tCors[-window:]], [x["pr1sd"] for x in tCors[-window:]]
        mlsd1, mrsd1 = [x["ml1sd"] for x in tCors[-window:]], [x["mr1sd"] for x in tCors[-window:]]
        lsd2, rsd2 = [1-x["l2sd"] for x in tCors[-window:]], [1-x["r2sd"] for x in tCors[-window:]]
        plsd2, mlsd2 = [x["l2sd"] for x in tCors[-window:]], [0-x["l2sd"] for x in tCors[-window:]]
        prsd2, mrsd2 = [x["r2sd"] for x in tCors[-window:]], [0-x["r2sd"] for x in tCors[-window:]]

        print "pltasx", repr(pltasx)
        print "pltas", repr(pltas)
        print "pltaex", repr(pltaex)
        print "pltae", repr(pltae)
        if figparms != None and figparms.has_key('figNums') == True:
            figs = figparms['figNums']
        else:
            figs = [4, 3]

        if 4 in figs:
            plt.figure(4, figsize=figsize)
            #plt.subplot(211)
            lline = plt.plot(pltx, lcor, 'ro-', label="levo oko", markeredgecolor='none')
            rline = plt.plot(pltx, rcor, 'bo-', label="desno oko", markeredgecolor='none')
            plt.plot(pltx, [1 for x in xrange(len(pltx))], 'g--') # ones
            anots1 = plt.plot(pltasx, pltas, 'go', markersize=15.0, label="anno")
            anots2 = plt.plot(pltaex, pltae, 'g^', markersize=15.0) # annots of blinks
            left1  = plt.plot(pltlxbs, pltlbs, 'ro', markersize=15.0, label="lef") # start & end of blinks
            left2  = plt.plot(pltlxbe, pltlbe, 'r^', markersize=15.0) # start & end of blinks
            right1 = plt.plot(pltrxbs, pltrbs, 'bo', markersize=15.0, label="rig") # start & end of blinks
            right2 = plt.plot(pltrxbe, pltrbe, 'b^', markersize=15.0) # start & end of blinks
            both1  = plt.plot(pltjxbs, pltjbs, 'yo', markersize=15.0, label="bot") # start & end of blinks
            both2  = plt.plot(pltjxbe, pltjbe, 'y^', markersize=15.0) # start & end of blinks
            lsd = plt.plot(pltx, lsd2, 'rs-', markeredgecolor='none')
            rsd = plt.plot(pltx, rsd2, 'bs-', markeredgecolor='none')
            if figparms != None and figparms.has_key('axis') == True:
                plt.axis(
                    xmin=figparms['axis']['xmin'], xmax=figparms['axis']['xmax'],
                    ymin=figparms['axis']['ymin'], ymax=figparms['axis']['ymax']
                )
            ls = [anots1, both1, left1, right1, anots2, both2, left2, right2]
            labs = ["", "", "", "",
                u"anotirani me\u017eiki", u"zaznani: obe o\u010desi", u"zaznani: levo oko", u"zaznani: desno oko"
            ]
            first_legend = plt.legend(ls, labs, ncol=2, numpoints=1, loc=figparms['legBpos'])
            plt.gca().add_artist(first_legend)

            plt.legend([lline, rline, lsd, rsd], ['levo oko', 'desno oko', '2. st. odk.', '2. st. odk.'], loc=figparms['legLpos'])

            plt.xlabel(u'sli\u010dice', fontsize=30)
            plt.ylabel(u'korelacija ujemanja s predlogo', fontsize=30)
            plt.tight_layout(pad=tightLayoutPad)
            if figparms != None and figparms.has_key('figName') == True:
                plt.savefig('/home/developer/other/notes/m/%s.png' % figparms['figName'], dpi=imgDpi, pad_inches=1)
        if 1 in figs:
            plt.figure(1, figsize=figsize)
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
            plt.figure(2, figsize=figsize)
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
            plt.figure(3, figsize=figsize)
            l = plt.plot(pltx, lDiff, 'r--')
            r = plt.plot(pltx, rDiff, 'b--')
            left1 = plt.plot(pltx, plsd1, 'r^-', markeredgecolor='none')
            right1 = plt.plot(pltx, prsd1, 'b^-', markeredgecolor='none')
            left2 = plt.plot(pltx, plsd2, 'yo-', markeredgecolor='none')
            right2 = plt.plot(pltx, prsd2, 'go-', markeredgecolor='none')
            plt.plot(pltx, mlsd1, 'r^-', markeredgecolor='none')
            plt.plot(pltx, mrsd1, 'b^-', markeredgecolor='none')
            plt.plot(pltx, mlsd2, 'yo-', markeredgecolor='none')
            plt.plot(pltx, mrsd2, 'go-', markeredgecolor='none')

            if figparms != None and figparms.has_key('axis') == True:
                plt.axis(
                    xmin=figparms['axis']['xmin'], xmax=figparms['axis']['xmax'],
                    ymin=figparms['axis']['ymin'], ymax=figparms['axis']['ymax']
                )

            ls = [l,r, left1, right1, left2, right2]
            labs = [
                'levo oko',
                'desno oko',
                'levo:    1. st. odk.',
                'desno: 1. st. odk.',
                'levo:    2. st. odk.',
                'desno: 2. st. odk.',
                #'1. st. odk.',
                #'2. st. odk.',
            ]
            plt.legend(ls, labs, loc=figparms['legBpos'])
            plt.xlabel(u'sli\u010dice', fontsize=30)
            #plt.ylabel(u'razlika vsote med zgornjim in spodnjim delom obmo\u010dja o\u010di', fontsize=30)
            plt.ylabel(u'odvod signala', fontsize=30)
            plt.tight_layout(pad=tightLayoutPad)
            if figparms != None and figparms.has_key('figName') == True:
                plt.savefig('/home/developer/other/notes/m/%s.png' % figparms['figName'], dpi=imgDpi, pad_inches=1)


        #plt.subplot(212)
        #plt.plot(pltx, pltlYdiff, 'ro-', pltx, pltrYdiff, 'bo-')
        if figparms != None and figparms.has_key('show') == True and figparms['show'] == False:
            pass
        else:
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
