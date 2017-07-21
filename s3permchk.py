#!/usr/bin/env python3

import boto3
import json
import os,sys

client = boto3.client('s3')
bucket_list = client.list_buckets()

def check_bucket(bucket):
    bucket_location = client.get_bucket_location(Bucket=bucket)['LocationConstraint']
    new_client = boto3.client('s3', region_name=bucket_location)
    bucket_acl = new_client.get_bucket_acl(Bucket=bucket)
    permission = []

    for grants in bucket_acl['Grants']:
        if ('URI' in grants['Grantee']) and ('AllUser' in grants['Grantee']['URI']):
            permission.append(grants['Permission'])

        globalListAccess = 'no'
        globalWriteAccess = 'no'

        if len(permission) == 1:
            if permission[0] == 'READ':
                globalListAccess = 'YES'
                globalWriteAccess = 'no'
               
        elif len(permission) > 1:
       	    if permission[0] == 'READ':
            	globalListAccess = 'YES'
            if permission[1] == 'WRITE':
                globalWriteAccess = 'YES'
            else:
                globalWriteAccess = 'no'
    
    return(bucket, bucket_location, globalListAccess, globalWriteAccess)

def display_data(data):
    table = Texttable()
    table.set_cols_align(["l", "l", "c", "c"])
    table.set_cols_dtype(['t', 't', 't', 't'])
    table.set_cols_width(['60', '15', '12', '12'])
    table.add_rows([['Bucket', 'Region', 'Read Access', 'Write Access']])

    for s3 in data:
        table.add_row([s3['bucket'], s3['bucket_location'], s3['read'], s3['write']])

    print(table.draw())

def connect_s3():
    client = boto3.resource('s3')
    data = []

    for bucket in client.buckets.all():
        bucket, bucket_location, globalListAccess, globalWriteAccess =  check_bucket(bucket.name)
        data.append({'bucket':bucket, 'bucket_location':bucket_location, 'read':globalListAccess, 'write':globalWriteAccess})

    display_data(data)

def lambda_handler(event, context):
    libdir = os.path.dirname(os.path.realpath(__file__))
    # Import installed packages (in site-packages)
    site_pkgs = os.path.join(libdir, "libs")
    sys.path.append(site_pkgs)
    from texttable import Texttable
    try:
        print()
        connect_s3()
    except Exception as err:
        print(err)

if __name__ == "__main__":
    from texttable import Texttable
    try:
        print()
        connect_s3()
    except Exception as err:
        print(err)
