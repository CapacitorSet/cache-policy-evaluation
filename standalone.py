from optparse import OptionParser
from simulate import simulate

parser = OptionParser()
parser.set_usage("Usage: %prog [options] <binary to execute>")
parser.add_option("-p", "--policy", type="string",default="lru",
                    help="L1 I-cache eviction policy (one of random, lru, treelru, lip, mru, lfu, fifo, secondchance, nru, rrip, brrip). Default: lru")
# parser.add_option("-c", "--cache-policies", default="random,lru,treelru,lip,mru,lfu,fifo,secondchance,nru,rrip,brrip",
#                     help="comma-separated list of cache eviction policies to simulate (default: all existing ones"),
# parser.add_option("-d", "--cache-sizes", default="128,256,512,1024",
#                     help="comma-separated list of cache sizes to try, in bytes (default: 128,256,512,1024"),
parser.add_option("-t", "--cache-type", default="data",
                    help="which L1 cache to use (data or instruction, default: data)"),
parser.add_option("-1", "--l1-cache-size", default=1024,
                    help="L1 cache size in bytes"),
parser.add_option("-2", "--l2-cache-size", default=1024,
                    help="L2 cache size in bytes"),
# parser.add_option("-b", "--branch-predictors", default="",
#                     help="comma-separated list of branch prediction policies to simulate (default: all existing ones"),

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

simulate(opts.policy, opts.l1_cache_size, opts.l2_cache_size, opts.cache_type, binary)