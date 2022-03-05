#!/bin/bash

# below is a sample script
linode-cli firewalls rules-update 50400 \
--inbound '[{"action":"ACCEPT", "protocol": "TCP", "ports": "22", "label":"allow-SSH-from-local", "description":"Hello world", "addresses": {"ipv4": ["192.0.2.1/32"]}}]'