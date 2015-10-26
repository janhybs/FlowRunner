#!/bin/bash
#PBS -N flow-test
#PBS -l mem=4gb
#PBS -l scratch=1gb
#PBS -l nodes=1:ppn=3
#PBS -l walltime=01:00:00
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

#!/bin/bash
cd /storage/praha1/home/jan-hybs/projects/FlowRunner/
cd src
python testing/script_environment.py -o /storage/praha1/home/jan-hybs/projects/__output/environment.json arch.cpu.avail=4 arch.memory.avail=4g
python testing/script_performance.py -o /storage/praha1/home/jan-hybs/projects/__output/performance.json -c 1 -c 2 -c 3 -c 4
#!/bin/bash
cd /storage/praha1/home/jan-hybs/projects/FlowRunner/
cd src
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir=""