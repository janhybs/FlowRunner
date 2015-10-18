#!/bin/bash
#PBS -N flow-and-env
#PBS -l mem=4gb
#PBS -l scratch=1gb
#PBS -l nodes=1:ppn=4
#PBS -l walltime=01:30:00
#PBS -j oe
#PBS -m abe
#

module purge
module add /software/modules/current/metabase
module add cmake-2.8
module add python-2.7.6-gcc
module add gcc-4.7.0
module add openmpi
module add perl-5.10.1
module add boost-1.49
module add python26-modules-gcc
module add numpy-py2.6

CPU_ARCH_AVAIL="1"
CPU_MEMORY_AVAIL="4gb"

#!/usr/bin/env bash

DATADIR="$PBS_O_WORKDIR"

git clone https://github.com/x3mSpeedy/FlowRunner.git
cd FlowRunner/src
rm performance.json || echo "no such file"
python test.py -c 1 -c 2 -c 3 -c 4 -x "matrix-creation" -x "matrix-solve" -x "_matrix-solve" -x "_matrix-creation"
cp performance.json $DATADIR || export CLEAN_SCRATCH=false


git clone https://github.com/flow123d/flow123d.git
cd flow123d
cp config/config-jenkins-linux-debug.cmake config.cmake
cmake . > flow123d-build.log 2>&1
cp flow123d-build.log $DATADIR || export CLEAN_SCRATCH=false