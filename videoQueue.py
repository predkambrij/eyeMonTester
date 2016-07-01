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
    def initOverallReport():
        return

    @staticmethod
    def writeOverallReport():
        return

    @staticmethod
    def processOutputs(cfg, videos, videoRange, actions):
        #videoRange = videoRange[:1]

        if "writeOverallReport" in actions:

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
                    VideoQueue.writeOverallReport()
        return

