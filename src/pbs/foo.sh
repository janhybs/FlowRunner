#!/bin/bash
#PBS -N simple-test-job
#PBS -l mem=200mb
#PBS -l scratch=400mb
#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:05:00
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

# nastaveni uklidu SCRATCHE pri chybe nebo ukonceni
# (pokud nerekneme jinak, uklidime po sobe)
trap 'clean_scratch' TERM EXIT

DATADIR="/storage/praha1/home/$LOGNAME/" # sdilene pres NFSv4

cp $DATADIR/vstup.txt $SCRATCHDIR  || exit 1
cd $SCRATCHDIR || exit 2

pwd
whoami
nproc
cat vstup.txt
cat vstup.txt > vystup.txt
cat vstup.txt >> vystup.txt
python -V
gcc --version

cp vystup.txt $DATADIR || export CLEAN_SCRATCH=false