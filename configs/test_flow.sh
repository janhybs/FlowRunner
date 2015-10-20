#!/bin/bash
cd /storage/praha1/home/jan-hybs/projects/Flow123d/
cd flow123d
python flow/tests/script_run_tests.py --flow123d="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d/build_tree/bin/flow123d" --mpiexec="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d/build_tree/bin/mpiexec" --ndiff="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d/ndiff/ndiff.pl" --test-root="/storage/praha1/home/jan-hybs/projects/Flow123d/flow123d/tests" --tests-output="__output"