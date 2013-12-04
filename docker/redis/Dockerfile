FROM        ubuntu:12.10
RUN         apt-get update
RUN         apt-get -y install redis-server
RUN         echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf
RUN         sysctl vm.overcommit_memory=1
EXPOSE      6379
ENTRYPOINT  ["/usr/bin/redis-server"]
