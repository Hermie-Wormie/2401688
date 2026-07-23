#!/bin/sh
mkdir -p /home/git/.ssh
cp /tmp/keys/authorized_keys /home/git/.ssh/authorized_keys
chown -R git:git /home/git/.ssh
chmod 700 /home/git/.ssh
chmod 600 /home/git/.ssh/authorized_keys