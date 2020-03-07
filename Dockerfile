FROM python:3.7.6-slim-buster

RUN apt update
RUN apt install -y \
      gstreamer1.0-tools \
      gstreamer1.0-pulseaudio \
      gstreamer1.0-plugins-base \
      gstreamer1.0-plugins-good \
      gstreamer1.0-plugins-bad
RUN apt install -y git build-essential pkg-config autopoint autoconf libtool libcap-dev libsndfile-dev && \
      git clone https://github.com/pulseaudio/pulseaudio.git && \
      cd pulseaudio && \
      ./bootstrap.sh && \
      ./configure \
        --sysconfdir=/etc \
        --localstatedir=/var \
        --disable-nls \
        --disable-x11 \
        --disable-tests \
        --disable-oss-output \
        --disable-oss-wrapper \
        --disable-coreaudio-output \
        --disable-alsa \
        --disable-esound \
        --disable-waveout \
        --disable-glib2 \
        --disable-gtk3 \
        --disable-gsettings \
        --disable-gconf \
        --disable-avahi \
        --disable-jack \
        --disable-asyncns \
        --disable-lirc \
        --disable-dbus \
        --disable-bluez5 \
        --disable-bluez5-ofono-headset \
        --disable-bluez5-native-headset \
        --disable-udev \
        --disable-hal-compat \
        --disable-openssl \
        --disable-systemd-daemon \
        --disable-systemd-login \
        --disable-systemd-journal \
        --disable-manpages \
        --disable-per-user-esound-socket \
        --disable-default-build-tests \
        --disable-legacy-database-entry-format && \
      make && make install
RUN apt install -y procps vim git
RUN useradd -r -d /var/run/pulse -s /usr/sbin/nologin pulse && \
     mkdir -p /home/pulse/.config/pulse && chown -R pulse.pulse /home/pulse/.config && \
     mkdir /var/run/pulse && chown pulse.pulse /var/run/pulse

WORKDIR /opt/parent-radio-hk
RUN pip install azure.cognitiveservices.speech flask watchdog supervisor
ADD conf/pulseaudio.pa /etc/pulse/default.pa
ADD conf/supervisord.conf /opt/parent-radio-hk/conf/
ADD src/server.py src/playout.py /opt/parent-radio-hk/bin/
RUN chmod u+x bin/server.py bin/playout.py
RUN mkdir -p /opt/parent-radio-hk/queue &&  chmod 666 /opt/parent-radio-hk/queue

CMD supervisord -c conf/supervisord.conf
