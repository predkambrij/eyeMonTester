import os
import processVideo
from common import Common as Cmn
from farne import Farne

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
    def writeVideoResults(outputFileName, fFlows, lBlinks, rBlinks, l, r, o):
        f = file(outputFileName, "wb")
        f.write(repr(fFlows)+"\n")
        f.write(repr(lBlinks)+"\n")
        f.write(repr(rBlinks)+"\n")
        f.write(repr(l)+"\n")
        f.write(repr(r)+"\n")
        f.write(repr(o)+"\n")
        f.close()
        return

    @staticmethod
    def processVideoQueue(cfg, videos, videoRange):
        isWebcam = False
        if isWebcam == True:
            fFlows, lBlinks, rBlinks, l, r, o = processVideo.processVideo(cfg, isWebcam, None)
            return

        for vi in videoRange:
            videoDescription, videoName = videos[vi]
            print videoDescription, videoName

            # sed videoname in c++ source code
            settingsFile = cfg["othr"]["sourceCodePrefix"]+"/jni/main_settings_testpy.cpp"
            sedCmd = "sed -i 's|\(^char\ fileName\[100\]\ =\ \"\)\(.*\)\(\";$\)|\\1%s\\3|' %s " % (videoName, settingsFile)
            os.system(sedCmd)

            annotFilename = os.path.splitext(videoName)[0]+".tag"
            if not os.path.isfile(annotFilename):
                annotFilename = None

            fFlows, lBlinks, rBlinks, l, r, o = processVideo.processVideo(cfg, isWebcam, annotFilename)
            # reset processVideo's global variables
            reload(processVideo)
            outputFileName = VideoQueue.prepareOutputFileName(cfg["othr"]["codeDirectory"], cfg["othr"]["outputsPref"], videoName)
            VideoQueue.writeVideoResults(outputFileName, fFlows, lBlinks, rBlinks, l, r, o)
        return

    @staticmethod
    def readOutputsToVariables(outputFileName):
        variablesMap = {0:"fFlows", 1:"lBlinks", 2:"rBlinks", 3:"l", 4:"r", 5:"o"}
        varsDict = {}

        index = 0
        for line in file(outputFileName, "rb"):
            varsDict[variablesMap[index]] = eval(line)
            index += 1

        return varsDict

    @staticmethod
    def initOverallReport(cfg):
        fileName = cfg["othr"]["codeDirectory"] + cfg["othr"]["outputsPref"] + "/overall.tsv"
        # truncate the file or create it, if it doesn't exist yet
        title = "Description\tFile path\t"
        #title += "Ann\t"
        #title += "L tot\tL TP\tL mis\t"
        #title += "R tot\tR TP\tR mis\t"

        title += "T:A\tL\tR\t"
        title += "TP:A\tB\tLO\tRO\t"
        title += "M:A\tB\tLO\tRO\t"
        title += "FP:L\tR\tLO\tRO\tB\tAll\t"

        title += "TP/:L\tR\t"
        title += "FP/:L\tR\t"

        title += "\n"
        file(fileName, "wb").write(title)
        return fileName

    @staticmethod
    def writeOverallReport(fileName, videoDescription, videoName, varsDict):
        annotFilename = os.path.splitext(videoName)[0]+".tag"
        if not os.path.isfile(annotFilename):
            return
        annotsl, annots = Cmn.parseAnnotations(file(annotFilename), None, "farne")
        dc = Cmn.detectionCoverageF(annotsl, varsDict["lBlinks"], varsDict["rBlinks"])

        # video desc, filepath
        line = "%s\t%s\t" % (videoDescription, videoName.split("/posnetki/")[1])
        # total annot, left, right
        line += "%i\t%i\t%i\t" % (len(annotsl), len(varsDict["lBlinks"]), len(varsDict["rBlinks"]))
        # tp a, b, lo, ro
        line += "%i\t%i\t%i\t%i\t" % (len(dc["aCaught"]), len(dc["bCaught"]), len(dc["loCaught"]), len(dc["roCaught"]))
        # miss a, b, lo, ro
        line += "%i\t%i\t%i\t%i\t" % (len(dc["aMissed"]), len(dc["bMissed"]), len(dc["loMissed"]), len(dc["roMissed"]))
        # fp (l, r, lo, ro, b, all)
        line += "%i\t%i\t%i\t%i\t" % (len(dc["lFp"]), len(dc["rFp"]), len(dc["fpByOnlyL"]), len(dc["fpByOnlyR"]))
        # fp (b, all)
        line += "%i\t%i\t" % (len(dc["fpByBothEyes"]), len(dc["fpByOnlyL"])+len(dc["fpByOnlyR"])+len(dc["fpByBothEyes"]))

        lTPRatio = 0 if len(annotsl) == 0 else len(dc["lCaught"])/float(len(annotsl))*100
        lFPRatio = len(dc["lFp"]) if len(annotsl) == 0 else len(dc["lFp"])/float(len(annotsl))*100
        rTPRatio = 0 if len(annotsl) == 0 else len(dc["rCaught"])/float(len(annotsl))*100
        rFPRatio = len(dc["rFp"]) if len(annotsl) == 0 else len(dc["rFp"])/float(len(annotsl))*100
        bTPRatio = 0 if len(annotsl) == 0 else len(dc["bCaught"])/float(len(annotsl))*100
        aTPRatio = 0 if len(annotsl) == 0 else len(dc["aCaught"])/float(len(annotsl))*100

        line += "%.2f\t%.2f\t" % (lTPRatio, rTPRatio)
        line += "%.2f\t%.2f\t" % (lFPRatio, rFPRatio)
        line += "\n"
        file(fileName, "ab").write(line)
        return

    @staticmethod
    def processOutputs(cfg, videos, videoRange, actions):
        #videoRange = videoRange[:1]

        if "writeOverallReport" in actions:
            reportFileName = VideoQueue.initOverallReport(cfg)

        for vi in videoRange:
            videoDescription, videoName = videos[vi]
            print videoDescription, videoName

            outputFileName = VideoQueue.prepareOutputFileName(cfg["othr"]["codeDirectory"], cfg["othr"]["outputsPref"], videoName)
            if cfg["method"] == "farneback":
                varsDict = VideoQueue.readOutputsToVariables(outputFileName)

            if "displayDetectionCoverage" in actions:
                Cmn.displayDetectionCoverage(varsDict["l"], varsDict["r"], varsDict["o"])
            if "postProcessLogLine" in actions:
                Farne.postProcessLogLine(varsDict["fFlows"], varsDict["lBlinks"], varsDict["rBlinks"], True)
            if "writeOverallReport" in actions:
                VideoQueue.writeOverallReport(reportFileName, videoDescription, videoName, varsDict)
        return

