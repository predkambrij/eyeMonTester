import subprocess, threading, datetime, time, select, os
from common import Common as Cmn
from templ import Templ

# control flags
flg_excel_export = True
flg_coverage = True
#flg_method = "farneback"
flg_method = "templ"

# flow flags
stopListenLog        = False
stopListenLogStopped = False

# state variables
lBlinks, rBlinks = [], []
tCors = []

#videoName = "o44" # doma
#videoName = "o89" # knjiznica 40s
#videoName = "o90" # premikal glavo, zadej luc
vidPrefix = "/home/developer/other/posnetki/"
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
            except:
                print "crash", output
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
    vid = subprocess.Popen(
        ['make', 'dt'],
        cwd     = '/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/optical-flow',
        stdin   = subprocess.PIPE,
        stdout  = subprocess.PIPE,
        bufsize = 0,
    )
def terminateRunVideo():
    vid.terminate()
###

def main():
    global stopListenLog
    initListenLog()
    time.sleep(0.5)
    initRunVideo()

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
        if flg_method == "templ":
            fnl = Templ.generateTCSV(vidPrefix, videoAnnot, tCors, lBlinks, rBlinks)[1]
            res = Cmn.detectionCoverage(lBlinks, rBlinks, fnl)
            for r in res:
                print r



if __name__ == "__main__":
    main()

