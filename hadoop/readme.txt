export HADOOP_USER_NAME=cloudera
export HADOOP_CONF_DIR=/home/irocha/python/hadoop/configs/hadoop-conf

hdfs dfs -ls /user/cloudera
hdfs dfs -rm -r -f /user/cloudera/gutenberg*
hdfs dfs -mkdir -p /user/cloudera
hdfs dfs -copyFromLocal gutenberg /user/cloudera
hdfs dfs -ls /user/cloudera/gutenberg

hadoop jar hadoop-*streaming*.jar \
    -file mapper.py -mapper mapper.py \
    -file reducer.py -reducer reducer.py \
    -input /user/cloudera/gutenberg/* -output /user/cloudera/gutenberg-output

hdfs dfs -rm -r -f /user/cloudera/gutenberg-output

hdfs dfs -ls /user/cloudera/gutenberg-output
hdfs dfs -cat /user/cloudera/gutenberg-output/part-00000
hdfs dfs -rm -r -f /user/cloudera/gutenberg*
