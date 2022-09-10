
from amazonlinux:latest
RUN yum update -y && yum -y install tzdata python3 gzip tar git

WORKDIR /opt
RUN git clone https://github.com/munroebot/scoreboard.git
WORKDIR /opt/scoreboard
RUN pip3 install -r requirements.txt
COPY ./init.sh /opt/scoreboard/init.sh
RUN chmod 700 /opt/scoreboard/init.sh

CMD ["/bin/sh", "/opt/scoreboard/init.sh"]