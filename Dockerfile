FROM ubuntu:14.04

ENV DEBIAN_FRONTEND noninteractive

ARG ARG_UID
ARG ARG_GID
ARG ARG_DOCKERGID

ADD cfgs/supervisord.conf /etc/supervisord.conf

RUN apt-get update && \
    apt-get upgrade -y && \
    \
    echo "Europe/Ljubljana" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    /bin/bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf' && \
    \
    apt-get install -y pwgen python-setuptools && \
    easy_install supervisor

# http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/
RUN apt-get install -y x11-apps  && \
    export uid=$ARG_UID gid=$ARG_GID dgid=$ARG_DOCKERGID && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer && \
    /bin/bash -c "echo 'developer:developerpw' | chpasswd" && \
    /bin/echo "docker2:x:${dgid}:" >> /etc/group && \
    usermod -a -G docker2 developer && \
# ssh https://docs.docker.com/examples/running_ssh_service/
#   and SSH login fix. Otherwise user is kicked off after login
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

ADD matplotlib_patches/axes.py \
    matplotlib_patches/legend.py \
    /

RUN apt-get install -y docker.io python python-matplotlib python-numpy python-matplotlib && \
    bash -c "mv /{axes.py,legend.py} /usr/share/pyshared/matplotlib/"

USER developer
