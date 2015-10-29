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
moduel add

module rm python-2.7.6-gcc
module add python-2.7.6-gcc


CPU_ARCH_AVAIL="3"
CPU_MEMORY_AVAIL="4gb"

#!/bin/bash
cd /storage/praha1/home/jan-hybs/projects/FlowRunner/
cd src
python testing/script_environment.py -o /storage/praha1/home/jan-hybs/projects/Flow123d/flow123d/tests/__output/environment.json arch.cpu.avail=4 arch.memory.avail=4g
python testing/script_performance.py -o /storage/praha1/home/jan-hybs/projects/Flow123d/flow123d/tests/__output/performance.json -c 1 -c 2 -c 3 -c 4
#!/bin/bash
cd /storage/praha1/home/jan-hybs/projects/FlowRunner/
cd src
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="01_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="02_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="03_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="04_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="05_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="06_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="07_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="08_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="09_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="09_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="10_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="11_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="12_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="13_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="14_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="15_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="16_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="17_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="18_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="19_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="20_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="21_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="22_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="23_.*"
python flow/tests/script_run_tests.py --flow-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d" --output-timestamp-dir="" --select-dir-rule="24_.*"