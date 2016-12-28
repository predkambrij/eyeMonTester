import subprocess, threading, datetime, time, select, os, traceback
from common import Common as Cmn
from templ import Templ
from farne import Farne
from blackpixels import Blackpixels

# flow flags
stopListenLog        = False

# parsing logs
def initListenLog(cfg, isWebcam):
    global proc
    time.sleep(3)
    if not isWebcam:
        logfile = cfg["othr"]["codeDirectory"]+'/logfiles/eyemonpy.log'
    else:
        logfile = cfg["othr"]["codeDirectory"]+'/logfiles/testlog.txt'
    tailfCmd = ['tail', '-n0', '-f', logfile]
    if not os.path.isfile(logfile):
        file(logfile,"wb").write("")

    proc = subprocess.Popen(
        tailfCmd,
        stdin   = subprocess.PIPE,
        stdout  = subprocess.PIPE,
        bufsize = 0,
    )
def listenLog(cfg, annots, fFlows, fFlowsI, tracking, tCors, tCorsI, bPixes, lBlinks, rBlinks, jBlinks):
    poll_obj = select.poll()
    poll_obj.register(proc.stdout, select.POLLIN)
    while True:
        poll_result = poll_obj.poll(0)
        if poll_result:
            output = proc.stdout.readline().strip()
            try:
                if cfg["method"] == "templ":
                    if Templ.processLogLine(output, annots, tCors, tCorsI, lBlinks, rBlinks, jBlinks):
                        break
                elif cfg["method"] == "farneback":
                    res = Farne.processLogLine(output, annots, fFlows, fFlowsI, tracking, lBlinks, rBlinks, jBlinks)
                    if res:
                        break
                elif cfg["method"] == "blackpixels":
                    res = Blackpixels.processLogLine(output, bPixes, lBlinks, rBlinks, jBlinks)
                    if res:
                        break
            except StandardError,e:
                print "crash", output
                print traceback.format_exc()
                break
            continue

        time.sleep(0.1)
        if stopListenLog == True:
            break
    return

def terminateListenLog():
    proc.terminate()
####

# configure and run video
def initRunVideo(isWebcam):
    global vid
    if not isWebcam:
        cmd = ['./runEyemon.sh', 'make dtp']
    else:
        cmd = ['./runEyemon.sh', 'make d']
    vid = subprocess.Popen(
        cmd,
        cwd     = '/eyeMonTester',
        stdin   = subprocess.PIPE,
        stdout  = subprocess.PIPE,
        bufsize = 0,
    )
    outs, errs = vid.communicate()
def terminateRunVideo():
    vid.terminate()
###

def processVideo(cfg, isWebcam, annotFilename):
    global stopListenLog

    lBlinks, rBlinks, jBlinks = [], [], []
    fFlows, fFlowsI, tracking = [], {}, {"detecting":[], "pupilDisplacement":[], "upperLowerL":[], "upperLowerR":[]}
    tCors, tCorsI, bPixes   = [], {}, []

    initListenLog(cfg, isWebcam)
    time.sleep(0.5)
    initRunVideo(isWebcam)

    if type(annotFilename) == type(""):
        if annotFilename.endswith(".tag"):
            annotsl, annots = Cmn.parseAnnotations(file(annotFilename), None, "farne")
        elif annotFilename.endswith(".v1"):
            annotsl, annots = Cmn.parseAnnotationsMy(file(annotFilename), None, "farne")
        else:
            raise ValueError("unknown annotation format")
    else:
        annotsl, annots = [], ({}, {})

    listenLogThread = threading.Thread(target=listenLog, args=[cfg, annots, fFlows, fFlowsI, tracking, tCors, tCorsI, bPixes, lBlinks, rBlinks, jBlinks])
    listenLogThread.start()
    r = vid.wait()
    if r != 0:
        stopListenLog = True
        print "Processing didn't stop correctly %i" % r
    listenLogThread.join()
    terminateListenLog()

    if cfg["excel_export"]:
        if cfg["method"] == "templ":
            fnl = Templ.generateTCSV(vidPrefix, videoAnnot, tCors, lBlinks, rBlinks)[1]
            #Templ.writeTCSV("/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/test_runner/", fnl)

    if cfg["coverage"]:
        if cfg["method"] == "farneback":
            l, r, o = Cmn.detectionCoverageF(annotsl, lBlinks, rBlinks, jBlinks)
            Cmn.displayDetectionCoverage(l, r, o)
        elif cfg["method"] == "templ":
            fnl = Templ.generateTCSV(vidPrefix, videoAnnot, tCors, lBlinks, rBlinks)[1]
            res = Cmn.detectionCoverage(lBlinks, rBlinks, jBlinks, fnl)
            for r in res:
                print r
    if cfg["end_hook"]:
        if cfg["method"] == "farneback":
            Farne.postProcessLogLine(fFlows, lBlinks, rBlinks, jBlinks, True)
        elif cfg["method"] == "templ":
            Templ.postProcessLogLine(tCors, lBlinks, rBlinks, jBlinks, True)

    if cfg["method"] == "farneback":
        return fFlows, lBlinks, rBlinks, jBlinks, tracking
    elif cfg["method"] == "templ":
        return tCors, lBlinks, rBlinks, jBlinks, tracking
    elif cfg["method"] == "blackpixels":
        return bPixes, lBlinks, rBlinks, jBlinks, tracking
