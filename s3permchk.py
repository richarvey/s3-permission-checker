#!/usr/bin/env python3

import boto3
import json
import os,sys
import argparse
from texttable import Texttable

def get_options():
  parser = argparse.ArgumentParser(description='TAD_builder tool')
  parser.add_argument('-p','--profile', metavar='profile', help='profile in .aws/config', required=False)
  args = vars(parser.parse_args())
  profile = args['profile']
  return(profile)

def check_bucket(bucket, client):
    try:
        bucket_location = client.get_bucket_location(Bucket=bucket)['LocationConstraint']
        if (bucket_location == None):
            bucket_location = 'us-east-1'
    except:
        return(bucket, "FAIL_LOC", "FAIL", "FAIL")
    try:
        bucket_acl = client.get_bucket_acl(Bucket=bucket)
    except:
        return(bucket, "FAIL", "FAIL_ACL", "FAIL_ACL")
        
    permission = []
    auth_permission = []
        
    AllUsers = []
    AuthUsers = []

    for grants in bucket_acl['Grants']:
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

def connect_s3(profile):
    if(profile != None):
        boto3.setup_default_session(profile_name=profile)
    resource = boto3.resource('s3')
    client = boto3.client('s3')
    return(resource, client)


def s3_perm_chk(profile):
    resource, client = connect_s3(profile)
    data = []
    for bucket in resource.buckets.all():
        bucket, bucket_location, AllUsers, AuthUsers =  check_bucket(bucket.name, client)
        data.append({'bucket':bucket, 'bucket_location':bucket_location, 'allusers':AllUsers, 'authusers':AuthUsers})

    display_data(data)

if __name__ == "__main__":
    try:
        profile = get_options()
        s3_perm_chk(profile)
    except Exception as err:
        print(err)
