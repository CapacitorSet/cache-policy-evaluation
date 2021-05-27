from collections import namedtuple

keys = (
    "speed", # clock speed
    "policy", # cache replacement policy
    "l1_size", "l2_size",
    "predictor", # branch predictor
    "btb_entries",
    "global_buffer", # Global History Buffer on ARM
    "local_buffer", # local predictor size in TournamentBP
    "ras_size", # Return Address Stack
)
Entry = namedtuple("Entry", keys)