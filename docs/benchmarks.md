# Benchmarks

This project contains a small, representative sample of embedded benchmarks from [MiBench](http://vhosts.eecs.umich.edu/mibench/), specifically:

 - `automotive/basicmath`, a series of arithmetic operations
 - `automotive/bitcount`, doing bit operations (crashes on ALPHA)
 - `automotive/qsort`, sorting an array
 - `automotive/susan`, processing an image
 - `telecomm/FFT`, computing the Fast Fourier Transform

## Compiling

To compile a specific benchmark (eg. mibench/automotive/basicmath) inside the Docker container:

```sh
cd /gem5/project/mibench/automotive/basicmath
make CC=/gem5/alphaev67-unknown-linux-gnu/bin/alphaev67-unknown-linux-gnu-gcc
```

## Characterization

The metrics here are measured on the Cortex-A9 preset with the ALPHA architecture.

From least to most CPU-intensive (`sim_seconds`):

 - susan: 4.1 ms
 - fft: 57.0 ms
 - qsort: 130.2 ms
 - basicmath: 349.8 ms

From least to most memory-intensive (`system.mem_ctrl.bytes_read::total`):

 - susan: 93 kB
 - fft: 127 kB
 - basicmath: 147 kB
 - qsort: 15 MB

From least to most branch-intensive (`system.cpu.Branches`/`sim_insts`):

 - basicmath: 9.2%
 - susan: 9.5%
 - qsort: 12.8%
 - fft: 17%