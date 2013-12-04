# docker build -t irr/tomcat7 -rm .
# docker run -d -p 8080:8080 irr/tomcat7
FROM irr/jdk7-oracle
RUN apt-get -y install tomcat7
RUN echo "JAVA_HOME=/usr/lib/jvm/java-7-oracle" >> /etc/default/tomcat7
EXPOSE 8080
CMD service tomcat7 start && tail -f /var/lib/tomcat7/logs/catalina.out
