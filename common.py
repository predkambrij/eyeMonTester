import traceback

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
            annotsD = Common.makeAnnotDicts(annots)
            return annots, annotsD
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
    def _annotsById(annots):
        annotsD = {}
        for annot in annots:
            annotsD[annot["bi"]] = annot
        return annotsD


    @staticmethod
    def _detectionCoverageHelper(annotsl, annotsD, blinks):
        caught = set()
        caughtIndices = set()

        i = 0
        for blink in blinks:
            ai = 0
            for annot in annotsl:
                if ((annot["bs"] <= blink["fs"] and blink["fs"] <= annot["be"])
                    or (annot["bs"] <= blink["fe"] and blink["fe"] <= annot["be"])):
                    caught.add(annot["bi"])
                    caughtIndices.add(i)
                    del annotsl[ai]
                    break
                elif ((blink["fs"] <= annot["bs"] and annot["bs"] <= blink["fe"])
                    or (blink["fs"] <= annot["be"] and annot["be"] <= blink["fe"])):
                    caught.add(annot["bi"])
                    caughtIndices.add(i)
                    del annotsl[ai]
                    break
                ai += 1
            i+=1
        fp = [(x, blinks[x]) for x in xrange(len(blinks)) if x not in caughtIndices]
        missed = [x["bi"] for x in annotsl if not x["bi"] in caught]
        caught = sorted(list(caught), key=lambda x:x)
        return caught, caughtIndices, missed, fp

    @staticmethod
    def _processFps(lFps, rFps):
        byBothEyesS = set()
        byBothEyesLIndexesS = set()
        byBothEyesRIndexesS = set()

        # [(0, {'duration': 333.333333, 'start': 13000.0, 'fs': 389, 'end': 13333.333333, 'fe': 399}),
        for lIndex, lFp in lFps:
            for rIndex, rFp in rFps:
                if ((rFp["start"] <= lFp["start"] and lFp["start"] <= rFp["end"])
                    or (rFp["start"] <= lFp["end"] and lFp["end"] <= rFp["end"])):
                    byBothEyesLIndexesS.add(lIndex)
                    byBothEyesRIndexesS.add(rIndex)
                    byBothEyesS.add((lIndex, rIndex))
                    break
                elif ((lFp["start"] <= rFp["start"] and rFp["start"] <= lFp["end"])
                    or (lFp["start"] <= rFp["end"] and rFp["end"] <= lFp["end"])):
                    byBothEyesLIndexesS.add(lIndex)
                    byBothEyesRIndexesS.add(rIndex)
                    byBothEyesS.add((lIndex, rIndex))
                    break
        byOnlyL = [lFps[x] for x in xrange(len(lFps)) if x not in byBothEyesLIndexesS]
        byOnlyR = [rFps[x] for x in xrange(len(rFps)) if x not in byBothEyesRIndexesS]
        try:
            byBothEyes = [(lFps[li], rFps[ri]) for li, ri in byBothEyesS]
            byBothEyes.sort(key=lambda x:x[0][0])
        except:
            print traceback.format_exc()
            byBothEyes = []

        return byBothEyes, byOnlyL, byOnlyR

    @staticmethod
    def displayDetectionCoverage(l, r, o):
        print "annot %i" % (len(o[3]))
        print "left %i" % len(l[0])
        print "lCaught (%i) %s" % (len(l[1]), repr(l[1]))
        print "lMissed (%i) %s" % (len(l[2]), repr(l[2]))
        print "lFp (%i) %s" % (len(l[3]), repr(l[3]))
        print "right %i" % len(r[0])
        print "rCaught (%i) %s" % (len(r[1]), repr(r[1]))
        print "rMissed (%i) %s" % (len(r[2]), repr(r[2]))
        print "rFp (%i) %s" % (len(r[3]), repr(r[3]))
        print "other"
        print "bCaught (%i) %s" % (len(o[0]), o[0])
        print "aCaught (%i) %s" % (len(o[1]), o[1])
        print "aMissed (%i) %s" % (len(o[2]), o[2])

    @staticmethod
    def detectionCoverageF(annotsl, lBlinks, rBlinks):
        """
        lBlinks/rBlinks "fs", "fe", "start", "end", "duration"
        annots bs, be, bi
        """
        # TODO max frameNum
        annotsD = Common._annotsById(annotsl)
        lCaught, lCaughtIndices, lMissed, lFp = Common._detectionCoverageHelper(annotsl[:], annotsD, lBlinks)
        rCaught, rCaughtIndices, rMissed, rFp = Common._detectionCoverageHelper(annotsl[:], annotsD, rBlinks)

        aCaught = set.union(set(lCaught), set(rCaught))

        aMissed = [x["bi"] for x in annotsl if not x["bi"] in aCaught]
        bCaught = set.intersection(*[set(lCaught), set(rCaught)])
        bMissed = [x["bi"] for x in annotsl if not x["bi"] in bCaught]

        fpByBothEyes, fpByOnlyL, fpByOnlyR = Common._processFps(lFp, rFp)

        l = (lBlinks, lCaught, lMissed, lFp)
        r = (rBlinks, rCaught, rMissed, rFp)
        o = (bCaught, bMissed, aCaught, aMissed, fpByBothEyes, fpByOnlyL, fpByOnlyR)
        return l, r, o
