import os, traceback
import processVideo
from common import Common as Cmn
from farne import Farne
from templ import Templ
from blackpixels import Blackpixels

class VideoQueue:
    def __init__(self):
        pass

    @staticmethod
    def prepareOutputFileName(codeDirectory, outputPrefix, videoName):
        videoDir, videoFile = os.path.split(videoName)
        videoBase, videoExt = os.path.splitext(videoFile)
        outputFileDir = codeDirectory+outputPrefix+videoDir
        outputFileName = outputFileDir+"/"+videoBase+".out"

        if not os.path.exists(outputFileDir):
            os.makedirs(outputFileDir)
        return outputFileName

    @staticmethod
    def writeVideoResults(outputFileName, methodVar, lBlinks, rBlinks, jBlinks, tracking):
        f = file(outputFileName, "wb")
        f.write(repr(methodVar)+"\n")
        f.write(repr(lBlinks)+"\n")
        f.write(repr(rBlinks)+"\n")
        f.write(repr(jBlinks)+"\n")
        f.write(repr(tracking)+"\n")
        f.close()
        return

    @staticmethod
    def processVideoQueue(cfg, videos, videoRange):
        isWebcam = False
        if isWebcam == True:
            fFlows, lBlinks, rBlinks, jBlinks, tracking = processVideo.processVideo(cfg, isWebcam, None)
            return

        for vi in videoRange:
            videoDescription, videoName = videos[vi]
            print vi, videoDescription, videoName

            # sed videoname in c++ source code
            settingsFile = cfg["othr"]["sourceCodePrefix"]+"/jni/main_settings_testpy.cpp"
            sedCmd = "sed -i 's|\(^char\ fileName\[200\]\ =\ \"\)\(.*\)\(\";$\)|\\1%s\\3|' %s " % (videoName, settingsFile)
            os.system(sedCmd)

            annotFilename = os.path.splitext(videoName)[0]+".tag"
            annotFilename1 = os.path.splitext(videoName)[0]+".v1"
            if (os.path.isfile(annotFilename1)):
                annotFilename = annotFilename1
            if (not os.path.isfile(annotFilename)) and (not os.path.isfile(annotFilename1)):
                annotFilename = None

            if cfg["method"] == "farneback":
                fFlows, lBlinks, rBlinks, jBlinks, tracking = processVideo.processVideo(cfg, isWebcam, annotFilename)
            elif cfg["method"] == "templ":
                tCors, lBlinks, rBlinks, jBlinks, tracking = processVideo.processVideo(cfg, isWebcam, annotFilename)
            elif cfg["method"] == "blackpixels":
                bPixes, lBlinks, rBlinks, jBlinks, tracking = processVideo.processVideo(cfg, isWebcam, annotFilename)
            # reset processVideo's global variables
            reload(processVideo)
            outputFileName = VideoQueue.prepareOutputFileName(cfg["othr"]["codeDirectory"], cfg["othr"]["outputsPref"], videoName)
            if cfg["method"] == "farneback":
                VideoQueue.writeVideoResults(outputFileName, fFlows, lBlinks, rBlinks, jBlinks, tracking)
            elif cfg["method"] == "templ":
                VideoQueue.writeVideoResults(outputFileName, tCors, lBlinks, rBlinks, jBlinks, tracking)
            elif cfg["method"] == "blackpixels":
                VideoQueue.writeVideoResults(outputFileName, bPixes, lBlinks, rBlinks, jBlinks, tracking)
        return

    @staticmethod
    def readOutputsToVariables(cfg, outputFileName):
        if cfg["method"] == "farneback":
            methodVar = "fFlows"
        elif cfg["method"] == "templ":
            methodVar = "tCors"
        elif cfg["method"] == "blackpixels":
            methodVar = "bPixes"

        variablesMap = {0:methodVar, 1:"lBlinks", 2:"rBlinks", 3:"jBlinks", 4:"tracking"}
        varsDict = {}

        f = file(outputFileName, "rb")
        for index in sorted(variablesMap.keys()):
            line = f.readline()
            varsDict[variablesMap[index]] = eval(line)

        return varsDict
    rep = [
        "lprp",
        "tannot",
        "tlr",
        #"tpany",
        "tpboth",
        "tploro",
        #"many",
        "manyd",
        "manyr",
        #"mboth",
        "mbothd",
        "mbothr",
        #"mloro",
        "mlorod",
        "mloror",
        #"fpany",
        "fpboth",
        "fploro",
        # #"tprany",
        # "tprboth",
        # "tprloro",
        # #"fprany",
        # "fprboth",
        # "fprloro",
        #"sa",
        "sb",
    ]
    #rep = []
    @staticmethod
    def initOverallReport(cfg):
        fileName = cfg["othr"]["codeDirectory"] + cfg["othr"]["outputsPref"] + ("/overall_%s.tsv" % cfg["method"])
        # truncate the file or create it, if it doesn't exist yet
        title = "I\tC\tG\tL\tDesc\tFile path\t" # TODO total frames last time
        #title += "Ann\t"
        #title += "L tot\tL TP\tL mis\t"
        #title += "R tot\tR TP\tR mis\t"

        title += "I:"
        if "lprp" in VideoQueue.rep:
            title += "L%\tR%\t"
        title += "T:"
        if "tannot" in VideoQueue.rep:
            title += "A\t"
        if "tlr" in VideoQueue.rep:
            title += "L\tR\t"

        title += "TP:"
        if "tpany" in VideoQueue.rep:
            title += "A\t"
        if "tpboth" in VideoQueue.rep:
            title += "B\t"
        if "tploro" in VideoQueue.rep:
            title += "LO\tRO\t"
        title += "M:"
        if "many" in VideoQueue.rep:
            title += "A\t"
        if "manyd" in VideoQueue.rep:
            title += "Ad\t"
        if "manyr" in VideoQueue.rep:
            title += "Ar\t"
        if "mboth" in VideoQueue.rep:
            title += "B\t"
        if "mbothd" in VideoQueue.rep:
            title += "Bd\t"
        if "mbothr" in VideoQueue.rep:
            title += "Br\t"
        if "mloro" in VideoQueue.rep:
            title += "LO\tRO\t"
        if "mlorod" in VideoQueue.rep:
            title += "LOd\tROd\t"
        if "mloror" in VideoQueue.rep:
            title += "LOr\tROr\t"
        title += "FP:"
        if "fpany" in VideoQueue.rep:
            title += "A\t"
        if "fpboth" in VideoQueue.rep:
            title += "B\t"
        if "fploro" in VideoQueue.rep:
            title += "LO\tRO\t"

        title += "TP/:"
        if "tprany" in VideoQueue.rep:
            title += "A\t"
        if "tprboth" in VideoQueue.rep:
            title += "B\t"
        if "tprlr" in VideoQueue.rep:
            title += "L\tR\t"
        title += "FP/:"
        if "fprany" in VideoQueue.rep:
            title += "A\t"
        if "fprboth" in VideoQueue.rep:
            title += "B\t"
        if "fprloro" in VideoQueue.rep:
            title += "LO\tRO\t"
        #title += "M:L\tR\tB\tFL\tFR\tFB\t"

        title += "S:"
        if "sa" in VideoQueue.rep:
            title += "A\t"
        if "sb" in VideoQueue.rep:
            title += "B\t"

        title += "\n"
        file(fileName, "wb").write(title)
        return fileName

    @staticmethod
    def writeOverallReport(fileName, videoDescription, videoName, vi, annotsl, annots, varsDict, ppd):
        dc = Cmn.detectionCoverageF(annotsl, varsDict["lBlinks"], varsDict["rBlinks"], varsDict["jBlinks"])

        isChallenging = "U"
        hasGlasses = "U"
        if annots[3]["challenging"] == True:
            isChallenging = "Y"
        elif annots[3]["challenging"] == False:
            isChallenging = "N"
        if annots[3]["glasses"] == True:
            hasGlasses = "Y"
        elif annots[3]["glasses"] == False:
            hasGlasses = "N"
        if isChallenging == "Y":
            pass
            #return
        if hasGlasses == "Y":
            pass
            #return
        if (annots[3].has_key("length")):
            m, s = annots[3]["length"]/60, annots[3]["length"]%60
            #vLen = "%.0f %d:%2d" % (annots[3]["length"], m, s)
            vLen = "%d:%02d" % (m, s)
        else:
            vLen = ""
        # video desc, filepath
        line = "%d\t%s\t%s\t%s\t%s\t%s\t" % (vi, isChallenging, hasGlasses, vLen, videoDescription, videoName.split("/posnetki/")[1])

        if "lprp" in VideoQueue.rep:
            line += "%.2f\t%.2f\t" % (ppd["lPercent"], ppd["rPercent"])

        # total annot, left, right
        if "tannot" in VideoQueue.rep:
            line += "%i\t" % len(annotsl)
        if "tlr" in VideoQueue.rep:
            line += "%i\t%i\t" % (len(varsDict["lBlinks"]), len(varsDict["rBlinks"]))

        # tp a, b, lo, ro
        if "tpany" in VideoQueue.rep:
            line += "%i\t" % len(dc["aCaught"])
        if "tpboth" in VideoQueue.rep:
            line += "%i\t" % len(dc["bCaught"])
        if "tploro" in VideoQueue.rep:
            line += "%i\t%i\t" % (len(dc["loCaught"]), len(dc["roCaught"]))
        # miss a, b, lo, ro
        if "many" in VideoQueue.rep:
            line += "%i\t" % len(dc["aMissed"])
        if "manyd" in VideoQueue.rep:
            line += "%i\t" % len(ppd["aMissedByDisplacement"])
        if "manyr" in VideoQueue.rep:
            line += "%i\t" % len([x for x in dc["aMissed"] if not x in ppd["aMissedByDisplacement"]])
        if "mboth" in VideoQueue.rep:
            line += "%i\t" % len(dc["bMissed"])
        if "mbothd" in VideoQueue.rep:
            line += "%i\t" % len(ppd["bMissedByDisplacement"])
        if "mbothr" in VideoQueue.rep:
            line += "%i\t" % len([x for x in dc["bMissed"] if not x in ppd["bMissedByDisplacement"]])
        if "mloro" in VideoQueue.rep:
            line += "%i\t%i\t" % (len(dc["loMissed"]), len(dc["roMissed"]))
        if "mlorod" in VideoQueue.rep:
            line += "%i\t%i\t" % (len(ppd["loMissedByDisplacement"]), len(ppd["roMissedByDisplacement"]))
        if "mloror" in VideoQueue.rep:
            line += "%i\t%i\t" % (len([x for x in dc["loMissed"] if not x in ppd["loMissedByDisplacement"]]),
                                  len([x for x in dc["roMissed"] if not x in ppd["roMissedByDisplacement"]]))
        # fp (a, b, lo, ro)
        anyFp = len(dc["fpByOnlyL"])+len(dc["fpByOnlyR"])+len(dc["fpByBothEyes"])
        if "fpany" in VideoQueue.rep:
            line += "%i\t" % anyFp
        if "fpboth" in VideoQueue.rep:
            line += "%i\t" % len(dc["fpByBothEyes"])
        if "fploro" in VideoQueue.rep:
            line += "%i\t%i\t" % (len(dc["fpByOnlyL"]), len(dc["fpByOnlyR"]))

        # tp ratio a, b, l, r
        aTPRatio = 0 if len(annotsl) == 0 else len(dc["aCaught"])/float(len(annotsl))*100
        bTPRatio = 0 if len(annotsl) == 0 else len(dc["bCaught"])/float(len(annotsl))*100
        lTPRatio = 0 if len(annotsl) == 0 else len(dc["lCaught"])/float(len(annotsl))*100
        rTPRatio = 0 if len(annotsl) == 0 else len(dc["rCaught"])/float(len(annotsl))*100
        if "tprany" in VideoQueue.rep:
            line += "%.1f\t" % aTPRatio
        if "tprboth" in VideoQueue.rep:
            line += "%.1f\t" % bTPRatio
        if "tprlr" in VideoQueue.rep:
            line += "%.1f\t%.1f\t" % (lTPRatio, rTPRatio)

        # fp ratio a, b, l, r
        aFPRatio = anyFp if len(annotsl) == 0 else anyFp/float(len(annotsl))*100
        bFPRatio = len(dc["fpByBothEyes"]) if len(annotsl) == 0 else len(dc["fpByBothEyes"])/float(len(annotsl))*100
        loFPRatio = len(dc["fpByOnlyL"]) if len(annotsl) == 0 else len(dc["fpByOnlyL"])/float(len(annotsl))*100
        roFPRatio = len(dc["fpByOnlyR"]) if len(annotsl) == 0 else len(dc["fpByOnlyR"])/float(len(annotsl))*100
        if "fprany" in VideoQueue.rep:
            line += "%.2f\t" % aFPRatio
        if "fprboth" in VideoQueue.rep:
            line += "%.2f\t" % bFPRatio
        if "fprloro" in VideoQueue.rep:
            line += "%.2f\t%.2f\t" % (loFPRatio, roFPRatio)

        if "sa" in VideoQueue.rep:
            line += "%.2f\t" % (100-(100-aTPRatio)-aFPRatio)
        if "sb" in VideoQueue.rep:
            line += "%.2f\t" % (100-(100-bTPRatio)-bFPRatio)

        line += "\n"
        file(fileName, "ab").write(line)
        return



    repNum = 1
    @staticmethod
    def initOverallReportTable1(cfg):
        if VideoQueue.repNum == 1:
                VideoQueue.rept1 = [
            "Gla",
            "Len",
            "fileNam",
            "tannot",
            "tpboth",
            "tploro",
            "many",
            "manyd",
            #"mlorod",
            "tprboth",
            "titleTP/",
            "titleM",
            "fpboth",
            "fprboth",
        ]
        if VideoQueue.repNum == 2:
                VideoQueue.rept1 = [
            "fileNam",
            "tannot",
            "fpboth",
            #"fploro",
            "fprboth",
            #"titleTP/",
            #"titleS",
            #"sb",
        ]

        fileName = cfg["othr"]["codeDirectory"] + cfg["othr"]["outputsPref"] + ("/overall_%s.tex" % cfg["method"])

        space = " & "

        title = ""
        if "Gla" in VideoQueue.rept1:
            title += "O"+space+""
        if "Len" in VideoQueue.rept1:
            title += "D"+space+""
        if "fileNam" in VideoQueue.rept1:
            title += "Datoteka"+space+""

        if "titleI" in VideoQueue.rept1:
            title += "I:"
        if "lprp" in VideoQueue.rept1:
            title += "L%"+space+"R%"+space+""

        if "titleT" in VideoQueue.rept1:
            title += "T:"
        if "tannot" in VideoQueue.rept1:
            title += "A"+space+""
        if "tlr" in VideoQueue.rept1:
            title += "L"+space+"R"+space+""


        if "titleTP" in VideoQueue.rept1:
            title += "TP:"
        if "tpany" in VideoQueue.rept1:
            title += "A"+space+""
        if "tpboth" in VideoQueue.rept1:
            title += "O"+space+""
        if "tploro" in VideoQueue.rept1:
            title += "L"+space+"D"+space+""

        if "titleM" in VideoQueue.rept1:
            if "many" in VideoQueue.rept1:
                title += "Z"+space+""
            if "manyd" in VideoQueue.rept1:
                title += "Zd"+space+""
        if "manyr" in VideoQueue.rept1:
            title += "Ar"+space+""
        if "mboth" in VideoQueue.rept1:
            title += "B"+space+""
        if "mbothd" in VideoQueue.rept1:
            title += "Bd"+space+""
        if "mbothr" in VideoQueue.rept1:
            title += "Br"+space+""
        if "mloro" in VideoQueue.rept1:
            title += "LO"+space+"RO"+space+""
        if "mlorod" in VideoQueue.rept1:
            title += "Ld"+space+"Rd"+space+""
        if "mloror" in VideoQueue.rept1:
            title += "Lr"+space+"Rr"+space+""

        if "titleTP/" in VideoQueue.rept1:
            title += "PZ \\%"+space+""
        if "tprany" in VideoQueue.rept1:
            title += "A"+space+""
        if "tprlr" in VideoQueue.rept1:
            title += "L"+space+"R"+space+""

        if "titleFP" in VideoQueue.rept1:
            title += "FP:"
        if "fpany" in VideoQueue.rept1:
            title += "A"+space+""
        if "fpboth" in VideoQueue.rept1:
            title += "NZ"+space+""
        if "fploro" in VideoQueue.rept1:
            title += "LO"+space+"RO"+space+""

        if "titleFP/" in VideoQueue.rept1:
            title += "FP/:"
        if "fprany" in VideoQueue.rept1:
            title += "A"+space+""
        if "fprboth" in VideoQueue.rept1:
            title += "NZ \\%"+space+""
        if "fprloro" in VideoQueue.rept1:
            title += "LO"+space+"RO"+space+""
        #title += "M:L"+space+"R"+space+"B"+space+"FL"+space+"FR"+space+"FB"+space+""
        if "sa" in VideoQueue.rept1:
            title += "A"+space+""
        if "sb" in VideoQueue.rept1:
            title += "S \\%"+space+""

        title = title.rstrip(space)

        title += " \\\\ \\hline\n"

        file(fileName, "wb").write(title)
        return fileName

    @staticmethod
    def writeOverallReportTable1(fileName, videoDescription, videoName, vi, annotsl, annots, varsDict, ppd):
        dc = Cmn.detectionCoverageF(annotsl, varsDict["lBlinks"], varsDict["rBlinks"], varsDict["jBlinks"])

        # tp ratio a, b, l, r
        aTPRatio = 0 if len(annotsl) == 0 else len(dc["aCaught"])/float(len(annotsl))*100
        bTPRatio = 0 if len(annotsl) == 0 else len(dc["bCaught"])/float(len(annotsl))*100
        lTPRatio = 0 if len(annotsl) == 0 else len(dc["lCaught"])/float(len(annotsl))*100
        rTPRatio = 0 if len(annotsl) == 0 else len(dc["rCaught"])/float(len(annotsl))*100

        space = " & "
        nl = " \\\\\n"

        isChallenging = "?"
        hasGlasses = "?"

        if annots[3]["challenging"] == True:
            isChallenging = "D"
        elif annots[3]["challenging"] == False:
            isChallenging = "N"
        if annots[3]["glasses"] == True:
            hasGlasses = "D"
        elif annots[3]["glasses"] == False:
            hasGlasses = "N"
        if isChallenging == "Y":
            pass
            #return
        if hasGlasses == "Y":
            pass
            #return
        if (annots[3].has_key("length")):
            m, s = annots[3]["length"]/60, annots[3]["length"]%60
            #vLen = "%.0f %d:%2d" % (annots[3]["length"], m, s)
            vLen = "%d:%02d" % (m, s)
        else:
            vLen = ""

        line = ""
        if "Gla" in VideoQueue.rept1:
            line += ("%s"+space) % hasGlasses
        if "Len" in VideoQueue.rept1:
            line += ("%s"+space) % vLen
        if "fileNam" in VideoQueue.rept1:
            fn = videoName.split("/posnetki/")[1].split("/")[-1]
            fn = os.path.splitext(fn)[0]
            fn = fn.replace("_x263", "")
            fn = fn.replace("_", "\\_")
            line += ("%s"+space) % fn


        if "lprp" in VideoQueue.rept1:
            line += ("%.2f"+space+"%.2f"+space+"") % (ppd["lPercent"], ppd["rPercent"])

        # total annot, left, right
        if "tannot" in VideoQueue.rept1:
            line += ("%i"+space+"") % len(annotsl)
        if "tlr" in VideoQueue.rept1:
            line += ("%i"+space+"%i"+space+"") % (len(varsDict["lBlinks"]), len(varsDict["rBlinks"]))

        # tp a, b, lo, ro
        if "tpany" in VideoQueue.rept1:
            line += ("%i"+space+"") % len(dc["aCaught"])
        if "tpboth" in VideoQueue.rept1:
            line += ("%i"+space+"") % len(dc["bCaught"])
        if "tploro" in VideoQueue.rept1:
            line += ("%i"+space+"%i"+space+"") % (len(dc["loCaught"]), len(dc["roCaught"]))
        # miss a, b, lo, ro
        if "many" in VideoQueue.rept1:
            line += ("%i"+space+"") % len(dc["aMissed"])
        if "manyd" in VideoQueue.rept1:
            line += ("%i"+space+"") % len(ppd["aMissedByDisplacement"])
        if "manyr" in VideoQueue.rept1:
            line += ("%i"+space+"") % len([x for x in dc["aMissed"] if not x in ppd["aMissedByDisplacement"]])
        if "mboth" in VideoQueue.rept1:
            line += ("%i"+space+"") % len(dc["bMissed"])
        if "mbothd" in VideoQueue.rept1:
            line += ("%i"+space+"") % len(ppd["bMissedByDisplacement"])
        if "mbothr" in VideoQueue.rept1:
            line += ("%i"+space+"") % len([x for x in dc["bMissed"] if not x in ppd["bMissedByDisplacement"]])
        if "mloro" in VideoQueue.rept1:
            line += ("%i"+space+"%i"+space+"") % (len(dc["loMissed"]), len(dc["roMissed"]))
        if "mlorod" in VideoQueue.rept1:
            line += ("%i"+space+"%i"+space+"") % (len(ppd["loMissedByDisplacement"]), len(ppd["roMissedByDisplacement"]))
        if "mloror" in VideoQueue.rept1:
            line += ("%i"+space+"%i"+space+"") % (len([x for x in dc["loMissed"] if not x in ppd["loMissedByDisplacement"]]),
                                  len([x for x in dc["roMissed"] if not x in ppd["roMissedByDisplacement"]]))

        # tp ratio a, b, l, r
        if "tprany" in VideoQueue.rept1:
            line += ("%.1f"+space+"") % aTPRatio
        if "tprboth" in VideoQueue.rept1:
            line += ("%.1f"+space+"") % bTPRatio
        if "tprlr" in VideoQueue.rept1:
            line += ("%.1f"+space+"%.1f"+space+"") % (lTPRatio, rTPRatio)

        # fp (a, b, lo, ro)
        anyFp = len(dc["fpByOnlyL"])+len(dc["fpByOnlyR"])+len(dc["fpByBothEyes"])
        if "fpany" in VideoQueue.rept1:
            line += ("%i"+space+"") % anyFp
        if "fpboth" in VideoQueue.rept1:
            line += ("%i"+space+"") % len(dc["fpByBothEyes"])
        if "fploro" in VideoQueue.rept1:
            line += ("%i"+space+"%i"+space+"") % (len(dc["fpByOnlyL"]), len(dc["fpByOnlyR"]))


        # fp ratio a, b, l, r
        aFPRatio = anyFp if len(annotsl) == 0 else anyFp/float(len(annotsl))*100
        bFPRatio = len(dc["fpByBothEyes"]) if len(annotsl) == 0 else len(dc["fpByBothEyes"])/float(len(annotsl))*100
        loFPRatio = len(dc["fpByOnlyL"]) if len(annotsl) == 0 else len(dc["fpByOnlyL"])/float(len(annotsl))*100
        roFPRatio = len(dc["fpByOnlyR"]) if len(annotsl) == 0 else len(dc["fpByOnlyR"])/float(len(annotsl))*100
        if "fprany" in VideoQueue.rept1:
            line += ("%.2f"+space+"") % aFPRatio
        if "fprboth" in VideoQueue.rept1:
            line += ("%.2f"+space+"") % bFPRatio
        if "fprloro" in VideoQueue.rept1:
            line += ("%.2f"+space+"%.2f"+space+"") % (loFPRatio, roFPRatio)

        if "sa" in VideoQueue.rept1:
            line += ("%.2f"+space+"") % (100-(100-aTPRatio)-aFPRatio)
        if "sb" in VideoQueue.rept1:
            line += ("%.2f"+space+"") % (100-(100-bTPRatio)-bFPRatio)

        line = line.rstrip(space)
        line += (""+nl+"")

        file(fileName, "ab").write(line)
        return


    # @staticmethod
    # def calculateTrackingCoverage(methodTracks, annotTracks):
    #     trackableFrames = 0
    #     trackedFrames = 0
    #     missedRanges = []
    #     for annotTrack in annotTracks["track"]:
    #         lastAddedStart, lastAddedStop = -1, -1
    #         aStart, aStop = annotTrack[0][1], annotTrack[1][1]
    #         trackableFrames += (aStop-aStart)

    #         for methodTrack in methodTracks["detecting"]:
    #             if len(methodTrack) != 2:
    #                 print "foobar", repr(methodTrack)
    #                 continue
    #             mStart, mStop = methodTrack[0][1], methodTrack[1][1]
    #             addStart, addStop = -1, -1
    #             if mStart <= aStart and (aStart <= mStop and mStop <= aStop):
    #                 addStart, addStop = aStart, mStop
    #             elif aStart <= mStart and mStop <= aStop:
    #                 addStart, addStop = mStart, mStop
    #             elif (aStart <= mStart and mStart <= aStop) and aStop < mStop:
    #                 addStart, addStop = mStart, aStop
    #             elif mStart <= aStart and aStop <= mStop:
    #                 addStart, addStop = aStart, aStop

    #             if addStart != -1 and addStop != -1:
    #                 trackedFrames += (addStop-addStart)
    #                 if lastAddedStart == -1 and lastAddedStop == -1:
    #                     print "here once?"
    #                     if addStart != aStart:
    #                         missedRanges.append((aStart, addStart-1))
    #                 else:
    #                     print "here multiple times?"
    #                     if (addStart-lastAddedStop) > 1:
    #                         missedRanges.append((lastAddedStop+1, addStart-1))
    #                 lastAddedStart, lastAddedStop = addStart, addStop
    #     if lastAddedStop != aStop:
    #         missedRanges.append((lastAddedStop+1, aStop))
    #     print "missedRanges", missedRanges


    #     print repr(methodTracks)
    #     print repr(annotTracks)
    #     print "trackedFrames", trackedFrames, "trackableFrames",trackableFrames
    #     return

    @staticmethod
    def processOutputs(cfg, videos, videoRange, actions):
        #videoRange = videoRange[:1]

        if "writeOverallReport" in actions:
            reportFileName = VideoQueue.initOverallReport(cfg)
            reportFileNameT1 = VideoQueue.initOverallReportTable1(cfg)

        for vi in videoRange:
            videoDescription, videoName = videos[vi]
            print vi, videoDescription, videoName

            outputFileName = VideoQueue.prepareOutputFileName(cfg["othr"]["codeDirectory"], cfg["othr"]["outputsPref"], videoName)
            try:
                varsDict = VideoQueue.readOutputsToVariables(cfg, outputFileName)
            except IOError, e:
                print "breaking"
                print traceback.format_exc()
                break
            if "postProcessLogLine" in actions or "displayDetectionCoverage" in actions or "writeOverallReport" in actions or "displayPupilDisplacement" in actions or "postProcessTracking" in actions:
                #if cfg["method"] == "farneback":
                    annotFilename = os.path.splitext(videoName)[0]+".tag"
                    annotFilenameL = os.path.splitext(videoName)[0]+".txt"
                    annotFilename1 = os.path.splitext(videoName)[0]+".v1"
                    if os.path.isfile(annotFilename):
                        annotsl, annots = Cmn.parseAnnotations(file(annotFilename), None, "farne")
                        if os.path.isfile(annotFilenameL):
                            videoLen = float(file(annotFilenameL, "rb").read().strip().split("\n")[-1].split(" ")[1])
                            annots[-1]["length"] = videoLen
                        else:
                            annots[-1]["length"] = -1
                    elif os.path.isfile(annotFilename1):
                        annotsl, annots = Cmn.parseAnnotationsMy(file(annotFilename1), None, "farne")
                        if "poli1person10" in annotFilename1:
                            annots[-1]["glasses"] = True
                        else:
                            annots[-1]["glasses"] = False
                        if os.path.isfile(annotFilenameL):
                            videoLenS = float(file(annotFilenameL, "rb").read().strip().split("\n")[0].split(" ")[1])
                            videoLenE = float(file(annotFilenameL, "rb").read().strip().split("\n")[-1].split(" ")[1])
                            annots[-1]["length"] = (videoLenE-videoLenS)
                        else:
                            annots[-1]["length"] = -1
            if "displayDetectionCoverage" in actions:
                if cfg["method"] == "farneback":
                    dc = Cmn.detectionCoverageF(annotsl, varsDict["lBlinks"], varsDict["rBlinks"], varsDict["jBlinks"])
                    Cmn.displayDetectionCoverageF1(dc, annotsl)
                    pass
                    #Cmn.displayDetectionCoverage(varsDict["l"], varsDict["r"], varsDict["o"])
                elif cfg["method"] == "templ":
                    pass
                elif cfg["method"] == "blackpixels":
                    pass
            if "signalProcessing" in actions:
                #print repr(varsDict["tCors"])
                print repr([x["fn"] for x in varsDict["tCors"]])
                print
                print
                print repr([x["lcor"] for x in varsDict["tCors"]])
                print
                print
                print repr([x["rcor"] for x in varsDict["tCors"]])
                pass
            if "writeOverallReport" in actions:
                dc = Cmn.detectionCoverageF(annotsl, varsDict["lBlinks"], varsDict["rBlinks"], varsDict["jBlinks"])
                ppd = Farne.processPupilDisplacement(varsDict["tracking"], dc, annotsl, annots)
                VideoQueue.writeOverallReport(reportFileName, videoDescription, videoName, vi, annotsl, annots, varsDict, ppd)
                VideoQueue.writeOverallReportTable1(reportFileNameT1, videoDescription, videoName, vi, annotsl, annots, varsDict, ppd)
            if "postProcessLogLine" in actions:
                if cfg["method"] == "farneback":
                    dc = Cmn.detectionCoverageF(annotsl, varsDict["lBlinks"], varsDict["rBlinks"], varsDict["jBlinks"])
                    Farne.postProcessLogLine(varsDict["fFlows"], varsDict["lBlinks"], varsDict["rBlinks"], varsDict["jBlinks"], True, dc, varsDict["tracking"])
                elif cfg["method"] == "templ":
                    Templ.postProcessLogLine(varsDict["tCors"], varsDict["lBlinks"], varsDict["rBlinks"], varsDict["jBlinks"], True)
                elif cfg["method"] == "blackpixels":
                    Blackpixels.postProcessLogLine(varsDict["bPixes"], varsDict["lBlinks"], varsDict["rBlinks"], varsDict["jBlinks"], True)
            if "displayPupilDisplacement" in actions:
                if cfg["method"] == "farneback":
                    dc = Cmn.detectionCoverageF(annotsl, varsDict["lBlinks"], varsDict["rBlinks"], varsDict["jBlinks"])
                    ppd = Farne.processPupilDisplacement(varsDict["tracking"], dc, annotsl, annots)
                    Farne.displayPupilDisplacement(ppd)
        return

