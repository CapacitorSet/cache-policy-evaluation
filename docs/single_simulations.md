# Single simulations

To run a single simulation with given parameters, just use `standalone.py`; pass `--help` for a list of parameters.

This is especially useful for quick experiments or if you have a use case that `combination.py` does not cover. For instance, to run a few benchmarks over a list of presets the following command line is used:

```sh
for preset in {cortex-a8,cortex-a9,stm32mp1,stm32h7}; do for benchmark in /gem5/project/mibench/{automotive/basicmath/basicmath_small,automotive/bitcount/bitcnts,automotive/qsort/qsort_small,automotive/susan/susan,telecomm/FFT/fft}; do echo $preset $benchmark; gem5 --redirect-stdout --stdout-file /dev/null --outdir $preset --stats-file $(basename $benchmark).txt /gem5/project/standalone.py --preset $preset $benchmark; done; done
```

Note the use of `--outdir` and `--stats-file` to ensure that statistics files do not overlap.