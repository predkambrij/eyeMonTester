from videoQueue import VideoQueue

def prepareVideosList(cfg):
    #videoName = "o44" # doma
    #videoName = "o89" # knjiznica 40s
    #videoName = "o90" # premikal glavo, zadej luc
    vidPrefix = cfg["othr"]["vidPrefix"]
    eyeblink8 = [
        ("punca od dalec", vidPrefix+"sk/eyeblink8/1/26122013_223310_cam.avi"),
        ("fant gleda neki", vidPrefix+"sk/eyeblink8/3/26122013_230103_cam.avi"),
        ("", vidPrefix+"sk/eyeblink8/8/27122013_151644_cam.avi"),
        ("", vidPrefix+"sk/eyeblink8/9/27122013_152435_cam.avi"),
        ("bere neki, dobra slika", vidPrefix+"sk/eyeblink8/10/27122013_153916_cam.avi"),
        ("", vidPrefix+"sk/eyeblink8/11/27122013_154548_cam.avi"),
    ]
    eyeblink8HandInTheFirstFrames = [
        ("", vidPrefix+"sk/eyeblink8/2/26122013_224532_cam.avi"),
        ("", vidPrefix+"sk/eyeblink8/4/26122013_230654_cam.avi"),
    ]
    nightOfResearchers30 = [
        ("", vidPrefix+"sk/NightOfResearchers30/test/1/26092014_161749_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/10/26092014_173024_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/11/26092014_173630_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/12/26092014_175943_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/13/26092014_181011_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/14/26092014_182857_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/15/26092014_111716_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/16/26092014_183734_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/17/26092014_121151_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/18/26092014_184632_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/19/26092014_185952_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/2/26092014_150500_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/20/26092014_134306_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/21/26092014_191620_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/22/26092014_194520_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/23/26092014_195901_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/24/26092014_200714_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/25/26092014_201130_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/26/26092014_203937_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/27/26092014_204339_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/28/26092014_141144_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/29/26092014_210427_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/3/26092014_160051_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/30/26092014_125304_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/31/26092014_133722_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/32/26092014_130857_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/33/26092014_134925_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/34/26092014_142548_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/35/26092014_161141_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/4/26092014_163504_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/5/26092014_164703_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/6/26092014_164731_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/7/26092014_105214_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/8/26092014_141058_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/test/9/26092014_172120_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/1/26092014_113824_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/10/26092014_195612_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/11/26092014_144314_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/12/26092014_130620_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/13/26092014_204644_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/14/26092014_133535_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/15/26092014_134156_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/16/26092014_181133_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/17/26092014_160056_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/2/26092014_175010_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/3/26092014_133821_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/4/26092014_185440_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/5/26092014_191449_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/6/26092014_121842_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/7/26092014_192316_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/8/26092014_192746_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/train/9/26092014_195001_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/1/26092014_133154_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/10/26092014_122529_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/11/26092014_200204_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/12/26092014_122600_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/13/26092014_201335_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/14/26092014_203825_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/15/26092014_204844_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/16/26092014_211251_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/17/26092014_130017_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/2/26092014_162458_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/3/26092014_161025_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/4/26092014_171745_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/5/26092014_174355_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/6/26092014_181244_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/7/26092014_184450_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/8/26092014_184654_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers30/trainval/val/9/26092014_190156_cam.avi"),
    ]
    nightOfResearchers15 = [
        ("", vidPrefix+"sk/NightOfResearchers15/test/1/26092014_181912_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/10/26092014_203647_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/11/26092014_204021_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/12/26092014_205740_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/13/26092014_210519_cam.avi"),
        ("full partial", vidPrefix+"sk/NightOfResearchers15/test/14/26092014_211047_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/15/26092014_175102_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/16/26092014_175705_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/17/26092014_180329_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/18/26092014_180951_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/19/26092014_211637_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/2/26092014_183209_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/3/26092014_185953_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/4/26092014_191626_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/5/26092014_192313_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/6/26092014_200033_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/7/26092014_200537_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/8/26092014_201335_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/test/9/26092014_202134_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/1/26092014_172946_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/10/26092014_202954_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/2/26092014_181537_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/3/26092014_182216_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/4/26092014_182617_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/5/26092014_183818_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/6/26092014_185756_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/7/26092014_173827_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/8/26092014_190804_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/train/9/26092014_192934_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/val/1/26092014_184528_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/val/2/26092014_185044_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/val/3/26092014_190424_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/val/4/26092014_194530_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/val/5/26092014_195100_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/val/6/26092014_174618_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/val/7/26092014_203130_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/val/8/26092014_205352_cam.avi"),
        ("", vidPrefix+"sk/NightOfResearchers15/trainval/val/9/26092014_175359_cam.avi"),
    ]
    others = [
        ("talking", vidPrefix+"talking.avi"),
    ]
    myAnnots = [
        ("domaIv", vidPrefix+"o4_44.mp4"),
        ("knjiznica", vidPrefix+"o4_89.mp4"),
        ("knjiznica luc, premikal glavo", vidPrefix+"o4_90.mp4"),
        ("iso noise", vidPrefix+"o4_101.mp4"),
        ("phone1", vidPrefix+"phone1.mp4"),
    ]
    videos = nightOfResearchers15+nightOfResearchers30+eyeblink8HandInTheFirstFrames+eyeblink8+others
    #videos = eyeblink8HandInTheFirstFrames+eyeblink8+others
    #videos = myAnnots
    #videos = others
    videoRange = range(len(videos))
    #videoRange = [4] # punca od dalec
    #videoRange = [8] # dobra slika
    #videoRange = [5] # full partial
    #videoRange = [23, 24, 26, 32, 39] # out of borders
    #videoRange = [28] #templ winner
    #videoRange = [41] #templ lots of fp
    #videoRange = [19] #templ lots of missed
    #videoRange = [91] #templ lots of missed, fp
    #videoRange = videoRange[-1:] #talking
    #videoRange = [4]
    #videoRange = videoRange[:6]
    return videos, videoRange

def getConfigs():
    #method = "blackpixels"
    method = "templ"
    #method = "farneback"
    return {
        "excel_export": False,
        "coverage":     False,
        "end_hook":     False,
        "method": method,
        "othr" : {
            "vidPrefix":"/home/developer/other/posnetki/",
            "sourceCodePrefix":"/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/optical-flow",
            "codeDirectory":"/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/test_runner",

            #"outputsPref":"/vidProcOutputs",
            #"outputsPref":"/vidProcOutputs/ver1",
            #"outputsPref":"/vidProcOutputs/ver2"+method,
            #"outputsPref":"/vidProcOutputs/verTest"+method,
            "outputsPref":"/vidProcOutputs/ver3"+method, # dokoncan template, mckn potunan farneback (bounding box, fb region povecan vertikalno)
        }
    }

def main():
    # TODO add an option that we can roll over all possible settings
    #  - an option to getConfigs to postfix when options were used for outputsPref
    #  - for loop over VideoQueue with parameters what to sed
    cfg = getConfigs()
    videos, videoRange = prepareVideosList(cfg)

    VideoQueue.processVideoQueue(cfg, videos, videoRange)
    return


if __name__ == "__main__":
    main()
