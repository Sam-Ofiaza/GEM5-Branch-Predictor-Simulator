import subprocess
import sys
import multiprocessing as mp

GEM5_DIR = '../../../gem5'
LOGS_DIR = '../logs'

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

cur_params = {}
for key, val in params.items():
    cur_params[key] = val["default"]


def build_benchmark_args(Cpu_Type='TimingSimpleCPU', L1I_Size=params["L1I_Size"]["default"], L1D_Size=params["L1D_Size"]["default"], L2_Size=params["L2_Size"]["default"], Cacheline=params["Cacheline"]["default"], L1I_Assoc=params["L1I_Assoc"]["default"], L1D_Assoc=params["L1D_Assoc"]["default"], L2_Assoc=params["L2_Assoc"]["default"]):
    return f'-I 50000000 --cpu-type={Cpu_Type} --caches --l2cache --l1d_size={L1D_Size}kB --l1i_size={L1I_Size}kB --l2_size={L2_Size}MB --l1d_assoc={L1D_Assoc} --l1i_assoc={L1I_Assoc} --l2_assoc={L2_Assoc} --cacheline_size={Cacheline}'


# # Set the simulator branch predictor to NULL
with open(f'{GEM5_DIR}/src/cpu/simple/BaseSimpleCPU.py', 'r', encoding='utf-8') as file:
    data = file.readlines()

data[40] = '    branchPred = Param.BranchPredictor(NULL, "Branch Predictor")'

with open(f'{GEM5_DIR}/src/cpu/simple/BaseSimpleCPU.py', 'w', encoding='utf-8') as file:
    file.writelines(data)

# # Compile if necessary
subprocess.call(['./compile.sh', sys.argv[1],
                '&>>', f'{LOGS_DIR}/compile.log'])

# Run the benchmarks for each configuration in parallel
pool = mp.Pool()

for cpu_type in cpu_types:
    cur_params["Cpu_Type"] = cpu_type['param']

    pool.apply_async(subprocess.Popen, args=(
        ['./run_benchmarks.sh', f'{cpu_type["name"]}_No_Caches', f'-I 50000000 --cpu-type={cpu_type["name"]}', '&>>', f'{LOGS_DIR}/{cpu_type["name"]}_No_Caches.log'], ))

    for key, val in params.items():
        cur_val = val["range"][0]
        while cur_val <= val["range"][1]:
            cur_params[key] = cur_val
            output_dir_name = f'{cpu_type["name"]}_{key}_{cur_val}{"_" if val["units"] else ""}{val["units"]}'
            benchmark_args = build_benchmark_args(**cur_params)

            # print(f'{cur_params=}')
            # print(f'{output_dir_name=}')
            # print(f'{benchmark_args=}')

            pool.apply_async(subprocess.Popen, args=(
                ['./run_benchmarks.sh', output_dir_name, benchmark_args, '&>>', f'{LOGS_DIR}/{output_dir_name}.log'], ))

            cur_val *= 2
        cur_params[key] = params[key]["default"]

pool.close()
pool.join()
