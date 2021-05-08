# Compiling benchmarks

To compile a specific benchmark (eg. mibench/automotive/basicmath) inside the Docker container:

```sh
cd mibench/automotive/basicmath
make CC=/gem5/alphaev67-unknown-linux-gnu/bin/alphaev67-unknown-linux-gnu-gcc
```