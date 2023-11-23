import subprocess
import sys
import multiprocessing as mp
import math
import copy

GEM5_DIR = '../../../gem5'
LOGS_DIR = '../logs'

params = {
    "L1I_Size": {
        "units": "KB",
        "range": (1, 128)
    },
    "L1D_Size": {
        "units": "KB",
        "range": (1, 128)
    },
    "L2_Size": {
        "units": "MB",
        "range": (1, 128)
    },
    "Cacheline": {
        "units": "bytes",
        "range": (1, 128)
    },
    "L1I_Assoc": {
        "units": "",
        "range": (1, 8)
    },
    "L1D_Assoc": {
        "units": "",
        "range": (1, 18)
    },
    "L2_Assoc": {
        "units": "",
        "range": (1, 8)
    },
}

# Create the baseline parameters by calculating the roughly median value from each parameter's range
# e.g., L1I_Size's range = 1, 2, 4, 8, 16, 32, 64, 128 -> baseline parameter = 8
baseline_params = {}
for key, val in params.items():
    baseline_params[key] = 2 ** ((math.log2(val["range"][1]) -
                                 math.log2(val["range"][0])) // 2)

cur_params = copy.deepcopy(baseline_params)


def build_benchmark_args(L1I_Size=baseline_params["L1I_Size"], L1D_Size=baseline_params["L1D_Size"], L2_Size=baseline_params["L2_Size"], Cacheline=baseline_params["Cacheline"], L1I_Assoc=baseline_params["L1I_Assoc"], L1D_Assoc=baseline_params["L1D_Assoc"], L2_Assoc=baseline_params["L2_Assoc"]):
    return f'-I 50000000 --cpu-type=TimingSimpleCPU --caches --l2cache --l1d_size={L1D_Size}kB --l1i_size={L1I_Size}kB --l2_size={L2_Size}MB --l1d_assoc={L1D_Assoc} --l1i_assoc={L1I_Assoc} --l2_assoc={L2_Assoc} --cacheline_size={Cacheline}'


# # Set the simulator branch predictor to NULL
# with open(f'{GEM5_DIR}/src/cpu/pred/BranchPredictor.py', 'r', encoding='utf-8') as file:
#     data = file.readlines()

# data[40] = '    branchPred = Param.BranchPredictor(NULL, "Branch Predictor")'

# with open(f'{GEM5_DIR}/src/cpu/pred/BranchPredictor.py', 'w', encoding='utf-8') as file:
#     file.writelines(data)

# # Compile if necessary
# subprocess.call(['./compile.sh', sys.argv[1],
#                 '&>>', f'{LOGS_DIR}/compile.log'])

# Run the benchmarks for each configuration in parallel
pool = mp.Pool()

for key, val in params.items():
    cur_val = val["range"][0]
    while cur_val <= val["range"][1]:
        cur_params[key] = cur_val
        output_dir_name = f'{key}_{cur_val}_{val["units"]}'
        benchmark_args = build_benchmark_args(**cur_params)
        # pool.apply_async(subprocess.Popen, args=(
        #     ['./run_benchmarks.sh', output_dir_name, benchmark_args, '&>>', f'{LOGS_DIR}/{output_dir_name}.log'], ))
        print(f'{cur_params=}, {output_dir_name=}, {benchmark_args=}')
        cur_val *= 2
    cur_params[key] = baseline_params[key]

pool.close()
pool.join()
