import pandas as pd

OUTPUT_DIR = '../output'
OUTPUT_FILE = 'data.xlsx'

params = {
    "L1I_Size": {
        "units": "KB",
        "range": (1, 128),
        "default": 8
    },
    "L1D_Size": {
        "units": "KB",
        "range": (1, 128),
        "default": 8
    },
    "L2_Size": {
        "units": "MB",
        "range": (1, 128),
        "default": 8
    },
    "Cacheline": {
        "units": "bytes",
        "range": (8, 512),
        "default": 64
    },
    "L1I_Assoc": {
        "units": "",
        "range": (1, 8),
        "default": 2
    },
    "L1D_Assoc": {
        "units": "",
        "range": (1, 8),
        "default": 2
    },
    "L2_Assoc": {
        "units": "",
        "range": (1, 8),
        "default": 2
    },
}

data = []

for benchmark in ['hmmer', 'sjeng']:
    for key, val in params.items():
        cur_val = val["range"][0]
        while cur_val <= val["range"][1]:
            stats_path = f'{OUTPUT_DIR}/{key}_{cur_val}{"_" if val["units"] else ""}{val["units"]}/{benchmark}/stats.txt'
            with open(stats_path, 'r', encoding='utf-8') as file:
                l1i_miss_rate, l1d_miss_rate, l2_miss_rate, = -1, -1, -1

                for idx, line in enumerate(file):
                    if 'system.cpu.dcache.overallMissRate::total' in line:
                        l1d_miss_rate = float(line.split()[1])
                    elif 'system.cpu.icache.overallMissRate::total' in line:
                        l1i_miss_rate = float(line.split()[1])
                    elif 'system.l2.overallMissRate::total' in line:
                        l2_miss_rate = float(line.split()[1])
                        break

                data.append(
                    [benchmark, f'{key}_{cur_val}{"_" if val["units"] else ""}{val["units"]}', l1i_miss_rate, l1d_miss_rate, l2_miss_rate])
            cur_val *= 2

df = pd.DataFrame(data, columns=[
                  'Benchmark', 'Parameter', 'L1I Miss Rate', 'L1D Miss Rate', "L2 Miss Rate"])

df.to_excel(f'{OUTPUT_DIR}/{OUTPUT_FILE}')
