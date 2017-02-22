# -*- coding: utf-8 -*-
import os
import traceback

import boto3
import paramiko
from tornado.log import gen_log, enable_pretty_logging
# from apscheduler.schedulers.blocking import BlockingScheduler

enable_pretty_logging()
gen_log.setLevel(1)

s3 = None
_bucket_name = None


def start():
    gen_log.info('sycn sftp!')
    try:
        _start()
    except Exception as e:
        gen_log.error(e)
        gen_log.error(traceback.format_exc())


def init_s3(access_key, secret_key, settlement_bucket_name, region, **kwargs):
    global s3
    global _bucket_name
    s3 = boto3.client(
        's3',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    _bucket_name = settlement_bucket_name


def get_sftp_session(hostname, username, password=None, port=22, pk_path=None):
    try:
        t = paramiko.Transport((hostname, port))
        if pk_path:
            private_key = paramiko.RSAKey.from_private_key_file(pk_path)
            t.connect(username=username, pkey=private_key)
        elif username:
            t.connect(username=username, password=password)
        else:
            t.connect(username=username)

        gen_log.debug('SFTP Connection Succeed, hostname: {}, user: {}, port: {}'.format(
            hostname, username, port))
        # open session
        return paramiko.SFTPClient.from_transport(t)
    except Exception as e:
        gen_log.error('STTP Connection Failed, {}'.format(e))
        try:
            t.close()
        except:
            pass


def safe_path(path):
    if not os.path.exists(path):
        gen_log.debug('mkdir {}'.format(path))
        os.makedirs(path)
    return path


def init():
    init_s3('', '', '', '')


def upload_s3():
    while True:
        file_path = yield
        with open(file_path, 'r'):
            gen_log.info('uploading file to s3')
            s3.upload_fileobj(fp, _bucket_name, key_name)
            gen_log.info('uploaded file to s3')


hostname = 'localhost'
username = 'root'
port = 22

remote_path = 'remote/path/to'
local_path = safe_path('local/path/to')

s3 = upload_s3()
s3.send(None)


def sync(session, filename, src_path=None, des_path=None):
    src_path = os.path.join(src_path, filename)
    des_path = os.path.join(des_path, filename)

    stat = session.lstat(src_path)
    ptype = str(stat)[0]

    if ptype == 'd':
        files = session.listdir(src_path)
        [sync(session, f, src_path, safe_path(des_path)) for f in files]
    elif ptype == '-':
        gen_log.debug('sync file {} to {}'.format(src_path, des_path))
        session.get(src_path, des_path)
        s3.send(des_path)


def _start():
    global remote_path
    session = get_sftp_session(hostname, username, port, pk_path='.ssh/id_rsa')
    remote_path = session.normalize(remote_path)

    remote_file = set(session.listdir(remote_path))
    local_file = set(os.listdir(local_path))
    delta_file = remote_file - local_file
    gen_log.debug('delta file {}'.format((delta_file)))

    [sync(session, filename, remote_path, local_path) for filename in delta_file]

    session.close()

if __name__ == '__main__':
    init()
    start()
