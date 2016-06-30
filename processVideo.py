import subprocess, threading, datetime, time, select, os, traceback
from common import Common as Cmn
from templ import Templ
from farne import Farne
from blackpixels import Blackpixels

# flow flags
stopListenLog        = False
stopListenLogStopped = False


# parsing logs
def initListenLog(isWebcam):
    global proc
    if not isWebcam:
        tailfCmd = ['tail', '-n0', '-f', '/tmp/eyemonpy.log']
    else:
        tailfCmd = ['tail', '-n0', '-f', '/tmp/testlog.txt']

    proc = subprocess.Popen(
        tailfCmd,
        stdin   = subprocess.PIPE,
        stdout  = subprocess.PIPE,
        bufsize = 0,
    )
def listenLog(cfg, annots, fFlows, fFlowsI, tCors, bPixes, lBlinks, rBlinks):
    global stopListenLogStopped

    poll_obj = select.poll()
    poll_obj.register(proc.stdout, select.POLLIN)
    while True:
        poll_result = poll_obj.poll(0)
        if poll_result:
            output = proc.stdout.readline().strip()
            try:
                if cfg["method"] == "templ":
                    if Templ.processLogLine(output, tCors, lBlinks, rBlinks):
                        stopListenLogStopped = True
                        break
                elif cfg["method"] == "farneback":
                    res = Farne.processLogLine(output, annots, fFlows, fFlowsI, lBlinks, rBlinks)
                    if res:
                        stopListenLogStopped = True
                        break
                elif cfg["method"] == "blackpixels":
                    res = Blackpixels.processLogLine(output, bPixes, lBlinks, rBlinks)
                    if res:
                        stopListenLogStopped = True
                        break
            except StandardError,e:
                print "crash", output
                print traceback.format_exc()

                stopListenLogStopped = True
                break
            continue

        time.sleep(0.1)
        if stopListenLog == True:
            stopListenLogStopped = True
            break

def terminateListenLog():
    proc.terminate()
####

# configure and run video
def initRunVideo(isWebcam):
    global vid
    if not isWebcam:
        cmd = ['make', 'dtp']
    else:
        cmd = ['make', 'd']
    vid = subprocess.Popen(
        cmd,
        cwd     = '/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/optical-flow',
        stdin   = subprocess.PIPE,
        stdout  = subprocess.PIPE,
        bufsize = 0,
    )
def terminateRunVideo():
    vid.terminate()
###

def processVideo(cfg, isWebcam, annotFilename):
    global stopListenLog

    lBlinks, rBlinks = [], []
    fFlows, fFlowsI = [], {}
    tCors, bPixes   = [], []

    initListenLog(isWebcam)
    time.sleep(0.5)
    initRunVideo(isWebcam)

    if type(annotFilename) == type(""):
        if annotFilename.endswith(".tag"):
            f = file(annotFilename)
            annotsl, annots = Cmn.parseAnnotations(f, None, "farne")
        else:
            raise ValueError("unknown annotation format")
    else:
        annotsl, annots = [], ({}, {})

    listenLogThread = threading.Thread(target=listenLog, args=[cfg, annots, fFlows, fFlowsI, tCors, bPixes, lBlinks, rBlinks])
    listenLogThread.start()
    listenLogThread.join()

    stopListenLog = True
    while stopListenLogStopped != True:
        #print "Waiting thread to stop"
        time.sleep(0.1)
    terminateListenLog()
    terminateRunVideo()

    if cfg["excel_export"]:
        if cfg["method"] == "templ":
            fnl = Templ.generateTCSV(vidPrefix, videoAnnot, tCors, lBlinks, rBlinks)[1]
            Templ.writeTCSV("/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/test_runner/", fnl)

    if cfg["coverage"]:
        if cfg["method"] == "farneback":
            l, r, o = Cmn.detectionCoverageF(annotsl, lBlinks, rBlinks)
            Cmn.displayDetectionCoverage(l, r, o)
        elif cfg["method"] == "templ":
            fnl = Templ.generateTCSV(vidPrefix, videoAnnot, tCors, lBlinks, rBlinks)[1]
            res = Cmn.detectionCoverage(lBlinks, rBlinks, fnl)
            for r in res:
                print r
    if cfg["end_hook"]:
        if cfg["method"] == "farneback":
            Farne.postProcessLogLine(fFlows, lBlinks, rBlinks, True)
        elif cfg["method"] == "templ":
            Templ.postProcessLogLine(tCors, lBlinks, rBlinks, True)

    if cfg["method"] == "farneback":
        l, r, o = Cmn.detectionCoverageF(annotsl, lBlinks, rBlinks)
        return fFlows, lBlinks, rBlinks, l, r, o
    else:
        return
