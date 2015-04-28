#!/bin/bash

# 10 seconds interval time by default
INTERVAL=${INTERVAL:-10}

# Consul config directory
DNSMASQ_CONFIG=${DNSMASQ_CONFIG:-.}

# commands used in this script
DOCKER=${DOCKER:-docker}
SLEEP=${SLEEP:-sleep}
TAIL=${TAIL:-tail}

declare -A service_map

while true
do
    while read line
    do
        changed=false
        name=${line##* }
        ip=$(${DOCKER} inspect --format '{{.NetworkSettings.IPAddress}}' $name)
        if [ -z ${service_map[$name]} ] || [ ${service_map[$name]} != $ip ]
        then
            service_map[$name]=$ip
            # write to file
            echo $name has a new IP Address $ip >&2
            echo "host-record=$name,$ip"  > "${DNSMASQ_CONFIG}/docker-$name"
            changed=true
        else
            echo $name is unchanged.
        fi

        if [ $changed = true ];
        then
            systemctl restart dnsmasq
        fi
    done < <(${DOCKER} ps | ${TAIL} -n +2)

    ${SLEEP} $INTERVAL
done
