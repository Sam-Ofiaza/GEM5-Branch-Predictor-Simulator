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
    {'param': 'TimingSimpleCPU', 'name': 'Timing'},
    {'param': 'AtomicSimpleCPU', 'name': 'Atomic'},
]

cost_config = {
    'Cpu_Type': {'Timing': 1.5, 'Atomic': 1},
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
        'cost': lambda x: 2 ** (math.log2(x) - 3),
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

cost_info = []

for cur_param, info in cost_config.items():
    data = []
    if cur_param == 'Cpu_Type':
        for name, weight in cost_config[cur_param].items():
            data.append([name, weight])
        df = pd.DataFrame(data, columns=['CPU Type', 'Weight'])
        df.name = 'CPU Type Weights'
        cost_info.append(df)
    else:
        range = params[cur_param]['range']
        cur_val, end = range
        while cur_val <= end:
            cur_cost = cost_config[cur_param]['cost'](cur_val)
            weighted_cur_cost = cur_cost * cost_config[cur_param]['weight']
            data.append(
                [f'{cur_val}{" " if params[cur_param]["units"] else ""}{params[cur_param]["units"]}', cur_cost, weighted_cur_cost])
            cur_val *= 2
        df = pd.DataFrame(data, columns=['Value', 'Cost', 'Weighted Cost'])
        df.name = f'{cur_param} Costs'
        cost_info.append(df)

startrow = 0
with pd.ExcelWriter('../output/cost_info.xlsx') as writer:
    for df in cost_info:
        pd.Series(df.name).to_excel(writer, startrow=startrow,
                                    startcol=0, index=False, header=False)
        startrow += 1
        if df.name != 'CPU Type Weights':
            df.set_index('Value', inplace=True)
            df = df.transpose()
            df.to_excel(writer, engine='xlsxwriter',
                        startrow=startrow,)
        else:
            df.to_excel(writer, engine='xlsxwriter',
                        startrow=startrow, index=False)
        startrow += (df.shape[0] + 2)

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
                cost *= cost_config['Cpu_Type'][cpu_type['name']]

                stats_path = f'{OUTPUT_DIR}/{cpu_type["name"]}_{key}_{cur_val}{"_" if val["units"] else ""}{val["units"]}/{benchmark}/stats.txt'
                with open(stats_path, 'r', encoding='utf-8') as file:
                    direct_cpi, l1i_miss_rate, l1d_miss_rate, l2_miss_rate = -1, -1, -1, -1
                    l1i_miss_ticks, l1d_miss_ticks, l2_miss_ticks = -1, -1, -1
                    l1i_misses, l1d_misses, l2_misses = -1, -1, -1

                    for idx, line in enumerate(file):
                        if 'system.cpu.dcache.overallMissLatency::total' in line:
                            l1d_miss_ticks = float(line.split()[1])
                        elif 'system.cpu.icache.overallMissLatency::total' in line:
                            l1i_miss_ticks = float(line.split()[1])
                        elif 'system.l2.overallMissLatency::total' in line:
                            l2_miss_ticks = float(line.split()[1])
                        elif 'system.cpu.cpi' in line:
                            direct_cpi = float(line.split()[1])
                        elif 'system.cpu.dcache.overallMisses::total' in line:
                            l1d_misses = float(line.split()[1])
                        elif 'system.cpu.icache.overallMisses::total' in line:
                            l1i_misses = float(line.split()[1])
                        elif 'system.l2.overallMisses::total' in line:
                            l2_misses = float(line.split()[1])
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
                    misses_cpi = 1 + \
                        ((l1i_misses + l1d_misses + l2_misses) / 50000000)
                    miss_penalty_cpi = 1 + \
                        ((l1i_misses + l1d_misses) *
                         6 + l2_misses * 50) / 50000000

                    data.append(
                        [benchmark, cpu_type['name'], f'{key}_{cur_val}{"_" if val["units"] else ""}{val["units"]}', miss_penalty_cpi, cost, cost / miss_penalty_cpi])
                cur_val *= 2

df = pd.DataFrame(data, columns=[
                  'Benchmark', 'CPU Type', 'Parameter', 'CPI using Miss Penalties', 'Cost', 'Cost / CPI'])

df.to_excel(f'{OUTPUT_DIR}/{OUTPUT_FILE}')
