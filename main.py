import os
import processVideo

def processVideoQueue(cfg):
    #videoName = "o44" # doma
    #videoName = "o89" # knjiznica 40s
    #videoName = "o90" # premikal glavo, zadej luc
    vidPrefix = "/home/developer/other/posnetki/"
    sourceCodePrefix = "/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/optical-flow"
    isWebcam = False

    if isWebcam == True:
        fFlows, lBlinks, rBlinks, l, r, o = processVideo.processVideo(cfg, isWebcam, None)
        return

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
    for vi in videoRange:
        videoName = videos[vi]
        # sed videoname in c++ source code
        settingsFile = sourceCodePrefix+"/jni/main_settings_testpy.cpp"
        sedCmd = "sed -i 's|\(^char\ fileName\[100\]\ =\ \"\)\(.*\)\(\";$\)|\\1%s\\3|' %s " % (videoName, settingsFile)
        os.system(sedCmd)

        annotFilename = os.path.splitext(videoName)[0]+".tag"
        if not os.path.isfile(annotFilename):
            annotFilename = None

        fFlows, lBlinks, rBlinks, l, r, o = processVideo.processVideo(cfg, isWebcam, annotFilename)
    return



def main():
    cfg = {
        "excel_export": True,
        "coverage":     True,
        "end_hook":     True,
        #"method": "blackpixels",
        "method": "farneback",
        #"method": "templ",
    }

    outputs = "vidProcOutputs"
    processVideoQueue(cfg)

    return



if __name__ == "__main__":
    main()
