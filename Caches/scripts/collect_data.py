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

for key, val in params.items():
    cur_val = val["range"][0]
    while cur_val <= val["range"][1]:
        for benchmark in ['hmmer', 'sjeng']:
            stats_path = f'{OUTPUT_DIR}/{key}_{cur_val}{"_" if val["units"] else ""}{val["units"]}/{benchmark}/stats.txt'
            with open(stats_path, 'r', encoding='utf-8') as file:
                file_data = file.readlines()
                l1i_miss_rate = float(
                    file_data[345 if benchmark == 'hmmer' else 329].split()[1])
                l1d_miss_rate = float(
                    file_data[135 if benchmark == 'hmmer' else 135].split()[1])
                l2_miss_rate = float(
                    file_data[475 if benchmark == 'hmmer' else 457].split()[1])
                data.append(
                    [benchmark, key, f'{cur_val}{"_" if val["units"] else ""}{val["units"]}', l1i_miss_rate, l1d_miss_rate, l2_miss_rate])

            cur_val *= 2

df = pd.DataFrame(data, columns=['Benchmark', 'Parameter',
                  'Value', 'L1I Miss Rate', 'L1D Miss Rate', "L2 Miss Rate"])

df.to_excel(OUTPUT_FILE)
