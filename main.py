import subprocess, threading, datetime, time, select

stopListenLog        = False
stopListenLogStopped = False

# extracted info out of video
lBlinks = []
rBlinks = []
tCors   = []

def generateTCSV():
    tsdict = {}
    for d in tCors:
        tsdict[d["ts"]] = {"lcor" : d["lcor"], "rcor" : d["rcor"], "l1sd" : d["l1sd"], "l2sd" : d["l2sd"], "r1sd" : d["r1sd"], "r2sd" : d["r2sd"]}

    for blinks, blinkLabelPrefix in [(lBlinks, "l"), (rBlinks, "r")]:
        for blink in blinks:
            for eventName, eventNameTranslation in [("start", blinkLabelPrefix+"bs"), ("end", blinkLabelPrefix+"be")]:
                try:
                    tsdict[blink[eventName]][eventNameTranslation] = 1
                except:
                    print repr(sorted(tsdict.keys()))
                    print repr(blink[eventName])
                    e = 2/0

    tsl = sorted(tsdict.items(), key=lambda x:x[0])
    return tsdict, tsl

def writeTCSV(tsl):
    pref = "/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/test_runner/outputs/"
    f = file(pref+"out.csv","wb")
    for e in tsl:
        ws = e[0]
        d = e[1]

        for t in ["lcor", "rcor", "l1sd", "l2sd", "r1sd", "r2sd"]:
            ws += "\t%.6f" % d[t]

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
    global stopListenLogStopped, lBlinks, rBlinks, tCors

    poll_obj = select.poll()
    poll_obj.register(proc.stdout, select.POLLIN)
    while True:
        poll_result = poll_obj.poll(0)
        if poll_result:
            output = proc.stdout.readline().strip()

            if output.startswith("debug_blinks_d1:"):
                corsInfo = output.split(" ")
                print repr(corsInfo)
                if corsInfo[1:] == ['blinkMeasureSize', 'is', 'zero'] or corsInfo[1:-1] == ['shortBmSize', 'is', 'less', 'than', 'X']:
                    continue
                ts   = "%.2f" % float(corsInfo[corsInfo.index("lastT")+1])
                lcor = float(corsInfo[corsInfo.index("La")+1])
                rcor = float(corsInfo[corsInfo.index("Ra")+1])
                l1sd = float(corsInfo[corsInfo.index("lSD12")+2])
                l2sd = float(corsInfo[corsInfo.index("lSD12")+3])
                r1sd = float(corsInfo[corsInfo.index("rSD12")+2])
                r2sd = float(corsInfo[corsInfo.index("rSD12")+3])
                tCors.append({"ts" : ts, "lcor" : lcor, "rcor" : rcor, "l1sd" : l1sd, "l2sd" : l2sd, "r1sd" : r1sd, "r2sd" : r2sd})
            elif output.startswith("debug_blinks_d4:"):
                blinkInfo = output.split(" ")
                start     = float(blinkInfo[blinkInfo.index("start")+1])
                end       = float(blinkInfo[blinkInfo.index("end")+1])
                duration  = float(blinkInfo[blinkInfo.index("duration")+1])
                if start > 1000000000:
                    start /= 1000.
                    end /= 1000.
                start = "%.2f" % start
                end   = "%.2f" % end
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

    writeTCSV(generateTCSV()[1])



if __name__ == "__main__":
    main()

