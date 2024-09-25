import time
import simpy

def example(env):
    start = time.perf_counter()
    yield env.timeout(1)
    end = time.perf_counter()
    print('Duration of one simulation time unit: %.2fs' % (end - start))

env = simpy.Environment()
proc = env.process(example(env))
env.run(until=proc)
#Duration of one simulation time unit: 0.00s

import simpy.rt
env = simpy.rt.RealtimeEnvironment(initial_time=0,factor=100)
proc = env.process(example(env))
env.run(until=proc)
#Duration of one simulation time unit: 0.10s
