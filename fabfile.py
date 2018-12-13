import os
import smtplib

from fabric.api import local, settings, abort, run, cd, env, execute

env.user = ''
env.hosts = ['']
env.password = ''
env.root = ''

def collect_static():
    """
    Collect static files to the STATIC_ROOT directory.
    """
    with cd(env.root):
        run("python3 manage.py collectstatic --noinput")

def launch_gunicorn():
    with cd(env.root):
        run('./start.sh',pty=False)

def update():
    execute(collect_static)
    execute(launch_gunicorn)




