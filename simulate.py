from __future__ import absolute_import

# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *

# Add the common scripts to our path
gem5_path = os.environ.get("GEM5_PATH") or (os.path.expanduser("~") + '/gem5/configs/')
print("gem5_path:", gem5_path)
m5.util.addToPath(gem5_path)

# import the caches which we made
from caches import *


def simulate(policy, l1_cache_size, binary):
    if policy == 'random':
        policy_obj = RandomRP()
    elif policy == 'lru':
        policy_obj = LRURP()
    elif policy == 'treelru':
        policy_obj = TreePLRURP()
    elif policy == 'lip':
        policy_obj = LIPRP()
    elif policy == 'mru':
        policy_obj = MRURP()
    elif policy == 'lfu':
        policy_obj = LFURP()
    elif policy == 'fifo':
        policy_obj = FIFORP()
    elif policy == 'secondchance':
        policy_obj = SecondChanceRP()
    elif policy == 'nru':
        policy_obj = NRURP()
    elif policy == 'rrip':
        policy_obj = RRIPRP()
    elif policy == 'brrip':
        policy_obj = BRRIPRP()
    else:
        raise Exception("Unknown policy " + policy + ". Known policies:" + (",".join([it for it in globals() if it[-2:] == "RP"])))

    if cache_type not in ("data", "instruction"):
        raise Exception("--cache-type must be either 'data' or 'instruction'")

    # create the system we are going to simulate
    system = System()

    # Set the clock fequency of the system (and all of its children)
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = '1GHz'
    system.clk_domain.voltage_domain = VoltageDomain()

    # Set up the system
    system.mem_mode = 'timing'               # Use timing accesses
    system.mem_ranges = [AddrRange('512MB')] # Create an address range

    # Create a simple CPU
    system.cpu = TimingSimpleCPU()
    # system.cpu.wait_for_remote_gdb = True

    # Create an L1 instruction and data cache
    class CacheConfig():
        def __init__(self, l1_size, l2_size):
            self.l1i_size = self.l1d_size = str(l1_size) + "B"
            self.l2_size = str(l2_size) + "B"
    cache_config = CacheConfig(l1_cache_size, l2_cache_size)
    system.cpu.icache = L1ICache(cache_config)
    system.cpu.dcache = L1DCache(cache_config)
    system.cpu.dcache.replacement_policy = policy_obj
    system.cpu.icache.replacement_policy = policy_obj

    # Connect the instruction and data caches to the CPU
    system.cpu.icache.connectCPU(system.cpu)
    system.cpu.dcache.connectCPU(system.cpu)

    # Create a memory bus
    system.membus = SystemXBar()

    has_l2_cache = False
    if has_l2_cache:
        # Create a memory bus, a coherent crossbar, in this case
        system.l2bus = L2XBar()

        # Hook the CPU ports up to the l2bus
        system.cpu.icache.connectBus(system.l2bus)
        system.cpu.dcache.connectBus(system.l2bus)

        # Create an L2 cache and connect it to the l2bus
        system.l2cache = L2Cache(cache_config)
        system.l2cache.replacement_policy = policy_obj
        system.l2cache.connectCPUSideBus(system.l2bus)

        # Connect the L2 cache to the membus
        system.l2cache.connectMemSideBus(system.membus)
    else:
        # Connect the CPU ports to the membus
        system.cpu.icache.connectBus(system.membus)
        system.cpu.dcache.connectBus(system.membus)

    # create the interrupt controller for the CPU
    system.cpu.createInterruptController()

    # For x86 only, make sure the interrupts are connected to the memory
    # Note: these are directly connected to the memory bus and are not cached
    if m5.defines.buildEnv['TARGET_ISA'] == "x86":
        system.cpu.interrupts[0].pio = system.membus.master
        system.cpu.interrupts[0].int_master = system.membus.slave
        system.cpu.interrupts[0].int_slave = system.membus.master

    # Create a DDR3 memory controller
    if m5.defines.buildEnv['TARGET_ISA'].lower() == "alpha":
        # syntax for gem5 v19, required for using ALPHA
        print("Using old (gem5 v19) syntax for the memory controller, patch simulate.py if this is incorrect")
        system.mem_ctrl = DDR3_1600_8x8()
        system.mem_ctrl.range = system.mem_ranges[0]
        system.mem_ctrl.port = system.membus.master
    else:
        # syntax for the latest version of gem5 (v21)
        print("Using new (gem5 v21) syntax for the memory controller, patch simulate.py if this is incorrect")
        system.mem_ctrl = MemCtrl()
        system.mem_ctrl.dram = DDR3_1600_8x8()
        system.mem_ctrl.dram.range = system.mem_ranges[0]
        system.mem_ctrl.port = system.membus.master

    # Connect the system up to the membus
    system.system_port = system.membus.slave

    # Create a process for a simple "Hello World" application
    process = Process()
    # Set the command
    # cmd is a list which begins with the executable (like argv)
    process.cmd = [binary]
    # Set the cpu to use the process as its workload and create thread contexts
    system.cpu.workload = process
    system.cpu.createThreads()

    # set up the root SimObject and start the simulation
    root = Root(full_system = False, system = system)
    # instantiate all of the objects we've created above
    m5.instantiate()

    print("Beginning simulation!")
    exit_event = m5.simulate()
    print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))

if __name__ == '__m5_main__':
    print("You're probably looking for standalone.py.")