from __future__ import print_function

import urllib
import boto3
import os.path
import uuid

import sys
sys.path.insert(0, "./lib")
from sftp import *
from base64 import b64decode

host = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['host']))['Plaintext']
remote_path = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['remote_path']))['Plaintext']
username = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['username']))['Plaintext']
password = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['password']))['Plaintext']

s3 = boto3.client('s3')

def object_created(bucket, key):
    try:
        ssh = SSHConnection(host, username, password)
        try:
            file='/tmp/'+str(uuid.uuid4())
            try:
                s3.download_file(bucket, key, file)
            except Exception as e:
                print(e)
                print('ERROR: download')
                raise
            try:
                ssh.put(file, '/'+bucket+'-'+remote_path, key)
                os.remove(file)
            except Exception as e:
                print(e)
                print('ERROR: put')
                raise
        except Exception as e:
            print(e)
            print('ERROR: params')
            raise
    except Exception as e:
        print(e)
        print('ERROR: connection')
        raise
    ssh.close()

def object_removed(bucket, key):
    try:
        ssh = SSHConnection(host, username, password)
        try:
            ssh.remove('/'+bucket+'-'+remote_path, key)
        except Exception as e:
            print(e)
            print('ERROR: params')
            raise
    except Exception as e:
        print(e)
        print('ERROR: connection')
        raise
    ssh.close()

def main (event, context):
    #print("Received event: " + json.dumps(event['Records'][0]['eventName'], indent=2))
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    eventName = event['Records'][0]['eventName']
    print('Received ['+bucket+'] event')
    if "ObjectCreated" in eventName:
        object_created(bucket, key)
    elif "ObjectRemoved" in eventName:
        object_removed(bucket, key)
    else:
        print('ERROR: Unknown eventName')