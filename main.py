import os
import processVideo


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

    #videoName = "o44" # doma
    #videoName = "o89" # knjiznica 40s
    #videoName = "o90" # premikal glavo, zadej luc
    vidPrefix = "/home/developer/other/posnetki/"


    vidNum = 1
    isWebcam = False
    if vidNum == 0:
        isWebcam = True
        videoName = ""
    elif vidNum == 1:
        vidPrefix += "sk/eyeblink8/1/" # punca od dalec
        videoName = "26122013_223310_cam.avi"
    elif vidNum == 2:
        vidPrefix += "sk/NightOfResearchers15/test/14/" # full partial
        videoName = "26092014_211047_cam.avi"
    elif vidNum == 3:
        videoName = "talking.avi"

    videoAnnot = os.path.splitext(videoName)[0]+".tag"

    stateVariables = {"lBlinks":[], "rBlinks":[],
        "tCors":[], "fFlows":[], "bPixes":[],
        "fFlowsI":{},
    }
    processVideo.processVideo(cfg, stateVariables, isWebcam, vidPrefix, videoAnnot)
    return



if __name__ == "__main__":
    main()
