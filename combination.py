from optparse import OptionParser
from multiprocessing import Pool, Value, cpu_count
import itertools
import os
import subprocess
import csv

from entry import Entry, keys

parser = OptionParser()
parser.set_usage("Usage: %prog [options] <binary to execute>")
parser.add_option("-g", "--path", type="string",
                    help="Path to gem5 binary")
parser.add_option("-o", "--output", type="string", default="output.csv",
                    help="CSV output file (default: output.csv)")
parser.add_option("-j", "--jobs", type="int", default=cpu_count(),
                    help="Number of jobs to run in parallel (default: one per CPU core)")
parser.add_option("-P", "--prefix", type="str",
                    help="Prefix for stats file (default: binary filename)")
parser.add_option("-q", "--quiet", action="store_true", default=False,
                    help="Silence stdout and stderr from the binary (default: false)")
parser.add_option("-p", "--policy", type="string",default="lru",
                    help="Cache eviction policies (comma-separated list; one or more of of random,lru,treelru,lip,mru,lfu,fifo,secondchance,nru,rrip,brrip). Default: lru")
parser.add_option("-1", "--l1-size", default="1024",
                    help="L1 cache sizes (comma-separated list in bytes). Default: 1024"),
parser.add_option("-2", "--l2-size", default="0",
                    help="L2 cache sizes (comma-separated list in bytes). Default: 0"),
parser.add_option("-b", "--btb-entries", type="string",default="8",
                    help="Number of BTB entries (comma-separated list). Default: 8")
parser.add_option("-B", "--global-buffer", type="string",default="256",
                    help="Branch prediction buffer size (comma-separated list). Default: 256")

(opts, args) = parser.parse_args()

if len(args) == 0:
    print("A binary to run is required.")
    print("You can find a hello-world in tests/test-progs/hello/bin/arm/linux/hello inside the gem5 folder.")
    exit(1)
# Check if there was a binary passed in via the command line
elif len(args) == 1:
    binary = args[0]
# Error if there are too many arguments
elif len(args) > 1:
    parser.print_help()
    print("Expected a single binary to run. Arguments are not supported.")
    exit(1)

project_path = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(project_path + "/simulate.py"):
    print("Can't find simulate.py: expected to find it in " + project_path + ". Possibly a bug in combination.py?")
    exit(1)

if opts.prefix is None:
    opts.prefix = os.path.basename(binary) + "-"

if type(opts.path) != type("") or not os.path.isfile(opts.path):
    print("A valid gem5 path (-g) is required.")
    exit(1)

csv_outfile = open(opts.output, 'w', newline='', buffering=1)
outwriter = csv.writer(csv_outfile)

policies = opts.policy.split(",")
# cache_types = opts.cache_type.split(",")
l1_sizes = opts.l1_size.split(",")
l2_sizes = opts.l2_size.split(",")
btb_entries = opts.btb_entries.split(",")
global_buffers = opts.global_buffer.split(",")

for policy in policies:
    if policy not in ("random","lru","treelru","lip","mru","lfu","fifo","secondchance","nru","rrip","brrip"):
        print("Policy {} is unknown." % policy)

num_combinations = len(policies)*len(l1_sizes)*len(l2_sizes)*len(btb_entries)*len(global_buffers)
print(f"Iterating over {num_combinations} combinations with {opts.jobs} jobs.")

# write a header line to the csv
outwriter.writerow(keys + ("num_cycles",))
i = Value('i', 0)

def process_single(values):
    entry = Entry(*values)
    with i.get_lock():
        i.value += 1
        print("[{:.0%}, {}/{}] ".format(i.value/num_combinations, i.value, num_combinations), entry)

    output_filename = opts.prefix + entry.policy + "-" + entry.l1_size + "-" + entry.l2_size + ".txt"
    gem5_binary = [opts.path,
        "--quiet",
        "--stats-file", output_filename,
    ]
    if opts.quiet:
        gem5_binary = gem5_binary + ["--redirect-stdout",
            "--stdout-file=/dev/null"]
    subprocess.run(gem5_binary + [
        project_path + "/standalone.py",
        "--policy", entry.policy,
        "--l1-size", entry.l1_size,
        "--l2-size", entry.l2_size,
        "--btb-entries", entry.btb_entries,
        "--global-buffer", entry.global_buffer,
        binary
    ], check=True)

    for line in open("m5out/" + output_filename, "r"):
        if line[:20] == "system.cpu.numCycles":
            parts = line.split(" ")
            num_cycles = [int(p) for p in parts if p.isnumeric()][0]
            outwriter.writerow(values + (num_cycles,))

with Pool(processes=opts.jobs) as pool:
    # Some params are hardcoded for simplicity. It's trivial to add support for them though
    # Note that the order must match that of Entry
    speeds = ["1 GHz"]
    predictors = ["local"]
    ras_sizes = ["8"]
    local_buffers = ["1"]
    iterator = itertools.product(speeds, policies, l1_sizes, l2_sizes, predictors, btb_entries, global_buffers, local_buffers, ras_sizes)
    pool.map(process_single, iterator)