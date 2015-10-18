#!/usr/bin/env bash

DATADIR="$PBS_O_WORKDIR"


cd $DATADIR
git clone https://github.com/x3mSpeedy/FlowRunner.git
cd FlowRunner/src
rm performance.json || echo "no such file"
python environment.py -o environment.json arch.cpu.avail=4 arch.memory.avail=4g
python performance.py -o performance.json -c 1 -c 2 -c 3 -c 4 -x "matrix-creation" -x "matrix-solve" -x "_matrix-solve" -x "_matrix-creation"


cd $DATADIR
git clone https://github.com/flow123d/flow123d.git
cd flow123d
cp config/config-jenkins-linux-debug.cmake config.cmake
cmake . > flow123d-build.log 2>&1
cp flow123d-build.log $DATADIR || export CLEAN_SCRATCH=false



cd $DATADIR
mkdir data
find . -type f -name *.json -exec cp --parent {} $DATADIR/data