#!/usr/bin/python3
# -*- up coding: utf-8 -*-
# deploy sending

"""deploy archive usign fabric"""

from fabric.api import sudo, env, put
import os


env.hosts = ['35.168.8.139', '54.157.191.131']


def do_deploy(archive_path):
    """deploy archive to server"""

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
