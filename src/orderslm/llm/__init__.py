"""Provider clients for API models (teacher candidates; later the M4 generator/labeler).

Layering, outermost first: CachedClient (record/replay) → Throttle → provider client. Replays
never wait on the throttle and never touch the network.
"""
