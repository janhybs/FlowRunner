#!/bin/bash
cd /storage/praha1/home/jan-hybs/projects/FlowRunner/
cd src
python environment.py -o environment.json arch.cpu.avail=4 arch.memory.avail=4g
python performance.py -o performance.json -c 1 -c 2 -c 3 -c 4