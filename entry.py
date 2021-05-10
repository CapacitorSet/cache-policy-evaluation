from collections import namedtuple

keys = (
    "policy", # cache replacement policy
    "l1_size", "l2_size",
    "predictor", # branch predictor
    "btb_entries",
    "ras_size", # Return Address Stack
    "global_buffer", # Global History Buffer on ARM
    "local_buffer" # local predictor size in TournamentBP
)
Entry = namedtuple("Entry", keys)