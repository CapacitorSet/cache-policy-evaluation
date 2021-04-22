# cache-policy-evaluation

Evaluate cache replacement policies with gem5 simulations. Work in progress.

This is a tool to simulate different types of workloads on a simple CPU, running a given benchmark on a matrix (Cartesian product) of policies and L1-i/L1-d cache sizes. The output is a simple CSV file that can be later plotted and analyzed; a Jupyter notebook is given.

The CPU is described in `simulate.py`: it is a simplified model of `configs/learning_gem5/part1/simple.py` that uses the TimingSimpleCPU model from gem5 with a simple L1-DDR3 memory hierarchy.

The list of known policies can also be found in `simulate.py`.

**Known issues with ALPHA**:

 - You must use a different syntax for the memory controller, but simulate.py should take care of that automatically.
 - If cross-compiling on Ubuntu, you cannot use `alpha-linux-gnu-gcc-10` as it will cause mysterious null ptr derefs ("Tried to access unmapped address 0"). A known-good version is at http://www.m5sim.org/dist/current/alphaev67-unknown-linux-gnu.tar.bz2; just decompress it with `tar -xjvf alphaev67-unknown-linux-gnu.tar.bz2` and use `bin/alphaev67-unknown-linux-gnu-gcc` as a compiler.

## Usage

You might want to compile a benchmark from `mibench` before running simulations. To use a custom compiler (eg. the ALPHA compiler mentioned previously):

```bash
make CC=path/to/compiler
```

Note that if you use the gem5-dev Docker image you must also run the following (inside the container):

```bash
export GEM5_PATH=/gem5/configs
```

### Single simulation

To run a single simulation, use `standalone.py` *from gem5*, eg.

```bash
/gem5/build/ALPHA/gem5.opt standalone.py mibench/automotive/basicmath/basicmath_small
```

### Marix of simulations

To run a matrix of simulations, use `combination.py`. The output will be a CSV file.
