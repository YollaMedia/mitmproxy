#!/bin/bash

# Grab directory this script is located in
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# CMD="/usr/local/bin/mitmdump -T --cert=${DIR}/certs/server.pem --no-upstream-cert -s ${DIR}/revProxy.py"
CMD="browserup-proxy"

while eval $CMD; do
        echo "Proxy crashed with exit code $?, restarting..." >&2
        sleep 1
done

echo "Proxy Done"

exit 0