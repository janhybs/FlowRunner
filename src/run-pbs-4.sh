#!/bin/bash
#PBS -N flow-test-production
#PBS -l mem=6gb
#PBS -l scratch=1gb
#PBS -l nodes=1:ppn=4
#PBS -l walltime=01:30:00
#PBS -j oe
#PBS -m abe
#

module purge
module add /software/modules/current/metabase
module add cmake-2.8
module add gcc-4.7.0
module add openmpi
module add perl-5.10.1
module add boost-1.49
module add python26-modules-gcc
module add numpy-py2.6
module add python-2.7.6-gcc

CPU_ARCH_AVAIL="4"
CPU_MEMORY_AVAIL="6442450944"
TESTS_OUTPUT_DIR="/auto/praha1/jan-hybs/projects/tests/__output/4"


cd /storage/praha1/home/jan-hybs/projects/FlowRunner/src
# run architecture detection (specify number of CPU and reserved memory)
python flowrunner/testing/script_environment.py -o ${TESTS_OUTPUT_DIR}/environment.json arch.cpu.avail=${CPU_ARCH_AVAIL} arch.memory.avail=8${CPU_MEMORY_AVAIL}
# run calibration tests with no. CPU up to 4 
python flowrunner/testing/script_performance.py -o ${TESTS_OUTPUT_DIR}/performance.json -c 1 -c 2 -c 3 -c 4


cd /storage/praha1/home/jan-hybs/projects/FlowRunner/src
# run benchmark tests on 1, 2, 3, 4, 6 and 8 CPUs
python flowrunner/flow/tests/script_run_tests.py --nproc=1:5 --nproc=6 --nproc=8 --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d"  --test-root="/auto/praha1/jan-hybs/projects/tests" --output-timestamp-dir="" --tests-output=${TESTS_OUTPUT_DIR} --randomize-output-folder=1

