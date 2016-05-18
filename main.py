import subprocess


proc = subprocess.Popen(['bash', "/tmp/slowcat.sh"],
                        #shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        bufsize=0,
                        )

for i in range(10):
    proc.stdin.write('%d\n' % i)
    output = proc.stdout.readline()
    print "pri:",output.rstrip()
proc.terminate()
remainder = proc.communicate()[0]
print "remainder:", remainder
