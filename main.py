import subprocess, threading, datetime, time, select, os, traceback
from common import Common as Cmn
from templ import Templ
from farne import Farne
from blackpixels import Blackpixels

# control flags
flg_excel_export = True
flg_coverage = True
flg_end_hook = True
#flg_method = "blackpixels"
flg_method = "farneback"
#flg_method = "templ"

# flow flags
stopListenLog        = False
stopListenLogStopped = False

# state variables
lBlinks, rBlinks = [], []
tCors, fFlows, bPixes = [], [], []
fFlowsI = {}

#videoName = "o44" # doma
#videoName = "o89" # knjiznica 40s
#videoName = "o90" # premikal glavo, zadej luc
vidPrefix = "/home/developer/other/posnetki/"

vidNum = 0
if vidNum == 0:
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

path = "/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/test_runner/"

# parsing logs
def initListenLog():
    global proc
    proc = subprocess.Popen(
        ['tail', '-n0', '-f', '/tmp/testlog.txt'],
        stdin   = subprocess.PIPE,
        stdout  = subprocess.PIPE,
        bufsize = 0,
    )
def listenLog():
    global stopListenLogStopped

    poll_obj = select.poll()
    poll_obj.register(proc.stdout, select.POLLIN)
    while True:
        poll_result = poll_obj.poll(0)
        if poll_result:
            output = proc.stdout.readline().strip()
            try:
                if flg_method == "templ":
                    if Templ.processLogLine(output, tCors, lBlinks, rBlinks):
                        stopListenLogStopped = True
                        break
                elif flg_method == "farneback":
                    res = Farne.processLogLine(output, annots, fFlows, fFlowsI, lBlinks, rBlinks)
                    if res:
                        stopListenLogStopped = True
                        break
                elif flg_method == "blackpixels":
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
def initRunVideo():
    global vid
    if vidNum != 0:
        cmd = ['make', 'dt']
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

def main():
    global stopListenLog, annots
    initListenLog()
    time.sleep(0.5)
    initRunVideo()

    if videoAnnot != ".tag":
        f = file(vidPrefix+videoAnnot)
        annotsl, annots = Cmn.parseAnnotations(f, None, "farne")
    else:
        annotsl, annots = [], ({}, {})

    listenLogThread = threading.Thread(target=listenLog, args=[])
    listenLogThread.start()
    listenLogThread.join()

    stopListenLog = True
    while stopListenLogStopped != True:
        print "Waiting thread to stop"
        time.sleep(0.1)
    terminateListenLog()
    terminateRunVideo()

    if flg_excel_export:
        if flg_method == "templ":
            fnl = Templ.generateTCSV(vidPrefix, videoAnnot, tCors, lBlinks, rBlinks)[1]
            Templ.writeTCSV(path, fnl)

    if flg_coverage:
        if flg_method == "farneback":
            l, r, o = Cmn.detectionCoverageF(annotsl, lBlinks, rBlinks)
            Cmn.displayDetectionCoverage(l, r, o)
        elif flg_method == "templ":
            fnl = Templ.generateTCSV(vidPrefix, videoAnnot, tCors, lBlinks, rBlinks)[1]
            res = Cmn.detectionCoverage(lBlinks, rBlinks, fnl)
            for r in res:
                print r
    if flg_end_hook:
        if flg_method == "farneback":
            Farne.postProcessLogLine(fFlows, lBlinks, rBlinks, True)
        elif flg_method == "templ":
            Templ.postProcessLogLine(tCors, lBlinks, rBlinks, True)



if __name__ == "__main__":
    main()

