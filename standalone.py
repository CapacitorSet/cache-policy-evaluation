from optparse import OptionParser
from simulate import simulate

import presets

parser = OptionParser()
parser.set_usage("Usage: %prog [options] <binary to execute>")
parser.add_option("-s", "--speed", type="string",default="1GHz",
                    help="Clock speed (given with unit, no spaces). Default: 1GHz")
parser.add_option("-p", "--policy", type="string",default="lru",
                    help="L1 I-cache eviction policy (one of random, lru, treelru, lip, mru, lfu, fifo, secondchance, nru, rrip, brrip). Default: lru")
parser.add_option("-1", "--l1-size", default=1024,
                    help="L1 cache size in bytes"),
parser.add_option("-2", "--l2-size", default=1024,
                    help="L2 cache size in bytes"),
parser.add_option("-b", "--predictor", default="local",
                    help="Branch predictor (one of local, tournament, bimode)"),
parser.add_option("-P", "--preset", type="string",default="",
                    help="Use a known processor (one of cortex-a8, cortex-a9, stm32mp1, stm32h7). Default: no preset")

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

if opts.preset != "":
    print("[!] Using a preset; other command line flags will be ignored.")
    if opts.preset == "cortex-a8":
        opts = presets.cortex_a8
    elif opts.preset == "cortex-a9":
        opts = presets.cortex_a9
    elif opts.preset == "stm32mp1":
        opts = presets.stm32mp1
    elif opts.preset == "stm32h7":
        opts = presets.stm32h7
    else:
        print("Unknown preset " + opts.preset)
        exit(1)

simulate(opts, binary)