#!/usr/bin/python3
# Compress before sending
"""Compress usign fabric -- all in one"""
from fabric.api import sudo, env, put, local
import os
import datetime


env.hosts = ['100.24.238.134', '54.208.230.191']


def do_pack():
    """compress function"""
    try:
        local("mkdir -p versions")
        date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        local("tar -cvzf versions/web_static_{}.tgz web_static".format(date))
        return "versions/web_static_{}.tgz".format(date)
    except Exception:
        return None


def deploy():
    """deploy archive to server"""
    archive_path = do_pack()
    if not os.path.isfile(archive_path):
        return False
    try:
        name = archive_path.split('/')[-1]
        put(archive_path, '/tmp/{}'.format(name))
        sudo('rm -rf /data/web_static/releases/{}'.format(name[0:-4]))
        sudo('mkdir -p /data/web_static/releases/{}'.format(name[0:-4]))
        sudo('tar -xzvf /tmp/{} -C /data/web_static/releases/{}'.format(name,
             name[0:-4]))
        sudo("mv -f /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}".format(name[0:-4],
             name[0:-4]))
        sudo('rm -f /tmp/{}'.format(name))
        sudo('rm -f /data/web_static/current')
        sudo("ln -sf /data/web_static/releases/{} \
        /data/web_static/current".format(name[0:-4]))
        return True
    except Exception:
        return False


def do_clean(number=0):
    """clean outdated"""
    files = sudo('ls /data/web_static/releases')
    files = files.split('  ')
    files.remove('test')
    print(files)
    print(len(files))
    files.sort()
    if number == 0:
        number = 1
    number = int(number) + 1
    it = len(files) - number
    for i in range(it):
        sudo('rm /data/web_static/releases/{}'.format(files[i]))
    current = os.getcwd()
    current = os.chdir(current + '/versions')
    files = os.listdir(current)
    files.sort()
    print(files)
    it = len(files) - number
    for i in range(it):
        os.remove(files[i])
    os.chdir('../')
