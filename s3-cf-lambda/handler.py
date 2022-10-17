import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        keys = key.split("/")
        distro = keys[1].split(".")[0].split("/")[0]
        datestr = keys[1].split(".")[1].split("/")[0]
        y, m, d, h = datestr.split("-")
        dest = f"partitioned/{keys[0]}/year={y}/month={m}/day={d}/hour={h}/{key}"
        
        s3.copy_object(Bucket=bucket, Key=dest, CopySource=bucket + "/" + key)        
        #s3.delete_object(Bucket=bucket, Key=key)

        print(f"copy ({distro}): s3://{bucket}/{key} -> s3://{bucket}/{dest}")


"""
Testing:
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "irr-static-logs"
        },
        "key": {
          "key": "irrlab.domain/E3U1KSE3QN2C8K.2022-10-17-08.14d3fe18.gz"
        }
      }
    }
  ]
}

Role (dev purposes only!):
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "s3-key-lambda:*"
            ],
            "Resource": "*"
        }
    ]
}

Athena catalog creation:

CREATE EXTERNAL TABLE IF NOT EXISTS
    default.partitioned_irrlab_domain (
         date DATE,
         time STRING,
         location STRING,
         bytes BIGINT,
         requestip STRING,
         method STRING,
         host STRING,
         uri STRING,
         status INT,
         referrer STRING,
         useragent STRING,
         querystring STRING,
         cookie STRING,
         resulttype STRING,
         requestid STRING,
         hostheader STRING,
         requestprotocol STRING,
         requestbytes BIGINT,
         timetaken FLOAT,
         xforwardedfor STRING,
         sslprotocol STRING,
         sslcipher STRING,
         responseresulttype STRING,
         httpversion STRING,
         filestatus STRING,
         encryptedfields INT 
)
PARTITIONED BY(
         year string,
         month string,
         day string,
         hour string )
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
LOCATION 's3://irr-static-logs/partitioned/irrlab.domain'
TBLPROPERTIES ( 'skip.header.line.count'='2');

msck repair table default.partitioned_irrlab_domain


Basic tests:

SELECT * FROM default.partitioned_irrlab_domain LIMIT 20;

SELECT *
FROM default.partitioned_irrlab_domain
WHERE year = '2022'
AND month = '10'
AND day = '17'
AND hour BETWEEN '00' AND '23';

"""