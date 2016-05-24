import subprocess, threading, datetime, time, select

stopListenLog        = False
stopListenLogStopped = False

# extracted info out of video
lBlinks = []
rBlinks = []

def generateCSV():
    #file(pref+"lBlinks.csv","wb").write("\n".join("%s\t%.2f" % (x["start"].strftime("%d/%m/%y %H:%M:%S"), x["duration"]) for x in lBlinks))
    #file(pref+"rBlinks.csv","wb").write("\n".join("%s\t%.2f" % (x["start"].strftime("%d/%m/%y %H:%M:%S"), x["duration"]) for x in rBlinks))
    #file(pref+"lBlinks.csv","wb").write("\n".join("%.2f\t%.2f" % (x["start"], 1) for x in lBlinks)) # x["duration"]
    #file(pref+"rBlinks.csv","wb").write("\n".join("%.2f\t%.2f" % (x["start"], 1) for x in rBlinks)) # x["duration"]
    # rewrite based on timestamp key
    tsdict = {}
    for bl, bn in [(lBlinks, "l"), (rBlinks, "r")]:
        for e in bl:
            for k, t in [("start", bn+"bs"), ("end", bn+"be")]:
                if tsdict.has_key(e[k]):
                    tsdict[e[k]][t] = 1
                else:
                    tsdict[e[k]] = {t:1}
    tsl = sorted(tsdict.items(), key=lambda x:x[0])
    return tsdict, tsl

def writeCSV(tsl):
    pref = "/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/test_runner/outputs/"
    f = file(pref+"out.csv","wb")
    for e in tsl:
        ws = "%.2f" % e[0]
        d = e[1]

        for t in ["lbs", "lbe", "rbs", "rbe"]:
            ws += "\t"
            if d.has_key(t):
                ws += "%.2f" % d[t]
        ws += "\n"
        f.write(ws)
    f.close()

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
            output = proc.stdout.readline().strip()
            if output.startswith("debug_blinks_d4:"):
                blinkInfo = output.split(" ")
                start     = float(blinkInfo[blinkInfo.index("start")+1])
                end       = float(blinkInfo[blinkInfo.index("end")+1])
                duration  = float(blinkInfo[blinkInfo.index("duration")+1])
                if start > 1000000000:
                    start /= 1000.
                    end /= 1000.
                #start = datetime.datetime.fromtimestamp(start)

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
        ['bash', 'compileDesktop', 'test'
        ],
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

    writeCSV(generateCSV()[1])



if __name__ == "__main__":
    main()

