import sys


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


if __name__ == "__main__":
    #analizeAnnotated("o90")
    partialBlinks()

