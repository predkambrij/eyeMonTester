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
        tracking = {"track":[]}
        notes = {"challenging":None, "glasses":None}
        curTrack = None
        lastFn = None
        annots = []
        curBlinkId = ""
        curBlinkStart = ""
        curBlinkEnd = ""
        curBlinkLC = []
        curBlinkRC = []

        content = False
        for fline in f:
            fline = fline.strip()
            # starting part of annot file
            if not content:
                if fline == "#start":
                    content = True
                elif fline.startswith("#challenging:"):
                    data = fline.split(" ")
                    if data[1] == "YES":
                        notes["challenging"] = True
                    elif data[1] == "NO":
                        notes["challenging"] = False
                elif fline.startswith("#glasses:"):
                    data = fline.split(" ")
                    if data[1] == "YES":
                        notes["glasses"] = True
                    elif data[1] == "NO":
                        notes["glasses"] = False
                continue
            else:
                if fline == "#end":
                    break

            #&temp.frameCounter,&temp.blinkID,
            #&nonFrontalFace,&leftFullyClosed,&leftNonFrontal,&rightFullyClosed,&rightNonFrontal,
            #&temp.faceX,&temp.faceY,&temp.faceWidth,&temp.faceHeight,
            #&temp.leftEye1x,&temp.leftEye1y,&temp.leftEye2x,&temp.leftEye2y,
            #&temp.rightEye1x,&temp.rightEye1y,&temp.rightEye2x,&temp.rightEye2y);
            # 0 frameCounter 1 blinkID 2 nonFrontalFace 3 leftFullyClosed 4 leftNonFrontal 5 rightFullyClosed 6 rightNonFrontal
            line = fline.split(":")
            # parse tracking slices
            if curTrack == None:
                lastFn = int(line[0])
                curTrack = [("start", lastFn)]
            else:
                curFn = int(line[0])
                if curFn != (lastFn+1):
                    curTrack.append(("end", lastFn))
                    tracking["track"].append(curTrack)
                    curTrack = [("start", curFn)]
                lastFn = curFn
            # parse blinks
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

        # finish tracking slices
        curTrack.append(("end", lastFn))
        tracking["track"].append(curTrack)

        # finish last blink if applicable
        if curBlinkId != "":
            if method == "farne":
                annots.append({"bs":int(curBlinkStart), "be":int(curBlinkEnd), "bi":int(curBlinkId)})
            else:
                Common.writeBlinkToFndict(fndict, curBlinkId, curBlinkStart, curBlinkEnd)

        if method == "farne":
            annotsD = Common.makeAnnotDicts(annots)
            annotsD.append(tracking)
            annotsD.append(notes)
            return annots, annotsD
        return

    @staticmethod
    def makeAnnotDicts(annots):
        annotsByStart = {}
        annotsByEnd = {}
        for annot in annots:
            annotsByStart[annot["bs"]] = annot
            annotsByEnd[annot["be"]]   = annot
        return [annotsByStart, annotsByEnd]

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

        for lFpsIndex, (lIndex, lFp) in zip(xrange(len(lFps)), lFps):
            for rFpsIndex, (rIndex, rFp) in zip(xrange(len(rFps)), rFps):
                if ((rFp["fs"] <= lFp["fs"] and lFp["fs"] <= rFp["fe"]) or (rFp["fs"] <= lFp["fe"] and lFp["fe"] <= rFp["fe"])):
                    byBothEyesLIndexesS.add(lFpsIndex)
                    byBothEyesRIndexesS.add(rFpsIndex)
                    byBothEyesS.add((lFpsIndex, rFpsIndex))
                    break
                elif ((lFp["fs"] <= rFp["fs"] and rFp["fs"] <= lFp["fe"]) or (lFp["fs"] <= rFp["fe"] and rFp["fe"] <= lFp["fe"])):
                    byBothEyesLIndexesS.add(lFpsIndex)
                    byBothEyesRIndexesS.add(rFpsIndex)
                    byBothEyesS.add((lFpsIndex, rFpsIndex))
                    break

        byOnlyL = [lFps[x] for x in xrange(len(lFps)) if x not in byBothEyesLIndexesS]
        byOnlyR = [rFps[x] for x in xrange(len(rFps)) if x not in byBothEyesRIndexesS]

        byBothEyes = [(lFps[li], rFps[ri]) for li, ri in byBothEyesS]
        byBothEyes.sort(key=lambda x:x[0][0])

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
        bCaught = set.intersection(*[set(lCaught), set(rCaught)])

        loCaught = [x["bi"] for x in annotsl if (x["bi"] in lCaught and (not x["bi"] in bCaught))]
        roCaught = [x["bi"] for x in annotsl if (x["bi"] in rCaught and (not x["bi"] in bCaught))]

        bMissed = [x["bi"] for x in annotsl if not x["bi"] in aCaught]
        aMissed = [x["bi"] for x in annotsl if not x["bi"] in bCaught]

        loMissed = [x["bi"] for x in annotsl if (x["bi"] in lMissed and (not x["bi"] in bMissed))]
        roMissed = [x["bi"] for x in annotsl if (x["bi"] in rMissed and (not x["bi"] in bMissed))]

        fpByBothEyes, fpByOnlyL, fpByOnlyR = Common._processFps(lFp, rFp)

        dc = {
            "lCaught":lCaught, "rCaught":rCaught, "loCaught":loCaught, "roCaught":roCaught, "bCaught":bCaught, "aCaught":aCaught,
            "lMissed":lMissed, "roMissed":roMissed, "loMissed":loMissed, "rMissed":rMissed, "bMissed":bMissed, "aMissed":aMissed,
            "lFp":lFp, "rFp":rFp, "fpByBothEyes":fpByBothEyes, "fpByOnlyL":fpByOnlyL, "fpByOnlyR":fpByOnlyR
        }
        return dc

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
