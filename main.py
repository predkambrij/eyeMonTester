from videoQueue import VideoQueue

def prepareVideosList(cfg):
    #videoName = "o44" # doma
    #videoName = "o89" # knjiznica 40s
    #videoName = "o90" # premikal glavo, zadej luc
    vidPrefix = cfg["othr"]["vidPrefix"]
    eyeblink8 = [
        vidPrefix+"sk/eyeblink8/1/26122013_223310_cam.avi", # punca od dalec
        vidPrefix+"sk/eyeblink8/3/26122013_230103_cam.avi",
        vidPrefix+"sk/eyeblink8/8/27122013_151644_cam.avi",
        vidPrefix+"sk/eyeblink8/9/27122013_152435_cam.avi",
        vidPrefix+"sk/eyeblink8/10/27122013_153916_cam.avi",
        vidPrefix+"sk/eyeblink8/11/27122013_154548_cam.avi",
    ]
    eyeblink8HandInTheFirstFrames = [
        vidPrefix+"sk/eyeblink8/2/26122013_224532_cam.avi",
        vidPrefix+"sk/eyeblink8/4/26122013_230654_cam.avi",
    ]
    others = [
        # full partial
        vidPrefix+"sk/NightOfResearchers15/test/14/26092014_211047_cam.avi",
        # talking
        vidPrefix+"talking.avi",
    ]
    videos = others+eyeblink8HandInTheFirstFrames+eyeblink8
    #videoRange = range(len(videos))
    videoRange = [0]
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
            "outputsPref":"/vidProcOutputs/verTest",
        }
    }

def main():
    cfg = getConfigs()
    videos, videoRange = prepareVideosList(cfg)

    VideoQueue.processVideoQueue(cfg, videos, videoRange)
    return


if __name__ == "__main__":
    main()
