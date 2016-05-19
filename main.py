import subprocess, threading, time, select

stopListenLog        = False
stopListenLogStopped = False

# extracted info out of video
lBlinks = []
rBlinks = []

# parsing logs
def initListenLog():
    global proc
    proc = subprocess.Popen(
        #['bash', "/tmp/slowcat.sh"],
        ['tail', '-n0', '-f', '/tmp/testlog.txt'],
        #shell  = True,
        stdin   = subprocess.PIPE,
        stdout  = subprocess.PIPE,
        bufsize = 0,
    )

def listenLog():
    global stopListenLogStopped, lBlinks, rBlinks
    poll_obj = select.poll()
    poll_obj.register(proc.stdout, select.POLLIN)
    while True:
        poll_result = poll_obj.poll(0)
        if poll_result:
            output = proc.stdout.readline()
            if output.startswith("debug_blinks_d4:"):
                blinkInfo = output.split(" ")
                start     = float(blinkInfo[blinkInfo.index("start")+1])
                end       = float(blinkInfo[blinkInfo.index("end")+1])
                duration  = float(blinkInfo[blinkInfo.index("duration")+1])
                blinkInfoDict = {"start":start, "end":end, "duration":duration}

                if blinkInfo[1] == "adding_lBlinkChunks":
                    lBlinks.append(blinkInfoDict)
                elif blinkInfo[1] == "adding_rBlinkChunks":
                    rBlinks.append(blinkInfoDict)

                print "adding:", blinkInfo[1], blinkInfo
            elif output.startswith("exiting"):
                stopListenLogStopped = True
                break

            continue

        time.sleep(0.1)
        if stopListenLog == True:
            stopListenLogStopped = True
            print "I quit"
            break

def terminateListenLog():
    proc.terminate()
####

# configure and run video
def initRunVideo():
    global vid
    vid = subprocess.Popen(
        ['bash', 'compileDesktop'],
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



if __name__ == "__main__":
    main()

