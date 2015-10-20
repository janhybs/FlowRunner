#!/bin/bash
cd /storage/praha1/home/jan-hybs/projects/FlowRunner/
cd src
python testing/script_environment.py -o /storage/praha1/home/jan-hybs/projects/__output/environment.json arch.cpu.avail=4 arch.memory.avail=4g
python testing/script_performance.py -o /storage/praha1/home/jan-hybs/projects/__output/performance.json -c 1 -c 2 -c 3 -c 4