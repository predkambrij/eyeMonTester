eyeMonTester
============

Testing framework for [https://github.com/predkambrij/eyeMon](https://github.com/predkambrij/eyeMon)

EyeMonTester runs eyeMon's methods against recorded videos.
EyeMonTester can generate overall report (in CSV format) and draw debugging graphs from intermediate results.

##Prepare Docker images:
- build eyeMon Docker image (see the instructions in its [README.md](https://github.com/predkambrij/eyeMon)
- ```git clone git@github.com:predkambrij/eyeMonTester.git```
- ```docker build -t predkambrij/eyemontester eyeMonTester/```

##Prepare testing videos:
- Add videos (optionally with annotations) in this directory [https://github.com/predkambrij/eyeMon/tree/master/posnetki](https://github.com/predkambrij/eyeMon/tree/master/posnetki)
    - You can get example videos (with annotations) [here](http://www2.fiit.stuba.sk/~fogelton/acvr2014/index.html):
    - ```wget http://www2.fiit.stuba.sk/~fogelton/acvr2014/eyeblink8.zip -o /tmp/eyeblink8.zip```
    - ```mkdir eyeMon/posnetki/sk/```
    - ```unzip /tmp/eyeblink8.zip -d eyeMon/posnetki/sk/```
- Update videos and videoRange variables (in [prepareVideosList](https://github.com/predkambrij/eyeMonTester/blob/master/main.py) function) so that it refers to your video locations
    - example:
    - ```videos = eyeblink8HandInTheFirstFrames+eyeblink8``` # videos that are available to process
    - ```videoRange = range(len(videos))``` # videos you would like to process (you can select subset of available videos)

##Settings that require manual configuration:
Method for eye blink detection:
- make sure that both locations are updated to the same method:
    - ```(int method = ...)``` [in this file](https://github.com/predkambrij/eyeMon/blob/master/_1OpenCVopticalflow/src/main/jni/common_settings_testpy.cpp)
    - ```(method = ...)``` in [getConfigs()](https://github.com/predkambrij/eyeMonTester/blob/master/main.py)

##Start the container:
- ```docker run -it --rm -e DIRPREF=$(pwd) -v $(pwd)/eyeMon/_1OpenCVopticalflow/src/main/jni/main_settings_testpy.cpp:/tmp/main_settings_testpy.cpp -v $(pwd)/eyeMon/posnetki:/posnetki -v $(pwd)/eyeMonTester:/eyeMonTester -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v /var/run/docker.sock:/var/run/docker.sock predkambrij/eyemontester bash```

Generating intermediate results:
- ```cd /eyeMonTester```
- ```python main.py```

See the results:
- ```python misc.py -r``` # generate CSV report
- ```python misc.py -g``` # Show debugging graphs
- ```python misc.py -h``` # Show help (other options)


