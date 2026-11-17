#!/bin/bash
# build hostroot: pristine V30 gateway-release + stage overlay; big binaries hardlinked, rest copied
set -e
cd /home/user/work
rm -rf hostroot && mkdir -p hostroot/files
mkdir -p v30gw
if [ ! -f v30gw/.done ]; then unzip -q -o 73efootball-V30.apk 'assets/gateway-release/*' -x 'assets/gateway-release/livedata/*' 'assets/gateway-release/custom-resources/*' -d v30gw_tmp; cp -r v30gw_tmp/assets/gateway-release/. v30gw/; rm -rf v30gw_tmp; cp -al v30ga/assets/gateway-release/. v30gw/; touch v30gw/.done; fi
G=hostroot/files/embedded-gateway; mkdir -p $G
cp -al v30gw/livedata v30gw/custom-resources $G/
(cd v30gw && find . -path ./livedata -prune -o -path ./custom-resources -prune -o -type f -print) | while read f; do mkdir -p $G/$(dirname $f); cp $PWD/v30gw/$f $G/$f; done
rm -f $G/.done
(cd stage/assets/gateway-release && find . -type f) | while read f; do mkdir -p $G/$(dirname $f); rm -f $G/$f; if [[ $f == ./livedata/* || $f == ./custom-resources/* ]]; then ln stage/assets/gateway-release/$f $G/$f; else cp stage/assets/gateway-release/$f $G/$f; fi; done
rm -rf hostroot/app; mkdir -p hostroot/app; cp -r app/merged/. hostroot/app/
echo built
