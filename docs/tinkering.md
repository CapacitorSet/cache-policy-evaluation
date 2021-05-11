# Tinkering with this project

This document describes the inner workings of the project for anyone who wants to hack on it.

The overall structure of the project is as follows:

 - `entry.py` contains some parameters;
 - `simulate.py` exposes a simulate() function that runs a gem5 simulation. The CPU is a simplified model of `configs/learning_gem5/part1/simple.py` that uses the TimingSimpleCPU model from gem5 with a simple L1-L2-DDR3 memory hierarchy; it takes an argument of type `Entry` that describes the parameters to be customized, eg. the L1 size or the number of BTB entries.
 - `standalone.py` takes command-line arguments in a format that is compatible with `Entry`, and then calls `simulate()` on them.
 - `combination.py` creates an array of possible values for each parameter, then uses `itertools.product` to iterate through all possible combinations.

Note that `simulate.py` and `standalone.py` are meant to be run directly inside gem5 (`gem5.opt standalone.py`), but `combination.py` can't do that and will call gem5 manually for each combination.