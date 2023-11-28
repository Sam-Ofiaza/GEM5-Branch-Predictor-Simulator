import pandas as pd
import math

OUTPUT_DIR = '../output'
OUTPUT_FILE = 'data.xlsx'

params = {
    "L1I_Size": {
        "units": "KB",
        "range": (1, 128),
        "default": 1
    },
    "L1D_Size": {
        "units": "KB",
        "range": (1, 128),
        "default": 1
    },
    "L2_Size": {
        "units": "MB",
        "range": (1, 128),
        "default": 1
    },
    "Cacheline": {
        "units": "bytes",
        "range": (8, 512),
        "default": 8
    },
    "L1I_Assoc": {
        "units": "",
        "range": (1, 8),
        "default": 1
    },
    "L1D_Assoc": {
        "units": "",
        "range": (1, 8),
        "default": 1
    },
    "L2_Assoc": {
        "units": "",
        "range": (1, 8),
        "default": 1
    },
}

cpu_types = [
    {'param': 'BaseSimpleCPU', 'name': 'Base'},
    {'param': 'TimingSimpleCPU', 'name': 'Timing'},
    {'param': 'AtomicSimpleCPU', 'name': 'Atomic'},
]

cost_config = {
    'cpu_type': {'Base': 1, 'Timing': 1.5, 'Atomic': 1.5},
    "L1I_Size": {
        'cost': lambda x: x,
        'weight': 3,
    },
    "L1D_Size": {
        'cost': lambda x: x,
        'weight': 3,
    },
    "L2_Size": {
        'cost': lambda x: x,
        'weight': 1,
    },
    "Cacheline": {
        'cost': lambda x: math.log2(x) - 2,
        'weight': 2,
    },
    "L1I_Assoc": {
        'cost': lambda x: x,
        'weight': 2.5,
    },
    "L1D_Assoc": {
        'cost': lambda x: x,
        'weight': 2.5,
    },
    "L2_Assoc": {
        'cost': lambda x: x,
        'weight': 1.5,
    },
}

data = []

for benchmark in ['hmmer', 'sjeng']:
    for cpu_type in cpu_types:
        for key, val in params.items():
            cur_val = val["range"][0]
            while cur_val <= val["range"][1]:
                cost = 0
                for key2, val2 in params.items():
                    cost += cost_config[key2]['cost'](
                        cur_val if key == key2 else params[key2]['default']) * cost_config[key2]['weight']
                cost *= cost_config['cpu_type'][cpu_type['name']]

                stats_path = f'{OUTPUT_DIR}/{cpu_type["name"]}_{key}_{cur_val}{"_" if val["units"] else ""}{val["units"]}/{benchmark}/stats.txt'
                with open(stats_path, 'r', encoding='utf-8') as file:
                    direct_cpi, l1i_miss_rate, l1d_miss_rate, l2_miss_rate = -1, -1, -1, -1
                    l1i_miss_ticks, l1d_miss_ticks, l2_miss_ticks = -1, -1, -1

                    for idx, line in enumerate(file):
                        if 'system.cpu.dcache.overallMissLatency::total' in line:
                            l1d_miss_ticks = float(line.split()[1])
                        elif 'system.cpu.icache.overallMissLatency::total' in line:
                            l1i_miss_ticks = float(line.split()[1])
                        elif 'system.l2.overallMissLatency::total' in line:
                            l2_miss_ticks = float(line.split()[1])
                        elif 'system.cpu.cpi' in line:
                            direct_cpi = float(line.split()[1])
                        elif 'system.cpu.dcache.overallMissRate::total' in line:
                            l1d_miss_rate = float(line.split()[1])
                        elif 'system.cpu.icache.overallMissRate::total' in line:
                            l1i_miss_rate = float(line.split()[1])
                        elif 'system.l2.overallMissRate::total' in line:
                            l2_miss_rate = float(line.split()[1])
                            break

                    miss_rate_cpi = 1 + l1i_miss_rate + l1d_miss_rate + l2_miss_rate
                    miss_ticks_cpi = 1 + \
                        (((l1i_miss_ticks / 1000) + (l1d_miss_ticks / 1000) +
                          (l2_miss_ticks / 1000)) / 50000000)

                    data.append(
                        [benchmark, f'{key}_{cur_val}{"_" if val["units"] else ""}{val["units"]}', direct_cpi, miss_rate_cpi, miss_ticks_cpi, cost])
                cur_val *= 2

df = pd.DataFrame(data, columns=[
                  'Benchmark', 'Parameter', "Direct CPI", "CPI using Miss Rate", "CPI using Miss Ticks", "Cost"])

df.to_excel(f'{OUTPUT_DIR}/{OUTPUT_FILE}')
