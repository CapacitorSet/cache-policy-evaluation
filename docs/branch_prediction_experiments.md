# Branch prediction experiments

The `combination.py` script can also a run a matrix of simulations with varying branch prediction parameters, specifically:

 - `--btb-entries` for branch target prediction;
 - `--global-buffer` for the branch predictor buffer size.

Note that other parameters (return stack size, local buffer size) are hardcoded, but the script can be easily modified to add support for varying them if needed.

Refer to "Cache experiments" for information on how to use `combination.py`. Note that for branch prediction experiments you might be interested not only in the cycle count but also in the branch misprediction count or the BTB hit count:

```
root@4a3c2463127c:/gem5# grep 'system.cpu.BranchMispred' m5out/stats.txt
system.cpu.BranchMispred                     33106417                       # Number of branch mispredictions
root@4a3c2463127c:/gem5# grep 'system.cpu.branchPred.BTBHitPct' m5out/stats.txt
system.cpu.branchPred.BTBHitPct              0.000175                       # BTB Hit Percentage
```

Note that support for predictors other than `"local"` is limited; it is relatively simple to add support for other predictors, or hardcode a different predictor with fixed parameters. Advanced gem5 users may also implement and test custom branch predictors.