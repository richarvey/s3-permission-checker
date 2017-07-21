## S3 permission checker

Produces a report of all S3 buckets in your account and prints out a table to easily identify which buckets have open ACL's for read and write permissions.

### Requirements

 - Python 3
 - boto3
 - texttable
 - awscli installed and configure for credentials

#### Install Requirements

```
pip3 install -r requirements.txt
```

### Running

```
./s3permchk.py
```

### Example output

```
+--------------------------------------------------------------+-----------------+--------------+--------------+
|                            Bucket                            |     Region      | Read Access  | Write Access |
+==============================================================+=================+==============+==============+
| bucket_0                                                     | eu-west-1       |      no      |      no      |
+--------------------------------------------------------------+-----------------+--------------+--------------+
| bucket_1                                                     | eu-west-1       |      no      |      no      |
+--------------------------------------------------------------+-----------------+--------------+--------------+
| bucket_2                                                     | eu-west-1       |      no      |      no      |
+--------------------------------------------------------------+-----------------+--------------+--------------+
| bucket_3                                                     | eu-west-2       |     YES      |      YES     |
+--------------------------------------------------------------+-----------------+--------------+--------------+
| bucket_4                                                     | eu-west-2       |     YES      |      no      |
+--------------------------------------------------------------+-----------------+--------------+--------------+
......
```
