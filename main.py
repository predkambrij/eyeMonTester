import subprocess, threading, time, select

stopListenLog = False
stopListenLogStopped = False

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
            output = proc.stdout.readline()
            print "out:", output
            continue

        print "I'm here"
        time.sleep(0.1)
        if stopListenLog == True:
            stopListenLogStopped = True
            print "I quit"
            break

def terminateListenLog():
    proc.terminate()




def main():
    global stopListenLog
    initListenLog()

    listenLogThread = threading.Thread(target=listenLog, args=[])
    listenLogThread.start()
    time.sleep(5)

    stopListenLog = True
    while stopListenLogStopped != True:
        print "Waiting thread to stop"
        time.sleep(0.1)
    terminateListenLog()



if __name__ == "__main__":
    main()

