from multiprocessing import Process
import matplotlib.pyplot as plt

from common import Common as Cmn

# control flags
debugProcessLogLine = False

class Blackpixels:
    def __init__(self):
        pass

    @staticmethod
    def processLogLine(output, bPixes, lBlinks, rBlinks, jBlinks):
        if output.startswith("debug_bp_log_pix:"):
            flowsInfo = [x for x in output.split(" ") if x != ""]
            if debugProcessLogLine:
                print repr(flowsInfo)
            fn   = int(flowsInfo[flowsInfo.index("F")+1])
            ts   = float(flowsInfo[flowsInfo.index("T")+1])
            lNum, rNum = float(flowsInfo[flowsInfo.index("lNum")+1]), float(flowsInfo[flowsInfo.index("rNum")+1])

            bPixes.append({"fn":fn, "ts":ts, "lNum":lNum, "rNum":rNum})
            Blackpixels.postProcessLogLine(bPixes, lBlinks, rBlinks, jBlinks, False)
        elif output.startswith("exiting"):
            return True
        return False

    @staticmethod
    def postProcessLogLine(bPixes, lBlinks, rBlinks, jBlinks, isEnd, videoName=None, figparms=None):
        cm13_5 = 5.314961
        imgDpi = 150
        tightLayoutPad = 0.3
        figsize = (cm13_5*4, cm13_5*2)
        if not isEnd:
            window = 600
        else:
            window = 0

        if not isEnd and (len(bPixes) == 0 or len(bPixes) % window != 0):
            return
        #print repr(bPixes)
        if isEnd:
            window = 0
        pltx = [x["fn"] for x in bPixes[-window:]]
        lNum, rNum = [x["lNum"] for x in bPixes[-window:]], [x["rNum"] for x in bPixes[-window:]]

        annots = [
            "talkingFirst600"
        ]
        if "talkingFirst600" in annots:
            aVal = 2
            pltasx = [168, 225, 274]
            pltas = [aVal]*3
            pltaex = [176, 232, 280]
            pltae  = [aVal]*3


        plt.figure(1, figsize=figsize)
        plt.plot(pltx, lNum, 'ro-')
        plt.plot(pltx, rNum, 'bo-')
        plt.plot(pltasx, pltas, 'go', pltaex, pltae, 'g^', markersize=15.0) # annots of blinks
        #plt.figure(2)
        #plt.subplot(211)
        #plt.plot(pltx, lNum, 'ro-', pltx, rNum, 'bo-')
        if figparms != None and figparms.has_key('axis') == True:
            plt.axis(
                xmin=figparms['axis']['xmin'], xmax=figparms['axis']['xmax'],
                ymin=figparms['axis']['ymin'], ymax=figparms['axis']['ymax']
            )

        plt.legend(['levo oko', 'desno oko'])
        plt.xlabel(u'sli\u010dice', fontsize=30)
        #plt.ylabel(u'razlika vsote med zgornjim in spodnjim delom obmo\u010dja o\u010di', fontsize=30)
        plt.ylabel(u'\u0161tevilo \u010drnih to\u010dk', fontsize=30)
        plt.tight_layout(pad=tightLayoutPad)
        if figparms != None and figparms.has_key('figName') == True:
            plt.savefig('/home/developer/other/notes/m/%s.png' % figparms['figName'], dpi=imgDpi, pad_inches=1)
        if figparms != None and figparms.has_key('show') == True and figparms['show'] == False:
            pass
        else:
            plt.show()

        #plt.show(block=False)

        # if len(p) == 0:
        #     p.append(Process(target=plt.show))
        #     p[0].start()
        # else:
        #     p[0].terminate()
        #     p.pop()
        #     p.append(Process(target=plt.show))
        #     p[0].start()

        #plt.plot(pltx, pltlYdiff, 'ro-', pltx, pltrYdiff, 'ro-')
        #plt.show()
        return

