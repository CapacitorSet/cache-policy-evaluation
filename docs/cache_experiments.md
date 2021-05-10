# Running cache experiments

The `combination.py` script is used to run a matrix of simulations with varying cache replacement policies and cache sizes.

## Running the simulation

Assuming you already followed the documentation in *Running gem5 on ALPHA* and *Compiling benchmarks*, just run the following in the container:

```sh
cd /gem5
python3 project/combination.py -g /gem5/source/build/ALPHA/gem5.opt --help # Will show you a list of possible options
```

For example, suppose that you had a 32 KB L1 cache, no L2 cache, and wanted to try out a few cache replacement policies:

```sh
cd /gem5
python3 project/combination.py -g /gem5/source/build/ALPHA/gem5.opt --l1-size=32768 --l2-size=0 --policy=random,lru,treelru,lip,fifo /gem5/project/mibench/automotive/basicmath/basicmath_small
```

Or if you wanted to see how LRU behaves over a range of L1 cache sizes, from high cache pressure to low:

```sh
cd /gem5
python3 project/combination.py -g /gem5/source/build/ALPHA/gem5.opt --l1-size=1024,2048,4096,8192,16384,32768,65536 --l2-size=0 --policy=lru /gem5/project/mibench/automotive/basicmath/basicmath_small
```

Or yet, how a given benchmark performs over a handful of L1 and L2 cache sizes and the LRU policy:

```sh
cd /gem5
# L2 sizes: 0, 64 KB, 256 KB, 1 MB, 4 MB
python3 project/combination.py -g /gem5/source/build/ALPHA/gem5.opt --l1-size=4096,8192,16384,32768 --l2-size=0,65536,262144,1048576,4194304 --policy=lru /gem5/project/mibench/automotive/basicmath/basicmath_small
```

> If you're done debugging and you know that the benchmark works, you can reduce the amount of information printed to the screen with `--quiet`.

## Collecting the results

As the simulations finish, the cycle counts will be written to `output.csv` (unless specified otherwise with -o). You can then simply import this file in Excel or Pandas and analyse the data as needed; an example Jupyter notebook comparing the performance of different policies is given.

Note that `output.csv` is rewritten for each experiment (each command line run). If you were to try out different benchmarks you'll need to run one experiment per benchmark (possibly in parallel, if you have enough CPUs and know how to use tmux!), and pick a different output file for each (-o flag):

```sh
cd /gem5
# L2 sizes: 0, 64 KB, 256 KB, 1 MB, 4 MB
python3 project/combination.py -g /gem5/source/build/ALPHA/gem5.opt --l1-size=1024,2048,4096,8192,16384,32768,65536 --l2-size=0 --policy=lru /gem5/project/mibench/automotive/basicmath/basicmath_small -o basicmath.csv
python3 project/combination.py -g /gem5/source/build/ALPHA/gem5.opt --l1-size=1024,2048,4096,8192,16384,32768,65536 --l2-size=0 --policy=lru /gem5/project/mibench/automotive/bitcount/bitcnts -o bitcount.csv
python3 project/combination.py -g /gem5/source/build/ALPHA/gem5.opt --l1-size=1024,2048,4096,8192,16384,32768,65536 --l2-size=0 --policy=lru /gem5/project/mibench/automotive/susan/susan -o susan.csv
```

If you want to conduct deeper analyses, the full gem5 output is provided. In `m5out` you will find one file per simulation, with the format `prefix-policy-predictor-l1_size-l2_size.txt`:

```
root@4a3c2463127c:/gem5# python3 project/combination.py -g /gem5/source/build/ALPHA/gem5.opt --l1-size=1024,2048,4096,8192,16384,32768,65536 --l2-size=0 --policy=lru /gem5/project/mibench/automotive/susan/susan -o susan.csv -q
Iterating over 7 combinations with 2 jobs.
[14%, 1/7]  Entry(policy='lru', l1_size='1024', l2_size='0', predictor='local', btb_entries=8, ras_size=8, global_buffer=256, local_buffer=0)
[29%, 2/7]  Entry(policy='lru', l1_size='2048', l2_size='0', predictor='local', btb_entries=8, ras_size=8, global_buffer=256, local_buffer=0)
Redirecting stdout and stderr to /dev/null
Redirecting stdout and stderr to /dev/null
[43%, 3/7]  Entry(policy='lru', l1_size='4096', l2_size='0', predictor='local', btb_entries=8, ras_size=8, global_buffer=256, local_buffer=0)
[57%, 4/7]  Entry(policy='lru', l1_size='8192', l2_size='0', predictor='local', btb_entries=8, ras_size=8, global_buffer=256, local_buffer=0)
Redirecting stdout and stderr to /dev/null
Redirecting stdout and stderr to /dev/null
[71%, 5/7]  Entry(policy='lru', l1_size='16384', l2_size='0', predictor='local', btb_entries=8, ras_size=8, global_buffer=256, local_buffer=0)
[86%, 6/7]  Entry(policy='lru', l1_size='32768', l2_size='0', predictor='local', btb_entries=8, ras_size=8, global_buffer=256, local_buffer=0)
Redirecting stdout and stderr to /dev/null
Redirecting stdout and stderr to /dev/null
[100%, 7/7]  Entry(policy='lru', l1_size='65536', l2_size='0', predictor='local', btb_entries=8, ras_size=8, global_buffer=256, local_buffer=0)
Redirecting stdout and stderr to /dev/null
root@4a3c2463127c:/gem5# ls m5out/
config.ini   susan-lru-local-1024-0.txt   susan-lru-local-2048-0.txt   susan-lru-local-4096-0.txt   susan-lru-local-8192-0.txt
config.json  susan-lru-local-16384-0.txt  susan-lru-local-32768-0.txt  susan-lru-local-65536-0.txt
```

These files are gem5 outputs, so you can analyze them as usual. For instance, if you're interested in the number of D-cache misses:

```
root@4a3c2463127c:/gem5# grep 'system.cpu.dcache.overall_misses::total' m5out/susan-*                    
m5out/susan-lru-local-1024-0.txt:system.cpu.dcache.overall_misses::total         14096                       # number of overall misses
m5out/susan-lru-local-16384-0.txt:system.cpu.dcache.overall_misses::total          1177                       # number of overall misses
m5out/susan-lru-local-2048-0.txt:system.cpu.dcache.overall_misses::total          8277                       # number of overall misses
m5out/susan-lru-local-32768-0.txt:system.cpu.dcache.overall_misses::total           932                       # number of overall misses
m5out/susan-lru-local-4096-0.txt:system.cpu.dcache.overall_misses::total          5741                       # number of overall misses
m5out/susan-lru-local-65536-0.txt:system.cpu.dcache.overall_misses::total           876                       # number of overall misses
m5out/susan-lru-local-8192-0.txt:system.cpu.dcache.overall_misses::total          1594                       # number of overall misses
```