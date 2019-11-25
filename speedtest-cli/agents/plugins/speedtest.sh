#!/usr/bin/env bash

MK_CONFDIR=${MK_CONFDIR:-/etc/check_mk}
CONFIG=${MK_CONFDIR}/speedtest.cfg

if type speedtest-cli >/dev/null; then
	echo "<<<speedtest:sep(44)>>>"

    SERVER=""
    SECURITY=""

	if [ -e ${CONFIG} ]; then
		. ${CONFIG}
	fi

	if [ -z ${SERVER} ]; then
		SERVER="6601" # NetCologne Server, Cologne, Germany
	fi

	if [ "${SECURITY}" -eg "yes" ]; then
		SECURITY="--secure"
	fi

        speedtest-cli --csv-header
        speedtest-cli --csv ${SECURITY} --server ${SERVER} --share
fi
