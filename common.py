
class Common:
    def __init__(self):
        pass

    @staticmethod
    def addDetectedBlinks(lBlinks, rBlinks, fndict):
        for blink in lBlinks:
            for frame, timing in [("fs", "lbs"), ("fe", "lbe")]:
                fndict[blink[frame]][timing] = 0.998

        for blink in rBlinks:
            for frame, timing in [("fs", "rbs"), ("fe", "rbe")]:
                fndict[blink[frame]][timing] = 0.997
        return

    @staticmethod
    def writeBlinkToFndict(fndict, curBlinkId, curBlinkStart, curBlinkEnd):
        try:
            fndict[int(curBlinkStart)]["anots"] = 0.999
            fndict[int(curBlinkStart)]["anotBlinkId"] = curBlinkId
            fndict[int(curBlinkEnd)]["anote"] = 0.999
        except KeyError:
            print "skipping %s %s %s" % (curBlinkId, curBlinkStart, curBlinkEnd)

    @staticmethod
    def parseAnnotations(f, fndict, method):
        annots = []
        curBlinkId = ""
        curBlinkStart = ""
        curBlinkEnd = ""
        curBlinkLC = []
        curBlinkRC = []

        content = False
        for fline in f:
            fline = fline.strip()
            if not content:
                if fline == "#start":
                    content = True
                continue
            else:
                if fline == "#end":
                    break

            # 0 frameCounter 1 blinkID 2 nonFrontalFace 3 leftFullyClosed 4 leftNonFrontal 5 rightFullyClosed 6 rightNonFrontal
            line = fline.split(":")
            if line[1] != curBlinkId:
                if line[1] == "-1":
                    if curBlinkId == "":
                        continue
                    else:
                        if method == "farne":
                            annots.append({"bs":int(curBlinkStart), "be":int(curBlinkEnd), "bi":int(curBlinkId)})
                        else:
                            Common.writeBlinkToFndict(fndict, curBlinkId, curBlinkStart, curBlinkEnd)
                        curBlinkId    = ""
                        curBlinkStart = ""
                        curBlinkEnd   = ""
                else:
                    if curBlinkId == "":
                        curBlinkId = line[1]
                        curBlinkStart = line[0]
                    else:
                        if method == "farne":
                            annots.append({"bs":int(curBlinkStart), "be":int(curBlinkEnd), "bi":int(curBlinkId)})
                        else:
                            Common.writeBlinkToFndict(fndict, curBlinkId, curBlinkStart, curBlinkEnd)
                        curBlinkId    = line[1]
                        curBlinkStart = line[0]
                        curBlinkEnd   = ""
            # still the same, can also parse FullyClosed
            curBlinkEnd = line[0]

        if curBlinkId != "":
            if method == "farne":
                annots.append({"bs":int(curBlinkStart), "be":int(curBlinkEnd), "bi":int(curBlinkId)})
            else:
                Common.writeBlinkToFndict(fndict, curBlinkId, curBlinkStart, curBlinkEnd)

        if method == "farne":
            return Common.makeAnnotDicts(annots)
        return

    @staticmethod
    def makeAnnotDicts(annots):
        annotsByStart = {}
        annotsByEnd = {}
        for annot in annots:
            annotsByStart[annot["bs"]] = annot
            annotsByEnd[annot["be"]]   = annot
        return annotsByStart, annotsByEnd

    @staticmethod
    def detectionCoverage(lBlinks, rBlinks, fnl):
        """requires "lbs", "lbe", "rbs", "rbe", "anots", "anote", "anotBlinkId"
        """
        lCaughtI = set()
        rCaughtI = set()
        lCaught = set()
        rCaught = set()
        missed  = set()
        lookingEnd = False
        blinkId = None

        lStartBlink = {}
        for i in xrange(len(lBlinks)):
            lStartBlink[lBlinks[i]["fs"]] = i
        rStartBlink = {}
        for i in xrange(len(rBlinks)):
            rStartBlink[rBlinks[i]["fs"]] = i
        lEndBlink = {}
        for i in xrange(len(lBlinks)):
            lEndBlink[lBlinks[i]["fe"]] = i
        rEndBlink = {}
        for i in xrange(len(rBlinks)):
            rEndBlink[rBlinks[i]["fe"]] = i

        annotBlink = {}
        for frameNum, data in fnl:
            if lookingEnd == False:
                if data.has_key("anots"):
                    lookingEnd = True
                    blinkId = data["anotBlinkId"]
                    annotBlink[blinkId] = frameNum
            if lookingEnd == True:
                if data.has_key("lbs"):
                    lCaught.add(blinkId)
                    lCaughtI.add(lStartBlink[frameNum])
                if data.has_key("lbe"):
                    lCaught.add(blinkId)
                    lCaughtI.add(lEndBlink[frameNum])
                if data.has_key("rbs"):
                    rCaught.add(blinkId)
                    rCaughtI.add(rStartBlink[frameNum])
                if data.has_key("rbe"):
                    rCaught.add(blinkId)
                    rCaughtI.add(rEndBlink[frameNum])
                if data.has_key("anote"):
                    if (not blinkId in lCaught) and (not blinkId in rCaught):
                        missed.add(blinkId)
                    lookingEnd = False
        aCaught = set.union(lCaught, rCaught)
        bCaught = set.intersection(*[lCaught, rCaught])

        lFp = []
        for bi in xrange(len(lBlinks)):
            if not bi in lCaughtI:
                lFp.append(lBlinks[bi])

        rFp = []
        for bi in xrange(len(rBlinks)):
            if not bi in rCaughtI:
                rFp.append(rBlinks[bi])
        r = [sorted(list(x), key=lambda y:int(y)) for x in (lCaught, rCaught, bCaught, aCaught, missed)]

        # timeline fs m, fs, lf
        falseFrames = []
        for mi in missed:
            falseFrames.append((annotBlink[mi], "m"))

        for lfp in lFp:
            falseFrames.append((lfp["fs"], "lf"))
        for rfp in rFp:
            falseFrames.append((rfp["fs"], "rf"))
        falseFrames.sort(key=lambda x:x[0])

        r.append(falseFrames)
        return r

    @staticmethod
    def detectionCoverageF(fFlows):
        """requires "lbs", "lbe", "rbs", "rbe", "anots", "anote", "anotBlinkId"
        """
        lCaughtI = set()
        rCaughtI = set()
        lCaught = set()
        rCaught = set()
        missed  = set()
        lookingEnd = False
        blinkId = None

        lStartBlink = {}
        for i in xrange(len(lBlinks)):
            lStartBlink[lBlinks[i]["fs"]] = i
        rStartBlink = {}
        for i in xrange(len(rBlinks)):
            rStartBlink[rBlinks[i]["fs"]] = i
        lEndBlink = {}
        for i in xrange(len(lBlinks)):
            lEndBlink[lBlinks[i]["fe"]] = i
        rEndBlink = {}
        for i in xrange(len(rBlinks)):
            rEndBlink[rBlinks[i]["fe"]] = i

        annotBlink = {}
        for frameNum, data in fnl:
            if lookingEnd == False:
                if data.has_key("anots"):
                    lookingEnd = True
                    blinkId = data["anotBlinkId"]
                    annotBlink[blinkId] = frameNum
            if lookingEnd == True:
                if data.has_key("lbs"):
                    lCaught.add(blinkId)
                    lCaughtI.add(lStartBlink[frameNum])
                if data.has_key("lbe"):
                    lCaught.add(blinkId)
                    lCaughtI.add(lEndBlink[frameNum])
                if data.has_key("rbs"):
                    rCaught.add(blinkId)
                    rCaughtI.add(rStartBlink[frameNum])
                if data.has_key("rbe"):
                    rCaught.add(blinkId)
                    rCaughtI.add(rEndBlink[frameNum])
                if data.has_key("anote"):
                    if (not blinkId in lCaught) and (not blinkId in rCaught):
                        missed.add(blinkId)
                    lookingEnd = False
        aCaught = set.union(lCaught, rCaught)
        bCaught = set.intersection(*[lCaught, rCaught])

        lFp = []
        for bi in xrange(len(lBlinks)):
            if not bi in lCaughtI:
                lFp.append(lBlinks[bi])

        rFp = []
        for bi in xrange(len(rBlinks)):
            if not bi in rCaughtI:
                rFp.append(rBlinks[bi])
        r = [sorted(list(x), key=lambda y:int(y)) for x in (lCaught, rCaught, bCaught, aCaught, missed)]

        # timeline fs m, fs, lf
        falseFrames = []
        for mi in missed:
            falseFrames.append((annotBlink[mi], "m"))

        for lfp in lFp:
            falseFrames.append((lfp["fs"], "lf"))
        for rfp in rFp:
            falseFrames.append((rfp["fs"], "rf"))
        falseFrames.sort(key=lambda x:x[0])

        r.append(falseFrames)
        return r
