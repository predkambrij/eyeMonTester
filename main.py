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
        print videoName

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
        outputFileName = prepareOutputFileName(cfg["othr"]["codeDirectory"], cfg["othr"]["outputsPref"], videoName)
        writeVideoResults(outputFileName, fFlows, lBlinks, rBlinks, l, r, o)
    return

#############################################
def prepareVideosList(cfg):
    #videoName = "o44" # doma
    #videoName = "o89" # knjiznica 40s
    #videoName = "o90" # premikal glavo, zadej luc
    vidPrefix = cfg["othr"]["vidPrefix"]
    eyeblink8 = [
        # punca od dalec
        vidPrefix+"sk/eyeblink8/1/26122013_223310_cam.avi",

        vidPrefix+"sk/eyeblink8/2/26122013_224532_cam.avi",
        vidPrefix+"sk/eyeblink8/3/26122013_230103_cam.avi",
        vidPrefix+"sk/eyeblink8/4/26122013_230654_cam.avi",
        vidPrefix+"sk/eyeblink8/8/27122013_151644_cam.avi",
        vidPrefix+"sk/eyeblink8/9/27122013_152435_cam.avi",
        vidPrefix+"sk/eyeblink8/10/27122013_153916_cam.avi",
        vidPrefix+"sk/eyeblink8/11/27122013_154548_cam.avi",
    ]
    others = [
        # full partial
        vidPrefix+"sk/NightOfResearchers15/test/14/26092014_211047_cam.avi",
        # talking
        vidPrefix+"talking.avi",
    ]
    #videos = others+eyeblink8
    videos = eyeblink8+others
    videoRange = range(len(videos)) #[0, 1, 2]
    #videoRange = xrange(len(videos))
    return videos, videoRange

def getConfigs():
    return {
        "excel_export": False,
        "coverage":     False,
        "end_hook":     False,
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
