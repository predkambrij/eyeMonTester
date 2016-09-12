FROM ubuntu:14.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get upgrade -y

RUN echo "Europe/Ljubljana" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# basic utilities and fixes
RUN apt-get install -y pwgen python-setuptools && \
    easy_install supervisor
ADD cfgs/supervisord.conf /etc/supervisord.conf

# http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/
RUN apt-get install -y x11-apps  && \
# Replace with your user / group id
    export uid=499 gid=100 && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer && \
    /bin/bash -c "echo 'developer:developerpw' | chpasswd" && \
# ssh https://docs.docker.com/examples/running_ssh_service/
#   and SSH login fix. Otherwise user is kicked off after login
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

RUN /bin/bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf' && \
    apt-get install -y python-numpy python-matplotlib && \
    true

RUN apt-get install -y docker.io && \
    true


RUN apt-get update
RUN apt-get install -y python python-matplotlib && \
    true

RUN /bin/echo 'docker2:x:131:' >> /etc/group && \
    usermod -a -G docker2 developer && \
    true

ADD matplotlib_patches/axes.py /axes.py
ADD matplotlib_patches/legend.py /legend.py
RUN bash -c "mv /{axes.py,legend.py} /usr/share/pyshared/matplotlib/"

USER developer
