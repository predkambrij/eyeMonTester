import sys, os, time, argparse

from common import Common as Cmn
#from farne import Farne
from videoQueue import VideoQueue
import videoQueue
import main, processVideo


import numpy as np
import matplotlib.pyplot as plt
def sd(data):
    n = len(data)
    mean = sum(data)/float(n)
    ss = sum((x-mean)**2 for x in data)
    return (ss/float(n))**0.5

def signalProc():
    inp = [1,1,1,1,1, 1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1.1,  1. ,  0.8,  0.9,
        1. ,  1.2,  0.9,  1. ,  1. ,  1.1,  1.2,  1. ,  1.5,  1. ,  3. ,
        2. ,  5. ,  3. ,  2. ,  1. ,  1. ,  1. ,  0.9,  1. ,  1. ,  3. ,
        2.6,  4. ,  3. ,  3.2,  2. ,  1. ,  1. ,  1. ,  1. ,  1., 1.5,1,1.5,1,1,1,1,1,1,1,1,1,1,
        2,3,4,5,5,5,4,4,3,4,5,5,6,7,8,9,8,9,8,7,6,5,4,4,4,3,2,4 ]
    input = np.array(inp)
    s = sd(inp)
    #m = 0.5
    m = s*0.8
    signal = (input > (np.roll(input,6)+m)) & (input > (np.roll(input,-6)+m))
    print signal
    plt.plot(input)
    plt.plot(signal.nonzero()[0], input[signal], 'ro')
    plt.show()


def testMain__():
    actions = ["postProcessLogLine",]
    cfg = main.getConfigs()
    vidPrefix = cfg["othr"]["vidPrefix"]
    farneVideos = [
        (
            "farnePresentation",
            vidPrefix+"talking.avi",
            {
                'graphs':['postProcessLogLine'],
                'figNums': [3],
                'axis' : {'xmin':600, 'xmax':1250, 'ymin':-6.0, 'ymax':6},
                'legBpos':2,
                'legLpos':1,
                'aVals': 2.9,
                'jVals': 2.65,
                'lVals': 2.4,
                'rVals': 2.15,
            }
        ),
        (
            "signalTalking",
            vidPrefix+"talking.avi",
            {
                'graphs':['postProcessLogLine'],
                'figNums': [3],
                'axis' : {'xmin':580, 'xmax':1000, 'ymin':-4.8, 'ymax':4.8},
                'legBpos':1,
                'legLpos':4,
                'aVals': 2.40,
                'jVals': 2.15,
                'lVals': 1.9,
                'rVals': 1.65,
            }
        ),
        (
            "talkingPupilDisplacement",
            vidPrefix+"talking.avi",
            {
                'graphs':['postProcessTracking'],
                #'axis' : {'xmin':0, 'xmax':5000, 'ymin':0, 'ymax':140},
                'legBpos':0,
                'legLpos':1,
            }
        ),
        (
            "signalIsoNoise",
            vidPrefix+"o4_101.mp4",
            {
                'graphs':['postProcessLogLine'],
                'figNums': [3],
                'axis' : {'xmin':0, 'xmax':400, 'ymin':-2.11, 'ymax':2.11},
                'legBpos':4,
                'legLpos':3,
                'aVals': 1.40,
                'jVals': 1.3,
                'lVals': 1.2,
                'rVals': 1.1,
            }
        ),
        (
            "signalFarneState", # sometimes doesnt render correctly
            vidPrefix+"o4_101.mp4",
            {
                'graphs':['postProcessLogLine'],
                'figNums': [3],
                'axis' : {'xmin':111, 'xmax':134, 'ymin':-1.44, 'ymax':1.44},
                'legBpos':4,
                'legLpos':3,
                'aVals': 1.30,
                'jVals': 1.2,
                'lVals': 1.1,
                'rVals': 1.0,
            }
        ),
        (
            "puncaOdDalec1MissedUpperLower",
            vidPrefix+"sk/eyeblink8/1/26122013_223310_cam.avi",
            {
                'graphs':['postProcessUpperLower'],
                'figNums': [3],
                'axis' : {'xmin':0, 'xmax':15000, 'ymin':0, 'ymax':3.3},
                'legBpos':2,
                'legLpos':1,
            }
        ),
        (
            "puncaOdDalecFpsUpperLower",
            #vidPrefix+"sk/eyeblink8/2/26122013_224532_cam.avi",
            vidPrefix+"sk/eyeblink8/1/26122013_223310_cam.avi",
            {
                'graphs':['postProcessUpperLower'],
                'figNums': [3],
                'axis' : {'xmin':7800, 'xmax':10900, 'ymin':0, 'ymax':3.3},
                'legBpos':2,
                'legLpos':1,
            }
        ),
    ]
    templVideos = [
        (
            "meHighIsoTempl",
            vidPrefix+"o4_101.mp4",
            {
                'figNums': [4], # 3 odvod
                'axis' : {'xmin':0, 'xmax':600, 'ymin':0.960, 'ymax':1.008},
                'legBpos':1,
                'legLpos':4,
                'aVals': 1.007,
                'jVals': 1.005,
                'lVals': 1.003,
                'rVals': 1.001,
            }
        ),
        (
            "talkingTemplPostureChanges",
            vidPrefix+"talking.avi",
            {
                'figNums': [4], # 3 odvod
                'axis' : {'xmin':600, 'xmax':1250, 'ymin':0.860, 'ymax':1.018},
                'legBpos':3,
                'legLpos':4,
                'aVals': 1.015,
                'jVals': 1.011,
                'lVals': 1.007,
                'rVals': 1.003,
            }
        ),
        (
            "talkingTemplInappropriateTemplate",
            vidPrefix+"talking.avi",
            {
                'figNums': [4], # 3 odvod
                'axis' : {'xmin':3000, 'xmax':3610, 'ymin':0.890, 'ymax':1.018},
                'legBpos':4,
                'legLpos':3,
                'aVals': 1.015,
                'jVals': 1.011,
                'lVals': 1.007,
                'rVals': 1.003,
            }
        ),
        (
            "templSignalSample", # TODO boljsi
            vidPrefix+"sk/eyeblink8/1/26122013_223310_cam.avi",
            {
                'figNums': [4], # 3 odvod
                'axis' : {'xmin':0, 'xmax':3000, 'ymin':0.861, 'ymax':1.018},
                'legBpos':3,
                'legLpos':4,
                'aVals': 1.015,
                'jVals': 1.011,
                'lVals': 1.007,
                'rVals': 1.003,
            }
        ),
        (
            "templSDDeriv", # TODO boljsi
            vidPrefix+"sk/eyeblink8/1/26122013_223310_cam.avi",
            {
                'figNums': [3],
                'axis' : {'xmin':0, 'xmax':3000, 'ymin':-0.043, 'ymax':0.043},
                'legBpos':2,
            }
        ),
        (
            "talkingTemplSignal1",
            vidPrefix+"talking.avi",
            {
                'figNums': [4], # 3 odvod
                'axis' : {'xmin':0, 'xmax':600, 'ymin':0.932, 'ymax':1.009},
                'legBpos':3,
                'legLpos':4,
                'aVals': 1.007,
                'jVals': 1.005,
                'lVals': 1.003,
                'rVals': 1.001,
            }
        ),
    ]
    bpVideos = [
        (
            "bpPresentation",
            vidPrefix+"talking.avi",
            {
                'graphs':['postProcessLogLine'],
                'axis' : {'xmin':600, 'xmax':1250, 'ymin':0, 'ymax':120},
            }
        ),
        (
            "talkingBlackPixelsSignal1DilateErodeAnnots",
            vidPrefix+"talking.avi",
            {
                'axis' : {'xmin':0, 'xmax':600, 'ymin':0, 'ymax':135},
            }
        ),
    ]
    vids = farneVideos
    #vids = templVideos
    #vids = bpVideos
    t0 = vids[0:1]
    t1 = vids[1:2]
    t2 = vids[2:3]
    t3 = vids[3:4]
    t4 = vids[4:5]
    t5 = vids[5:6]
    t6 = vids[6:7]
    t = t0
    #t = vids
    for video in t: # farneVideos templVideos bpVideos
        settings = {
            'pltSettings':{
                'show':False,
            },
        }
        settings['pltSettings'].update(video[2])
        settings['pltSettings'].update({'figName':video[0]})
        videoQueue.VideoQueue.processOutputs(cfg, [(video[0], video[1])], [0], actions, settings)
        #reload(main)
        #reload(videoQueue)
        #reload(processVideo)
        #os.system('sync')
        #time.sleep(0.5)

def testMain():
    settings = {
        'pltSettings':{
            'show':True,
                'legBpos':3,
                'legLpos':4,
            'figNums': [3],
            'graphs':[
                    'postProcessLogLine',
                    #'postProcessTracking',
                ],
            'disableLegend':True,
        },
    }
    cfg = main.getConfigs()
    videos, videoRange = main.prepareVideosList(cfg)

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--report', action='store_true', required=False, help="Generate overall CSV report")
    parser.add_argument('-g', '--graphs', action='store_true', required=False, help="Show debugging graphs")
    parser.add_argument('-c', '--detection-coverage', action='store_true', required=False, help="Show detection coverage")
    parser.add_argument('-d', '--pupil-displacement', action='store_true', required=False, help="Show pupil displacement graph")
    parser.add_argument('-s', '--signal-processing', action='store_true', required=False, help="Signal processing")
    args = parser.parse_args()
    actions = []
    if args.report:
        actions.append("writeOverallReport")
    if args.graphs:
        actions.append("postProcessLogLine")
    if args.detection_coverage:
        actions.append("displayDetectionCoverage")
    if args.pupil_displacement:
        actions.append("displayPupilDisplacement")
    if args.signal_processing:
        actions.append("signalProcessing")

    VideoQueue.processOutputs(cfg, videos, videoRange, actions, settings)

def pyplotGraphFromOutput():
    return
def analizeAnnotated(fn):
    blinks = [[float(y) for y in x.split(",") if y != "p"] for x in file("annotations/"+fn, "rb").read().strip().split("\n")]
    for blink in blinks:
        print blink[1]-blink[0], blink[2]-blink[0], repr(blink)
    #print blinks
    return

def partialBlinks():
    filesNum = len(sys.argv)-1
    print filesNum
    allBlinks = 0
    onePartialsN = 0
    bothPartialsN = 0
    for f in xrange(1, filesNum+1):
        onePartials = []
        bothPartials = []
        content = False
        curBlinkId = ""
        lFully = False
        rFully = False
        for fline in file(sys.argv[f]):
            fline = fline.strip()
            if not content:
                if fline == "#start":
                    content = True
                continue
            else:
                if fline == "#end":
                    break

            # 0 frameCounter 1 blinkID 2 nonFrontalFace 3 leftFullyClosed 4 leftNonFrontal 5 rightFullyClosed 6 rightNonFrontal
            line = fline.split(":")
            if line[1] != curBlinkId:
                if line[1] == "-1":
                    if curBlinkId == "":
                        continue
                    else:
                        # end of the blink
                        if lFully == False and rFully == False:
                            bothPartials.append([curBlinkId, lFully, rFully])
                        if (lFully == True and rFully == False) or (lFully == False and rFully == True):
                            onePartials.append([curBlinkId, lFully, rFully])
                        curBlinkId = ""
                        lFully = False
                        rFully = False
                else:
                    if curBlinkId == "":
                        # start of the blink
                        allBlinks += 1
                        curBlinkId = line[1]
                        lFully = False
                        rFully = False
                    else:
                        # end of previous, start of new one
                        allBlinks += 1
                        if lFully == False and rFully == False:
                            bothPartials.append([curBlinkId, lFully, rFully])
                        if (lFully == True and rFully == False) or (lFully == False and rFully == True):
                            onePartials.append([curBlinkId, lFully, rFully])
                        curBlinkId = line[1]
                        lFully = False
                        rFully = False

            # still the same, can also parse FullyClosed
            if line[3] == "C":
                lFully = True
            if line[5] == "C":
                rFully = True
        if len(onePartials) > 0 or len(bothPartials) > 0:
            file("/tmp/partials", "ab").write("%s\n%d %s\n%d %s\n" % (
                sys.argv[f],
                len(bothPartials), str(repr(bothPartials)),
                len(onePartials), str(repr(onePartials))
                ))
        onePartialsN += len(onePartials)
        bothPartialsN += len(bothPartials)

    print allBlinks
    file("/tmp/partials", "ab").write("onePartials %d bothPartials %d\n" % (onePartialsN, bothPartialsN))
    return

def showAnnots():
    cfg = main.getConfigs()
    videos, videoRange = main.prepareVideosList(cfg)
    videoName = videos[videoRange[0]][1]

    annotFilename = os.path.splitext(videoName)[0]+".tag"
    if not os.path.isfile(annotFilename):
        return
    annotsl, annots = Cmn.parseAnnotations(file(annotFilename), None, "farne")
    print annots[2]
    return

def bc():
    #annots = ({1284: {'be': 1289, 'bi': 12, 'bs': 1284}, 4229: {'be': 4234, 'bi': 50, 'bs': 4229}, 2696: {'be': 2702, 'bi': 33, 'bs': 2696}, 4322: {'be': 4328, 'bi': 53, 'bs': 4322}, 4880: {'be': 4887, 'bi': 60, 'bs': 4880}, 1809: {'be': 1817, 'bi': 19, 'bs': 1809}, 274: {'be': 280, 'bi': 3, 'bs': 274}, 2883: {'be': 2890, 'bi': 35, 'bs': 2883}, 916: {'be': 922, 'bi': 6, 'bs': 916}, 1173: {'be': 1178, 'bi': 9, 'bs': 1173}, 1942: {'be': 1946, 'bi': 21, 'bs': 1942}, 3972: {'be': 3979, 'bi': 46, 'bs': 3972}, 3247: {'be': 3252, 'bi': 39, 'bs': 3247}, 3996: {'be': 4003, 'bi': 47, 'bs': 3996}, 3359: {'be': 3363, 'bi': 42, 'bs': 3359}, 2466: {'be': 2472, 'bi': 28, 'bs': 2466}, 1444: {'be': 1457, 'bi': 13, 'bs': 1444}, 1959: {'be': 1968, 'bi': 22, 'bs': 1959}, 168: {'be': 176, 'bi': 1, 'bs': 168}, 2350: {'be': 2356, 'bi': 27, 'bs': 2350}, 1199: {'be': 1204, 'bi': 10, 'bs': 1199}, 4401: {'be': 4408, 'bi': 55, 'bs': 4401}, 3509: {'be': 3514, 'bi': 43, 'bs': 3509}, 4662: {'be': 4670, 'bi': 57, 'bs': 4662}, 3257: {'be': 3263, 'bi': 40, 'bs': 3257}, 1723: {'be': 1728, 'bi': 17, 'bs': 1723}, 2493: {'be': 2500, 'bi': 29, 'bs': 2493}, 3006: {'be': 3012, 'bi': 36, 'bs': 3006}, 2625: {'be': 2632, 'bi': 32, 'bs': 2625}, 1602: {'be': 1606, 'bi': 15, 'bs': 1602}, 2755: {'be': 2761, 'bi': 34, 'bs': 2755}, 2119: {'be': 2124, 'bi': 25, 'bs': 2119}, 4797: {'be': 4801, 'bi': 59, 'bs': 4797}, 1485: {'be': 1492, 'bi': 14, 'bs': 1485}, 2509: {'be': 2516, 'bi': 30, 'bs': 2509}, 1105: {'be': 1113, 'bi': 7, 'bs': 1105}, 2002: {'be': 2010, 'bi': 23, 'bs': 2002}, 4179: {'be': 4194, 'bi': 48, 'bs': 4179}, 4312: {'be': 4316, 'bi': 52, 'bs': 4312}, 1241: {'be': 1248, 'bi': 11, 'bs': 1241}, 3279: {'be': 3283, 'bi': 41, 'bs': 3279}, 2524: {'be': 2531, 'bi': 31, 'bs': 2524}, 2014: {'be': 2019, 'bi': 24, 'bs': 2014}, 4301: {'be': 4307, 'bi': 51, 'bs': 4301}, 2272: {'be': 2279, 'bi': 26, 'bs': 2272}, 225: {'be': 232, 'bi': 2, 'bs': 225}, 1122: {'be': 1129, 'bi': 8, 'bs': 1122}, 613: {'be': 617, 'bi': 4, 'bs': 613}, 3047: {'be': 3053, 'bi': 37, 'bs': 3047}, 4220: {'be': 4227, 'bi': 49, 'bs': 4220}, 3602: {'be': 3609, 'bi': 44, 'bs': 3602}, 3645: {'be': 3651, 'bi': 45, 'bs': 3645}, 1832: {'be': 1844, 'bi': 20, 'bs': 1832}, 4723: {'be': 4729, 'bi': 58, 'bs': 4723}, 756: {'be': 763, 'bi': 5, 'bs': 756}, 3191: {'be': 3196, 'bi': 38, 'bs': 3191}, 1785: {'be': 1791, 'bi': 18, 'bs': 1785}, 4986: {'be': 4991, 'bi': 61, 'bs': 4986}, 4603: {'be': 4610, 'bi': 56, 'bs': 4603}, 1660: {'be': 1664, 'bi': 16, 'bs': 1660}, 4351: {'be': 4357, 'bi': 54, 'bs': 4351}}, {1664: {'be': 1664, 'bi': 16, 'bs': 1660}, 4610: {'be': 4610, 'bi': 56, 'bs': 4603}, 3252: {'be': 3252, 'bi': 39, 'bs': 3247}, 4357: {'be': 4357, 'bi': 54, 'bs': 4351}, 2356: {'be': 2356, 'bi': 27, 'bs': 2350}, 1289: {'be': 1289, 'bi': 12, 'bs': 1284}, 4234: {'be': 4234, 'bi': 50, 'bs': 4229}, 3979: {'be': 3979, 'bi': 46, 'bs': 3972}, 2702: {'be': 2702, 'bi': 33, 'bs': 2696}, 4227: {'be': 4227, 'bi': 49, 'bs': 4220}, 4991: {'be': 4991, 'bi': 61, 'bs': 4986}, 4003: {'be': 4003, 'bi': 47, 'bs': 3996}, 3609: {'be': 3609, 'bi': 44, 'bs': 3602}, 280: {'be': 280, 'bi': 3, 'bs': 274}, 1817: {'be': 1817, 'bi': 19, 'bs': 1809}, 1946: {'be': 1946, 'bi': 21, 'bs': 1942}, 922: {'be': 922, 'bi': 6, 'bs': 916}, 176: {'be': 176, 'bi': 1, 'bs': 168}, 3363: {'be': 3363, 'bi': 42, 'bs': 3359}, 2472: {'be': 2472, 'bi': 28, 'bs': 2466}, 4316: {'be': 4316, 'bi': 52, 'bs': 4312}, 1968: {'be': 1968, 'bi': 22, 'bs': 1959}, 1457: {'be': 1457, 'bi': 13, 'bs': 1444}, 1204: {'be': 1204, 'bi': 10, 'bs': 1199}, 1178: {'be': 1178, 'bi': 9, 'bs': 1173}, 4408: {'be': 4408, 'bi': 55, 'bs': 4401}, 1844: {'be': 1844, 'bi': 20, 'bs': 1832}, 3514: {'be': 3514, 'bi': 43, 'bs': 3509}, 4670: {'be': 4670, 'bi': 57, 'bs': 4662}, 3263: {'be': 3263, 'bi': 40, 'bs': 3257}, 1728: {'be': 1728, 'bi': 17, 'bs': 1723}, 4801: {'be': 4801, 'bi': 59, 'bs': 4797}, 3651: {'be': 3651, 'bi': 45, 'bs': 3645}, 2500: {'be': 2500, 'bi': 29, 'bs': 2493}, 1606: {'be': 1606, 'bi': 15, 'bs': 1602}, 2632: {'be': 2632, 'bi': 32, 'bs': 2625}, 2761: {'be': 2761, 'bi': 34, 'bs': 2755}, 2890: {'be': 2890, 'bi': 35, 'bs': 2883}, 2124: {'be': 2124, 'bi': 25, 'bs': 2119}, 4887: {'be': 4887, 'bi': 60, 'bs': 4880}, 2531: {'be': 2531, 'bi': 31, 'bs': 2524}, 1492: {'be': 1492, 'bi': 14, 'bs': 1485}, 4729: {'be': 4729, 'bi': 58, 'bs': 4723}, 1113: {'be': 1113, 'bi': 7, 'bs': 1105}, 2010: {'be': 2010, 'bi': 23, 'bs': 2002}, 3012: {'be': 3012, 'bi': 36, 'bs': 3006}, 1248: {'be': 1248, 'bi': 11, 'bs': 1241}, 4194: {'be': 4194, 'bi': 48, 'bs': 4179}, 2019: {'be': 2019, 'bi': 24, 'bs': 2014}, 2279: {'be': 2279, 'bi': 26, 'bs': 2272}, 232: {'be': 232, 'bi': 2, 'bs': 225}, 617: {'be': 617, 'bi': 4, 'bs': 613}, 3053: {'be': 3053, 'bi': 37, 'bs': 3047}, 4307: {'be': 4307, 'bi': 51, 'bs': 4301}, 4328: {'be': 4328, 'bi': 53, 'bs': 4322}, 3283: {'be': 3283, 'bi': 41, 'bs': 3279}, 1129: {'be': 1129, 'bi': 8, 'bs': 1122}, 2516: {'be': 2516, 'bi': 30, 'bs': 2509}, 763: {'be': 763, 'bi': 5, 'bs': 756}, 3196: {'be': 3196, 'bi': 38, 'bs': 3191}, 1791: {'be': 1791, 'bi': 18, 'bs': 1785}})
    annotsL = [{'be': 1289, 'bi': 12, 'bs': 1284}, {'be': 4887, 'bi': 60, 'bs': 4880}, {'be': 1817, 'bi': 19, 'bs': 1809}, {'be': 280, 'bi': 3, 'bs': 274}, {'be': 3252, 'bi': 39, 'bs': 3247}, {'be': 3363, 'bi': 42, 'bs': 3359}, {'be': 1844, 'bi': 20, 'bs': 1832}, {'be': 2356, 'bi': 27, 'bs': 2350}, {'be': 4408, 'bi': 55, 'bs': 4401}, {'be': 4670, 'bi': 57, 'bs': 4662}, {'be': 3651, 'bi': 45, 'bs': 3645}, {'be': 2632, 'bi': 32, 'bs': 2625}, {'be': 1606, 'bi': 15, 'bs': 1602}, {'be': 2890, 'bi': 35, 'bs': 2883}, {'be': 2124, 'bi': 25, 'bs': 2119}, {'be': 1113, 'bi': 7, 'bs': 1105}, {'be': 4194, 'bi': 48, 'bs': 4179}, {'be': 1129, 'bi': 8, 'bs': 1122}, {'be': 617, 'bi': 4, 'bs': 613}, {'be': 3609, 'bi': 44, 'bs': 3602}, {'be': 2500, 'bi': 29, 'bs': 2493}, {'be': 4729, 'bi': 58, 'bs': 4723}, {'be': 3196, 'bi': 38, 'bs': 3191}, {'be': 4991, 'bi': 61, 'bs': 4986}, {'be': 4227, 'bi': 49, 'bs': 4220}, {'be': 3979, 'bi': 46, 'bs': 3972}, {'be': 4234, 'bi': 50, 'bs': 4229}, {'be': 2702, 'bi': 33, 'bs': 2696}, {'be': 4307, 'bi': 51, 'bs': 4301}, {'be': 922, 'bi': 6, 'bs': 916}, {'be': 1178, 'bi': 9, 'bs': 1173}, {'be': 1946, 'bi': 21, 'bs': 1942}, {'be': 4003, 'bi': 47, 'bs': 3996}, {'be': 2472, 'bi': 28, 'bs': 2466}, {'be': 1457, 'bi': 13, 'bs': 1444}, {'be': 1968, 'bi': 22, 'bs': 1959}, {'be': 176, 'bi': 1, 'bs': 168}, {'be': 1204, 'bi': 10, 'bs': 1199}, {'be': 3514, 'bi': 43, 'bs': 3509}, {'be': 3263, 'bi': 40, 'bs': 3257}, {'be': 1728, 'bi': 17, 'bs': 1723}, {'be': 4801, 'bi': 59, 'bs': 4797}, {'be': 3012, 'bi': 36, 'bs': 3006}, {'be': 2761, 'bi': 34, 'bs': 2755}, {'be': 1492, 'bi': 14, 'bs': 1485}, {'be': 2516, 'bi': 30, 'bs': 2509}, {'be': 2010, 'bi': 23, 'bs': 2002}, {'be': 4316, 'bi': 52, 'bs': 4312}, {'be': 1248, 'bi': 11, 'bs': 1241}, {'be': 3283, 'bi': 41, 'bs': 3279}, {'be': 2531, 'bi': 31, 'bs': 2524}, {'be': 2019, 'bi': 24, 'bs': 2014}, {'be': 2279, 'bi': 26, 'bs': 2272}, {'be': 232, 'bi': 2, 'bs': 225}, {'be': 4328, 'bi': 53, 'bs': 4322}, {'be': 3053, 'bi': 37, 'bs': 3047}, {'be': 1664, 'bi': 16, 'bs': 1660}, {'be': 763, 'bi': 5, 'bs': 756}, {'be': 1791, 'bi': 18, 'bs': 1785}, {'be': 4610, 'bi': 56, 'bs': 4603}, {'be': 4357, 'bi': 54, 'bs': 4351}]
    lBlinks = [{'duration': 300.0, 'start': 5700.0, 'fs': 170, 'end': 6000.0, 'fe': 179}, {'duration': 466.666667, 'start': 18766.67, 'fs': 562, 'end': 19233.333333, 'fe': 576}, {'duration': 366.666667, 'start': 25200.0, 'fs': 755, 'end': 25566.666667, 'fe': 766}, {'duration': 500.0, 'start': 30533.33, 'fs': 915, 'end': 31033.333333, 'fe': 930}, {'duration': 466.666667, 'start': 36033.33, 'fs': 1080, 'end': 36500.0, 'fe': 1094}, {'duration': 333.333333, 'start': 36866.67, 'fs': 1105, 'end': 37200.0, 'fe': 1115}, {'duration': 466.666667, 'start': 37333.33, 'fs': 1119, 'end': 37800.0, 'fe': 1133}, {'duration': 333.333333, 'start': 39133.33, 'fs': 1173, 'end': 39466.666667, 'fe': 1183}, {'duration': 200.0, 'start': 49466.67, 'fs': 1483, 'end': 49666.666667, 'fe': 1489}, {'duration': 266.666667, 'start': 55333.33, 'fs': 1659, 'end': 55600.0, 'fe': 1667}, {'duration': 400.0, 'start': 57466.67, 'fs': 1723, 'end': 57866.666667, 'fe': 1735}, {'duration': 433.333333, 'start': 59466.67, 'fs': 1783, 'end': 59900.0, 'fe': 1796}, {'duration': 466.666667, 'start': 64700.0, 'fs': 1940, 'end': 65166.666667, 'fe': 1954}, {'duration': 366.666667, 'start': 66766.67, 'fs': 2002, 'end': 67133.333333, 'fe': 2013}, {'duration': 400.0, 'start': 67133.33, 'fs': 2013, 'end': 67533.333333, 'fe': 2025}, {'duration': 366.666667, 'start': 70600.0, 'fs': 2117, 'end': 70966.666667, 'fe': 2128}, {'duration': 466.666667, 'start': 75733.33, 'fs': 2271, 'end': 76200.0, 'fe': 2285}, {'duration': 433.333333, 'start': 78366.67, 'fs': 2350, 'end': 78800.0, 'fe': 2363}, {'duration': 466.666667, 'start': 82100.0, 'fs': 2462, 'end': 82566.666667, 'fe': 2476}, {'duration': 333.333333, 'start': 84100.0, 'fs': 2522, 'end': 84433.333333, 'fe': 2532}, {'duration': 500.0, 'start': 87533.33, 'fs': 2625, 'end': 88033.333333, 'fe': 2640}, {'duration': 300.0, 'start': 89866.67, 'fs': 2695, 'end': 90166.666667, 'fe': 2704}, {'duration': 233.333333, 'start': 91866.67, 'fs': 2755, 'end': 92100.0, 'fe': 2762}, {'duration': 400.0, 'start': 100166.67, 'fs': 3004, 'end': 100566.666667, 'fe': 3016}, {'duration': 333.333333, 'start': 101533.33, 'fs': 3045, 'end': 101866.666667, 'fe': 3055}, {'duration': 333.333333, 'start': 106366.67, 'fs': 3190, 'end': 106700.0, 'fe': 3200}, {'duration': 433.333333, 'start': 108133.33, 'fs': 3243, 'end': 108566.666667, 'fe': 3256}, {'duration': 466.666667, 'start': 108566.67, 'fs': 3256, 'end': 109033.333333, 'fe': 3270}, {'duration': 400.0, 'start': 109233.33, 'fs': 3276, 'end': 109633.333333, 'fe': 3288}, {'duration': 333.333333, 'start': 111933.33, 'fs': 3357, 'end': 112266.666667, 'fe': 3367}, {'duration': 333.333333, 'start': 116900.0, 'fs': 3506, 'end': 117233.333333, 'fe': 3516}, {'duration': 300.0, 'start': 121500.0, 'fs': 3644, 'end': 121800.0, 'fe': 3653}, {'duration': 266.666667, 'start': 129366.67, 'fs': 3880, 'end': 129633.333333, 'fe': 3888}, {'duration': 366.666667, 'start': 131133.33, 'fs': 3933, 'end': 131500.0, 'fe': 3944}, {'duration': 166.666667, 'start': 140700.0, 'fs': 4220, 'end': 140866.666667, 'fe': 4225}, {'duration': 333.333333, 'start': 140966.67, 'fs': 4228, 'end': 141300.0, 'fe': 4238}, {'duration': 333.333333, 'start': 143366.67, 'fs': 4300, 'end': 143700.0, 'fe': 4310}, {'duration': 333.333333, 'start': 153433.33, 'fs': 4602, 'end': 153766.666667, 'fe': 4612}, {'duration': 266.666667, 'start': 157500.0, 'fs': 4724, 'end': 157766.666667, 'fe': 4732}, {'duration': 333.333333, 'start': 159900.0, 'fs': 4796, 'end': 160233.333333, 'fe': 4806}, {'duration': 400.0, 'start': 162600.0, 'fs': 4877, 'end': 163000.0, 'fe': 4889}, {'duration': 300.0, 'start': 166200.0, 'fs': 4985, 'end': 166500.0, 'fe': 4994}]
    rBlinks = [{'duration': 400.0, 'start': 5633.33, 'fs': 168, 'end': 6033.333333, 'fe': 180}, {'duration': 333.333333, 'start': 18900.0, 'fs': 566, 'end': 19233.333333, 'fe': 576}, {'duration': 366.666667, 'start': 25200.0, 'fs': 755, 'end': 25566.666667, 'fe': 766}, {'duration': 366.666667, 'start': 30533.33, 'fs': 915, 'end': 30900.0, 'fe': 926}, {'duration': 366.666667, 'start': 36833.33, 'fs': 1104, 'end': 37200.0, 'fe': 1115}, {'duration': 433.333333, 'start': 37400.0, 'fs': 1121, 'end': 37833.333333, 'fe': 1134}, {'duration': 166.666667, 'start': 40000.0, 'fs': 1199, 'end': 40166.666667, 'fe': 1204}, {'duration': 366.666667, 'start': 47666.67, 'fs': 1429, 'end': 48033.333333, 'fe': 1440}, {'duration': 300.0, 'start': 49533.33, 'fs': 1485, 'end': 49833.333333, 'fe': 1494}, {'duration': 400.0, 'start': 57433.33, 'fs': 1722, 'end': 57833.333333, 'fe': 1734}, {'duration': 500.0, 'start': 59466.67, 'fs': 1783, 'end': 59966.666667, 'fe': 1798}, {'duration': 366.666667, 'start': 64666.67, 'fs': 1939, 'end': 65033.333333, 'fe': 1950}, {'duration': 466.666667, 'start': 66666.67, 'fs': 1999, 'end': 67133.333333, 'fe': 2013}, {'duration': 366.666667, 'start': 67133.33, 'fs': 2013, 'end': 67500.0, 'fe': 2024}, {'duration': 400.0, 'start': 70633.33, 'fs': 2118, 'end': 71033.333333, 'fe': 2130}, {'duration': 433.333333, 'start': 78333.33, 'fs': 2349, 'end': 78766.666667, 'fe': 2362}, {'duration': 233.333333, 'start': 82200.0, 'fs': 2465, 'end': 82433.333333, 'fe': 2472}, {'duration': 233.333333, 'start': 83133.33, 'fs': 2493, 'end': 83366.666667, 'fe': 2500}, {'duration': 433.333333, 'start': 83666.67, 'fs': 2509, 'end': 84100.0, 'fe': 2522}, {'duration': 433.333333, 'start': 84100.0, 'fs': 2522, 'end': 84533.333333, 'fe': 2535}, {'duration': 333.333333, 'start': 87533.33, 'fs': 2625, 'end': 87866.666667, 'fe': 2635}, {'duration': 266.666667, 'start': 89900.0, 'fs': 2696, 'end': 90166.666667, 'fe': 2704}, {'duration': 366.666667, 'start': 91866.67, 'fs': 2755, 'end': 92233.333333, 'fe': 2766}, {'duration': 500.0, 'start': 96033.33, 'fs': 2880, 'end': 96533.333333, 'fe': 2895}, {'duration': 400.0, 'start': 100200.0, 'fs': 3005, 'end': 100600.0, 'fe': 3017}, {'duration': 466.666667, 'start': 101500.0, 'fs': 3044, 'end': 101966.666667, 'fe': 3058}, {'duration': 333.333333, 'start': 106366.67, 'fs': 3190, 'end': 106700.0, 'fe': 3200}, {'duration': 333.333333, 'start': 108233.33, 'fs': 3246, 'end': 108566.666667, 'fe': 3256}, {'duration': 200.0, 'start': 108566.67, 'fs': 3256, 'end': 108766.666667, 'fe': 3262}, {'duration': 466.666667, 'start': 109233.33, 'fs': 3276, 'end': 109700.0, 'fe': 3290}, {'duration': 266.666667, 'start': 111966.67, 'fs': 3358, 'end': 112233.333333, 'fe': 3366}, {'duration': 200.0, 'start': 116966.67, 'fs': 3508, 'end': 117166.666667, 'fe': 3514}, {'duration': 266.666667, 'start': 120100.0, 'fs': 3602, 'end': 120366.666667, 'fe': 3610}, {'duration': 333.333333, 'start': 121533.33, 'fs': 3645, 'end': 121866.666667, 'fe': 3655}, {'duration': 66.666667, 'start': 131233.33, 'fs': 3936, 'end': 131300.0, 'fe': 3938}, {'duration': 266.666667, 'start': 131400.0, 'fs': 3941, 'end': 131666.666667, 'fe': 3949}, {'duration': 166.666667, 'start': 131800.0, 'fs': 3953, 'end': 131966.666667, 'fe': 3958}, {'duration': 366.666667, 'start': 139266.67, 'fs': 4177, 'end': 139633.333333, 'fe': 4188}, {'duration': 300.0, 'start': 140666.67, 'fs': 4219, 'end': 140966.666667, 'fe': 4228}, {'duration': 500.0, 'start': 140966.67, 'fs': 4228, 'end': 141466.666667, 'fe': 4243}, {'duration': 333.333333, 'start': 143400.0, 'fs': 4301, 'end': 143733.333333, 'fe': 4311}, {'duration': 266.666667, 'start': 143733.33, 'fs': 4311, 'end': 144000.0, 'fe': 4319}, {'duration': 133.333333, 'start': 144100.0, 'fs': 4322, 'end': 144233.333333, 'fe': 4326}, {'duration': 200.0, 'start': 153433.33, 'fs': 4602, 'end': 153633.333333, 'fe': 4608}, {'duration': 300.0, 'start': 157500.0, 'fs': 4724, 'end': 157800.0, 'fe': 4733}, {'duration': 333.333333, 'start': 159900.0, 'fs': 4796, 'end': 160233.333333, 'fe': 4806}]
    l, r, o = Cmn.detectionCoverageF(annotsL, lBlinks, rBlinks)
    Cmn.displayDetectionCoverage(l, r, o)
    #for r in res:
    #    print r
    return


if __name__ == "__main__":
    #analizeAnnotated("o90")
    #partialBlinks()
    #showAnnots()
    #bc()
    testMain()

