#!/bin/bash

echo "Updating linode firewall rules"

# # firewall_rules_inbound='[{"action":"ACCEPT", "protocol": "TCP", "ports": "22", "label":"allow-SSH-from-github", "description":"Allow inbound ssh from github actions pipeline", "addresses": {"ipv4": ["192.0.2.1/32"]}},{"action":"ACCEPT", "protocol": "TCP", "ports": "22", "label":"allow-SSH-from-home", "description":"Allow inbound shh from home pc", "addresses": {"ipv4": ["8.39.18.208/32"]}}]'

github_action_publicip=$(curl -l http://checkip.amazonaws.com/)

echo "Github action pipeline runner public ip is : $github_action_publicip"

publicip_in_json_acceptable_format="\""$github_action_publicip"/32\""

echo "Github action pipeline runner public ip in /32 format is : $publicip_in_json_acceptable_format"

read -r -d '' json_github_action_publicip_rule <<EOM
{
        "action": "ACCEPT",
        "protocol": "TCP",
        "ports": "22",
        "label": "allow-SSH-from-github",
        "description": "Allow inbound ssh from github actions pipeline",
        "addresses": {
            "ipv4": [
                $publicip_in_json_acceptable_format
            ]
        }
    }
EOM

read -r -d '' json_home_publicip_rule <<EOM
{
        "action": "ACCEPT",
        "protocol": "TCP",
        "ports": "22",
        "label": "allow-SSH-from-home",
        "description": "Allow inbound shh from home pc",
        "addresses": {
            "ipv4": [
                "8.39.18.208/32"
            ]
        }
    }
EOM

read -r -d '' common_deny_all_inbound_rule <<EOM
{
        "action": "DROP",
        "protocol": "TCP",
        "ports": "22",
        "label": "deny-SSH-from-everywhere",
        "description": "DROP/Deny inbound shh from everywhere else",
        "addresses": {
            "ipv4": [
                "0.0.0.0/0"
            ]
        }
    }
EOM

if [ "$1" == "addgithub-pip" ]; then
    read -r -d '' firewall_rules_inbound <<EOM
[
    $json_github_action_publicip_rule, 
    $json_home_publicip_rule,
    $common_deny_all_inbound_rule
]
EOM

elif [ "$1" == "removegithub-pip" ]; then
    read -r -d '' firewall_rules_inbound <<EOM
    [
    $json_home_publicip_rule,
    $common_deny_all_inbound_rule
    ]
EOM
fi

linode-cli firewalls rules-update 50400 \
    --inbound "$firewall_rules_inbound" \
    --json --pretty

echo "Sleeping for 20s, allowing firewall rules to take effect"

if [ "$1" == "addgithub-pip" ]; then
    sleep 20
fi