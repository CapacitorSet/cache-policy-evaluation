# cache-policy-evaluation

Evaluate cache replacement and branch prediction policies with gem5 simulations.

This is a tool to simulate different types of workloads on a simple CPU, running a given benchmark on a matrix (Cartesian product) of policies and L1-i/L1-d cache sizes. The output is a simple CSV file that can be later plotted and analyzed; a Jupyter notebook is given.

The CPU is described in `simulate.py`: it is a simplified model of `configs/learning_gem5/part1/simple.py` that uses the TimingSimpleCPU model from gem5 with a simple L1-DDR3 memory hierarchy.

For detailed information refer to the `docs/` folder:

 - It is recommended to start with `gem5_on_alpha.md` to set up the simulation environment.
 - Then, read `benchmarks.md` to understand how to compile benchmarks and which ones are of interest to you.
 - Then, read `cache_experiments.md` to run your first experiment and learn how to process the data.
 - `branch_prediction_experiments.md` will then explain how to use different branch predictors.
 - `single_simulations.md` and `existing_cpus.md` are for one-shot simulations.
 - If you want to hack on this project, `tinkering.md` has a few notes to get you up and running on the internals.

Finally, in `notebooks/graphs.html` you can find a simple analysis of simulation data comparing different cache replacement policies in several scenarios.
