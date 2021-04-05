# cache-policy-evaluation

Evaluate cache replacement policies with gem5 simulations. Work in progress.

This is a tool to simulate different types of workloads on a simple CPU, running a given benchmark on a matrix (Cartesian product) of policies and L1-i/L1-d/L2 cache sizes. The output is a simple CSV file that can be later plotted and analyzed; a Jupyter notebook is given.

The CPU is described in `simulate.py`: it is based off the TimingSimpleCPU model from gem5 with a simple L1-L2-DDR3 memory hierarchy.

The list of known policies can also be found in `simulate.py`.

## Usage

You might want to compile a benchmark from `mibench` before running simulations.

### Single simulation

To run a single simulation, use `standalone.py`.

### Marix of simulations

To run a matrix of simulations, use `combination.py`. The output will be a CSV file.