# Simulating existing CPUs

When running standalone simulations you might be interested in comparing different CPUs rather than specifying parameters by hand. This project contains a few representative examples of embedded ARM CPUs, from the most powerful to the least powerful:

 - `cortex-a9`, a Cortex-A9 processor;
 - `cortex-a8`, a Cortex-A8 processor;
 - [`stm32mp1`](https://www.st.com/en/microcontrollers-microprocessors/stm32mp1-series.html), a commercial microprocessor based on the Cortex-A7;
 - [`stm32h7`](https://www.st.com/en/microcontrollers-microprocessors/stm32h725re.html), a commercial microprocessor based on the Cortex-M7.

Note that the models are not super accurate; only the clock speed, the cache replacement policy, the cache sizes and the branch prediction units are specified.

To use a CPU preset just pass eg. `--preset stm32h7` to `standalone.py`.