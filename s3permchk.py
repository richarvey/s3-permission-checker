#!/usr/bin/env python3

import boto3
import json
import os,sys
from texttable import Texttable

client = boto3.client('s3')
bucket_list = client.list_buckets()

def check_bucket(bucket):
    try:
        bucket_location = client.get_bucket_location(Bucket=bucket)['LocationConstraint']
    except:
        return(bucket, "FAIL", "FAIL")
    new_client = boto3.client('s3', region_name=bucket_location)
    bucket_acl = new_client.get_bucket_acl(Bucket=bucket)
    permission = []
    auth_permission = []
        
    AllUsers = []
    AuthUsers = []

    for grants in bucket_acl['Grants']:
        #print(bucket)
        #print(grants)
        if ('URI' in grants['Grantee']) and ('AllUser' in grants['Grantee']['URI']):
            permission.append(grants['Permission'])
        if ('URI' in grants['Grantee']) and ('AuthenticatedUsers' in grants['Grantee']['URI']):
            auth_permission.append(grants['Permission'])


    for perm in permission:
        AllUsers.append(perm)

    for auth_perm in auth_permission:
        AuthUsers.append(auth_perm)
    
    return(bucket, bucket_location, AllUsers, AuthUsers)

def display_data(data):
    table = Texttable()
    table.set_cols_align(["l", "l", "c", "c"])
    table.set_cols_dtype(['t', 't', 't', 't'])
    table.set_cols_width(['60', '15', '30', '30'])
    table.add_rows([['Bucket', 'Region', 'All Users Access', 'Auth\'d Users']])

    for s3 in data:
        table.add_row([s3['bucket'], s3['bucket_location'], s3['allusers'], s3['authusers']])

    print(table.draw())

def connect_s3():
    client = boto3.resource('s3')
    data = []

    for bucket in client.buckets.all():
        bucket, bucket_location, AllUsers, AuthUsers =  check_bucket(bucket.name)
        data.append({'bucket':bucket, 'bucket_location':bucket_location, 'allusers':AllUsers, 'authusers':AuthUsers})

    display_data(data)

if __name__ == "__main__":
    try:
        print()
        connect_s3()
    except Exception as err:
        print(err)
