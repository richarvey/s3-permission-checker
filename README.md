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

To run on a different AWS profile to default:

```
./s3permchk.py --profile <YOUR_PROFILE_NAME>
```

### Example output

```
+----------------------------------------------+-----------------+--------------------------------+--------------------------------+
|                    Bucket                    |     Region      |        All Users Access        |          Auth'd Users          |
+==============================================+=================+================================+================================+
| bucket_0                                     | eu-west-1       |               []               |               []               |
+----------------------------------------------+-----------------+--------------------------------+--------------------------------+
| bucket_1                                     | eu-west-2       |        ['FULL_CONTROL']        |               []               |
+----------------------------------------------+-----------------+--------------------------------+--------------------------------+
| bucket_1                                     | eu-west-1       |               []               |            ['READ']            |
+----------------------------------------------+-----------------+--------------------------------+--------------------------------+
| bucket_2                                     | eu-west-1       |      ['READ', 'READ_ACP']      |               []               |
+----------------------------------------------+-----------------+--------------------------------+--------------------------------+
......
```
