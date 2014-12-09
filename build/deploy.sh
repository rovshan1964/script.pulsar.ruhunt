#!/bin/sh
cd `dirname $0`/../src

OLD=`cat ./addon.xml | grep '<addon' | grep 'version="' | grep -E -o 'version="[0-9\.]+"' |  grep -E -o '[0-9\.]+'`
echo "Old version: $OLD"
echo -n 'New version: '
read NEW

sed -e "s/Pulsar\" version=\"$OLD\"/Pulsar\" version=\"$NEW\"/g" ./addon.xml > ./addon2.xml
mv ./addon2.xml ./addon.xml

rm -rf ../script.pulsar.ruhunt
rm -f ./script.pulsar.ruhunt.zip
mkdir ../script.pulsar.ruhunt
cp -r ./* ../script.pulsar.ruhunt/

cd ../
zip -rq ./script.pulsar.ruhunt.zip ./script.pulsar.ruhunt

cp ./script.pulsar.ruhunt.zip ../repository.hal9000/repo/script.pulsar.ruhunt/script.pulsar.ruhunt-$NEW.zip

rm -rf ./script.pulsar.ruhunt
rm -f ./script.pulsar.ruhunt.zip

`../repository.hal9000/build/build.sh`
