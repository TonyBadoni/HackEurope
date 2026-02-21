#!/bin/bash
set -e

# Run insecure setup
/app/setup.sh

# Generate host keys if missing
ssh-keygen -A

# Start SSH daemon
/usr/sbin/sshd

# Start Flask app
exec python app.py
