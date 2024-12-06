#!/usr/bin/env bash

MK_CONFDIR=${MK_CONFDIR:-/etc/check_mk}
CONFIG=${MK_CONFDIR}/speedtest.cfg

for SPEEDTEST in speedtest speedtest-cli; do
    if type ${SPEEDTEST}; then
        break
    else
        SPEEDTEST=
    fi
done

if type ${SPEEDTEST} >/dev/null; then
    echo "<<<speedtest:sep(44)>>>"

    SERVER=""
    SECURITY=""

    if [ -e ${CONFIG} ]; then
        . ${CONFIG}
    fi

    if [ -z ${SERVER} ]; then
        SERVER="6601" # NetCologne Server, Cologne, Germany
    fi

    if [ "${SECURITY}" -eq "yes" ]; then
        SECURITY="--secure"
    fi

    ${SPEEDTEST} --csv-header
    ${SPEEDTEST} --csv ${SECURITY} --server ${SERVER} --share
fi
