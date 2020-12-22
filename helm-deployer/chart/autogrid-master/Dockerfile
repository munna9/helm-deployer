#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


FROM registry.ep.shell.com/common/spark:base
WORKDIR /

# Reset to root to run installation tasks
USER 0

# RUN useradd -ms /bin/bash spark
RUN apt-get update
RUN apt-get install -y telnet
RUN apt-get install -y vim
RUN apt-get install -y wget
RUN mkdir /streaming-app
RUN mkdir -p /var/private/ssl
RUN mkdir -p /etc/hadoop/conf

#ADD sudo
#RUN apt-get -y install sudo
#RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
#USER docker
#CMD /bin/bash
 
#COPY python/pyspark ${SPARK_HOME}/python/pyspark
#COPY python/lib ${SPARK_HOME}/python/lib

#ADD Spark Streaming Kafka dependent jars
RUN wget https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.6.2/commons-pool2-2.6.2.jar 
RUN mv commons-pool2-2.6.2.jar /opt/spark/jars/commons-pool2-2.6.2.jar

RUN wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.3.1/kafka-clients-2.3.1.jar
RUN mv kafka-clients-2.3.1.jar /opt/spark/jars/kafka-clients-2.3.1.jar

RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.0.0-preview2/spark-token-provider-kafka-0-10_2.12-3.0.0-preview2.jar
RUN mv spark-token-provider-kafka-0-10_2.12-3.0.0-preview2.jar /opt/spark/jars/spark-token-provider-kafka-0-10_2.12-3.0.0-preview2.jar

RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-tags_2.12/3.0.0-preview2/spark-tags_2.12-3.0.0-preview2.jar
RUN mv spark-tags_2.12-3.0.0-preview2.jar /opt/spark/jars/spark-tags_2.12-3.0.0-preview2.jar

RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.0.0-preview2/spark-sql-kafka-0-10_2.12-3.0.0-preview2.jar
RUN mv spark-sql-kafka-0-10_2.12-3.0.0-preview2.jar /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.0.0-preview2.jar

# RUN wget https://repo.hortonworks.com/content/repositories/releases/org/apache/spark/spark-hadoop-cloud_2.11/2.4.2.3.1.3.0-79/spark-hadoop-cloud_2.11-2.4.2.3.1.3.0-79.jar
# RUN mv spark-hadoop-cloud_2.11-2.4.2.3.1.3.0-79.jar /opt/spark/jars/spark-hadoop-cloud_2.11-2.4.2.3.1.3.0-79.jar

RUN wget https://jdbc.postgresql.org/download/postgresql-42.2.10.jar
RUN mv postgresql-42.2.10.jar /opt/spark/jars/postgresql-42.2.10.jar

#Add config files
COPY conf/spark-env.conf /opt/spark/conf/spark-env.conf
COPY conf/spark-defaults.conf /opt/spark/conf/spark-defaults.conf
COPY conf/core-site.xml /etc/hadoop/conf/core-site.xml

#Copy keystore
COPY ssl/kafka.client.keystore.jks ssl/kafka.client.keystore.b64.jks
RUN cat ssl/kafka.client.keystore.b64.jks | base64 -d > /var/private/ssl/kafka.client.keystore.jks

#COPY source 
COPY src/asset_measures_stream.py /streaming-app/asset_measures_stream.py
COPY conf/autogrid_message.json /streaming-app/autogrid_message.json
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod 777 /opt/entrypoint.sh

WORKDIR /opt/spark/work-dir
ENTRYPOINT [ "/opt/entrypoint.sh" ]

# Specify the User that the actual main process will run as
ARG spark_uid=185
USER ${spark_uid}
