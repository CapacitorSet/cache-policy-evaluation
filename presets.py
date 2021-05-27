from entry import Entry

# Endo, F. A., Courousse, D., & Charles, H.-P. (2014). Micro-architectural simulation of in-order and out-of-order ARM microprocessors with gem5. 2014 International Conference on Embedded Computer Systems: Architectures, Modeling, and Simulation (SAMOS XIV)
# doi:10.1109/SAMOS.2014.6893220
# The paper also outlines how to simulate the branch prediction logic: use a tournament BP with a tiny local predictor
cortex_a8 = Entry(speed="600MHz", policy="random", l1_size=2**15, l2_size=2**18, predictor="tournament", btb_entries=512, global_buffer=512, local_buffer=1, ras_size=8)
cortex_a9 = Entry(speed="1GHz", policy="random", l1_size=2**15, l2_size=2**19, predictor="tournament", btb_entries=4096, global_buffer=4096, local_buffer=1, ras_size=8)

# https://www.st.com/en/microcontrollers-microprocessors/stm32mp1-series.html
# Based on ARM Cortex A7
# https://developer.arm.com/documentation/ddi0464/f/L1-Memory-System/L1-instruction-memory-system: BTAC ~= BTB
stm32mp1 = Entry(speed="650MHz", policy="random", l1_size=2**15, l2_size=2**18, predictor="tournament", btb_entries=8, global_buffer=256, local_buffer=1, ras_size=8)

# https://www.st.com/en/microcontrollers-microprocessors/stm32h725re.html
# ARM Cortex M7 + 32 KB L1 I-cache + 32 KB D-cache
# The Cortex M7 may include a BTAC (https://developer.arm.com/documentation/ddi0489/f/introduction/component-blocks/prefetch-unit)
# but ST gives no information about it; assume it is not present (set the values to the smallest values available).
stm32h7 = Entry(speed="550MHz", policy="random", l1_size=2**15, l2_size=0, predictor="tournament", btb_entries=1, global_buffer=1, local_buffer=1, ras_size=1)
