import os
import processVideo

def prepareOutputFileName(codeDirectory, outputPrefix, videoName):
    videoDir, videoFile = os.path.split(videoName)
    videoBase, videoExt = os.path.splitext(videoFile)
    outputFileDir = codeDirectory+outputPrefix+videoDir
    outputFileName = outputFileDir+"/"+videoBase+".out"

    if not os.path.exists(outputFileDir):
        os.makedirs(outputFileDir)
    return outputFileName

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

def writeOverallReport():
    return

def processVideoQueue(cfg):
    isWebcam = False
    if isWebcam == True:
        fFlows, lBlinks, rBlinks, l, r, o = processVideo.processVideo(cfg, isWebcam, None)
        return

    videos, videoRange = prepareVideosList(cfg)
    for vi in videoRange:
        videoName = videos[vi]
        # sed videoname in c++ source code
        settingsFile = cfg["othr"]["sourceCodePrefix"]+"/jni/main_settings_testpy.cpp"
        sedCmd = "sed -i 's|\(^char\ fileName\[100\]\ =\ \"\)\(.*\)\(\";$\)|\\1%s\\3|' %s " % (videoName, settingsFile)
        os.system(sedCmd)

        annotFilename = os.path.splitext(videoName)[0]+".tag"
        if not os.path.isfile(annotFilename):
            annotFilename = None

        fFlows, lBlinks, rBlinks, l, r, o = processVideo.processVideo(cfg, isWebcam, annotFilename)
        outputFileName = prepareOutputFileName(cfg["othr"]["codeDirectory"], cfg["othr"]["outputsPref"], videoName)
        writeVideoResults(outputFileName, fFlows, lBlinks, rBlinks, l, r, o)
    return

def prepareVideosList(cfg):
    #videoName = "o44" # doma
    #videoName = "o89" # knjiznica 40s
    #videoName = "o90" # premikal glavo, zadej luc
    vidPrefix = cfg["othr"]["vidPrefix"]
    videos = [
        # 0 punca od dalec
        vidPrefix+"sk/eyeblink8/1/26122013_223310_cam.avi",
        # 1 full partial
        vidPrefix+"sk/NightOfResearchers15/test/14/26092014_211047_cam.avi",
        # 2 talking
        vidPrefix+"talking.avi",
    ]
    videoRange = [0]
    #videoRange = xrange(len(videos))
    return videos, videoRange

def getConfigs():
    return {
        "excel_export": True,
        "coverage":     True,
        "end_hook":     True,
        #"method": "blackpixels",
        "method": "farneback",
        #"method": "templ",
        "othr" : {
            "vidPrefix":"/home/developer/other/posnetki/",
            "sourceCodePrefix":"/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/optical-flow",
            "codeDirectory":"/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/test_runner",

            #"outputsPref":"/vidProcOutputs",
            "outputsPref":"/vidProcOutputs/ver1",
        }
    }
def main():
    cfg = getConfigs()
    processVideoQueue(cfg)

    return



if __name__ == "__main__":
    main()
