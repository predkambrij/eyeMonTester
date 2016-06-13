import subprocess, threading, datetime, time, select, os

stopListenLog        = False
stopListenLogStopped = False

# extracted info out of video
lBlinks = []
rBlinks = []
tCors   = []

#videoName = "o44" # doma
#videoName = "o89" # knjiznica 40s
#videoName = "o90" # premikal glavo, zadej luc
vidPrefix = "/home/developer/other/posnetki/"
videoName = "talking.avi"
videoAnnot = os.path.splitext(videoName)[0]+".tag"

path = "/home/developer/other/android_deps/OpenCV-2.4.10-android-sdk/samples/test_runner/"
def buildFndict():
    fndict = {}
    for d in tCors:
        fndict[d["fn"]] = {
            "ts":d["ts"], "lcor":d["lcor"], "rcor":d["rcor"], "l1sd":d["l1sd"], "l2sd":d["l2sd"], "r1sd":d["r1sd"], "r2sd":d["r2sd"]
        }
    return fndict

def addDetectedBlinks(fndict):
    for blink in lBlinks:
        for frame, timing in [("fs", "lbs"), ("fe", "lbe")]:
            fndict[blink[frame]][timing] = 0.998

    for blink in rBlinks:
        for frame, timing in [("fs", "rbs"), ("fe", "rbe")]:
            fndict[blink[frame]][timing] = 0.997
    return

def writeBlinkToFndict(fndict, curBlinkId, curBlinkStart, curBlinkEnd, curBlinkLC, curBlinkRC):
    try:
        fndict[int(curBlinkStart)]["anots"] = 0.999
        fndict[int(curBlinkStart)]["anotBlinkId"] = curBlinkId
        fndict[int(curBlinkEnd)]["anote"] = 0.999
    except KeyError:
        print "skipping %s %s %s" % (curBlinkId, curBlinkStart, curBlinkEnd)


def parseAnnotations(f, fndict):
    curBlinkId = ""
    curBlinkStart = ""
    curBlinkEnd = ""
    curBlinkLC = []
    curBlinkRC = []

    content = False
    for fline in f:
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
                    writeBlinkToFndict(fndict, curBlinkId, curBlinkStart, curBlinkEnd, curBlinkLC, curBlinkRC)
                    curBlinkId    = ""
                    curBlinkStart = ""
                    curBlinkEnd   = ""
            else:
                if curBlinkId == "":
                    curBlinkId = line[1]
                    curBlinkStart = line[0]
                else:
                    writeBlinkToFndict(fndict, curBlinkId, curBlinkStart, curBlinkEnd, curBlinkLC, curBlinkRC)
                    curBlinkId    = line[1]
                    curBlinkStart = line[0]
                    curBlinkEnd   = ""
        # still the same, can also parse FullyClosed
        curBlinkEnd = line[0]

    if curBlinkId != "":
        writeBlinkToFndict(fndict, curBlinkId, curBlinkStart, curBlinkEnd, curBlinkLC, curBlinkRC)

    return

def generateTCSV():
    fndict = buildFndict()
    addDetectedBlinks(fndict)
    f = file(vidPrefix+videoAnnot)
    parseAnnotations(f, fndict)


    # sort by frame num
    fnl = sorted(fndict.items(), key=lambda x:float(x[0]))
    return fndict, fnl

def writeTCSV(fnl):
    pref = path+"outputs/"
    f = file(pref+"out.csv","wb")

    for frameNum, data in fnl:
        line = ""
        line += str(frameNum)

        for t in ["lcor", "rcor", "l1sd", "l2sd", "r1sd", "r2sd"]: # "ts", 
            line += "\t%.6f" % data[t]

        for t in ["lbs", "lbe", "rbs", "rbe"]:
            line += "\t"
            if data.has_key(t):
                line += "%.3f" % data[t]

        for t in ["anots", "anotc", "anote"]:
            line += "\t"
            if data.has_key(t):
                line += "%.3f" % data[t]

        line += "\n"
        f.write(line)
    f.close()

def detectionCoverage(fnl):
    lCaughtI = set()
    rCaughtI = set()
    lCaught = set()
    rCaught = set()
    missed  = set()
    lookingEnd = False
    blinkId = None

    lStartBlink = {}
    for i in xrange(len(lBlinks)):
        lStartBlink[lBlinks[i]["fs"]] = i
    rStartBlink = {}
    for i in xrange(len(rBlinks)):
        rStartBlink[rBlinks[i]["fs"]] = i
    lEndBlink = {}
    for i in xrange(len(lBlinks)):
        lEndBlink[lBlinks[i]["fe"]] = i
    rEndBlink = {}
    for i in xrange(len(rBlinks)):
        rEndBlink[rBlinks[i]["fe"]] = i

    annotBlink = {}
    for frameNum, data in fnl:
        if lookingEnd == False:
            if data.has_key("anots"):
                lookingEnd = True
                blinkId = data["anotBlinkId"]
                annotBlink[blinkId] = frameNum
        if lookingEnd == True:
            if data.has_key("lbs"):
                lCaught.add(blinkId)
                lCaughtI.add(lStartBlink[frameNum])
            if data.has_key("lbe"):
                lCaught.add(blinkId)
                lCaughtI.add(lEndBlink[frameNum])
            if data.has_key("rbs"):
                rCaught.add(blinkId)
                rCaughtI.add(rStartBlink[frameNum])
            if data.has_key("rbe"):
                rCaught.add(blinkId)
                rCaughtI.add(rEndBlink[frameNum])
            if data.has_key("anote"):
                if (not blinkId in lCaught) and (not blinkId in rCaught):
                    missed.add(blinkId)
                lookingEnd = False
    aCaught = set.union(lCaught, rCaught)
    bCaught = set.intersection(*[lCaught, rCaught])

    lFp = []
    for bi in xrange(len(lBlinks)):
        if not bi in lCaughtI:
            lFp.append(lBlinks[bi])

    rFp = []
    for bi in xrange(len(rBlinks)):
        if not bi in rCaughtI:
            rFp.append(rBlinks[bi])
    r = [sorted(list(x), key=lambda y:int(y)) for x in (lCaught, rCaught, bCaught, aCaught, missed)]

    # timeline fs m, fs, lf
    falseFrames = []
    for mi in missed:
        falseFrames.append((annotBlink[mi], "m"))
    
    for lfp in lFp:
        falseFrames.append((lfp["fs"], "lf"))
    for rfp in rFp:
        falseFrames.append((rfp["fs"], "rf"))
    falseFrames.sort(key=lambda x:x[0])

    r.append(falseFrames)
    return r

def processLogLine(output):
    global lBlinks, rBlinks, tCors
    if output.startswith("debug_blinks_d1:"):
        corsInfo = output.split(" ")
        print repr(corsInfo)
        if (corsInfo[1:] == ['blinkMeasureSize', 'is', 'zero']
            or corsInfo[3:7] == ['shortBmSize', 'is', 'less', 'than']
            or corsInfo[3:7] == ['fps', 'of', 'the', 'first']
            or corsInfo[3:-1] == ['shortBmSize', 'is', 'big', 'enough']
            or corsInfo[1:3] == ['updated', 'maxFramesShortList']
            ):
            return False
        fn   = int(corsInfo[corsInfo.index("lastF")+1])
        ts   = float(corsInfo[corsInfo.index("T")+1])
        lcor = float(corsInfo[corsInfo.index("La")+1])
        rcor = float(corsInfo[corsInfo.index("Ra")+1])
        l1sd = float(corsInfo[corsInfo.index("lSD12")+2])
        l2sd = float(corsInfo[corsInfo.index("lSD12")+3])
        r1sd = float(corsInfo[corsInfo.index("rSD12")+2])
        r2sd = float(corsInfo[corsInfo.index("rSD12")+3])
        tCors.append({"fn": fn, "ts" : ts, "lcor" : lcor, "rcor" : rcor, "l1sd" : l1sd, "l2sd" : l2sd, "r1sd" : r1sd, "r2sd" : r2sd})
    elif output.startswith("debug_blinks_d4:"):
        blinkInfo = output.split(" ")
        if blinkInfo[1] == "adding_lBlinkChunks":
            lst = lBlinks
        elif blinkInfo[1] == "adding_rBlinkChunks":
            lst = rBlinks

        fs = int(blinkInfo[blinkInfo.index("fs")+1])
        fe = int(blinkInfo[blinkInfo.index("fe")+1])
        start     = float(blinkInfo[blinkInfo.index("start")+1])
        end       = float(blinkInfo[blinkInfo.index("end")+1])
        duration  = float(blinkInfo[blinkInfo.index("duration")+1])
        if start > 1000000000:
            start /= 1000.
            end /= 1000.
        #start = datetime.datetime.fromtimestamp(start)
        blinkInfoDict = {"fs":fs, "fe":fe, "start":start, "end":end, "duration":duration}
        lst.append(blinkInfoDict)
    elif output.startswith("exiting"):
        return True
    return False

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
    global stopListenLogStopped

    poll_obj = select.poll()
    poll_obj.register(proc.stdout, select.POLLIN)
    while True:
        poll_result = poll_obj.poll(0)
        if poll_result:
            output = proc.stdout.readline().strip()
            try:
                if processLogLine(output):
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
            print "I quit"
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

    fnl = generateTCSV()[1]
    writeTCSV(fnl)
    res = detectionCoverage(fnl)
    for r in res:
        print r



if __name__ == "__main__":
    main()

