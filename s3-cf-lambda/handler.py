import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        distro = key.split(".")[0].split("/")[0]
        datestr = key.split(".")[1].split("/")[0]
        y, m, d, h = datestr.split("-")
        dest = f"partitioned/{distro}/year={y}/month={m}/day={d}/hour={h}/{key}"
        
        s3.copy_object(Bucket=bucket, Key=dest, CopySource=bucket + "/" + key)        
        #s3.delete_object(Bucket=bucket, Key=key)

        print(f"copy: s3://{bucket}/{key} -> s3://{bucket}/{dest}")


"""
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "irr-static-logs"
        },
        "key": {
          "key": "E3U1KSE3QN2C8K.2022-10-12-12.05c44449.gz"
        }
      }
    }
  ]
}

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


CREATE EXTERNAL TABLE IF NOT EXISTS
    default.partitioned_cf (
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
LOCATION 's3://irr-static-logs/partitioned/E3U1KSE3QN2C8K'
TBLPROPERTIES ( 'skip.header.line.count'='2');

msck repair table default.partitioned_cf

select * from default.partitioned_cf limit 20;

"""