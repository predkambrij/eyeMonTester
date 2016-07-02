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
        title += "TP:L\tR\tB\tA\t"
        title += "M:L\tR\tB\tA\t"
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
        l, r, o = Cmn.detectionCoverageF(annotsl, varsDict["lBlinks"], varsDict["rBlinks"])

        # video desc, filepath
        line = "%s\t%s\t" % (videoDescription, videoName.split("/posnetki/")[1])
        # total annot, left, right
        line += "%i\t%i\t%i\t" % (len(annotsl), len(l[0]), len(r[0]))
        # tp l, r, b, a
        line += "%i\t%i\t%i\t%i\t" % (len(l[1]), len(r[1]), len(o[0]), len(o[2]))
        # miss left, right, both, any
        line += "%i\t%i\t%i\t%i\t" % (len(l[2]), len(r[2]), len(o[1]), len(o[3]))
        # fp (l, r, lo, ro, b, all)
        line += "%i\t%i\t%i\t%i\t%i\t%i\t" % (len(l[3]), len(r[3]), len(o[5]), len(o[6]), len(o[4]), len(o[5])+len(o[6])+len(o[4]))

        lTPRatio = 0 if len(annotsl) == 0 else len(l[1])/float(len(annotsl))*100
        lFPRatio = len(l[3]) if len(annotsl) == 0 else len(l[3])/float(len(annotsl))*100
        rTPRatio = 0 if len(annotsl) == 0 else len(r[1])/float(len(annotsl))*100
        rFPRatio = len(r[3]) if len(annotsl) == 0 else len(r[3])/float(len(annotsl))*100
        bTPRatio = 0 if len(annotsl) == 0 else len(o[0])/float(len(annotsl))*100
        aTPRatio = 0 if len(annotsl) == 0 else len(o[2])/float(len(annotsl))*100

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

