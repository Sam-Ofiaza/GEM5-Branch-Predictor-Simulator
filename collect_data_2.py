import pandas as pd

REVERSE_OUTPUT_DIR_NAME_MAP = {'1k': 1024, '2k': 2048, '4k': 4096, '8k': 8192}

# All BPs
BTB_ENTRIES = ['2k', '4k']

# Local BP
LOCAL_PRED_SIZES = ['1k', '2k']

# BiMode BP
BIMODE_GLOBAL_PRED_SIZES = ['2k', '4k', '8k']
BIMODE_CHOICE_PREDICTOR_SIZES = ['2k', '4k', '8k']

# Tournament BP
TOURNY_LOCAL_PRED_SIZES = ['1k', '2k']
TOURNY_GLOBAL_PRED_SIZES = ['4k', '8k']
TOURNEY_CHOICE_PRED_SIZES = ['4k', '8k']


def get_stats(benchmark, stats_path):
    # print(stats_path)
    with open(stats_path, 'r', encoding='utf-8') as file:
        file_data = file.readlines()
        btb_miss_pct = float(file_data[26].split()[1]) - 99
        num_pred_branches = float(
            file_data[288 if benchmark == 'hmmer' else 271].split()[1])
        num_mispred_branches = float(
            file_data[289 if benchmark == 'hmmer' else 272].split()[1])
        branch_mispred_pct = num_mispred_branches / \
            (num_pred_branches + num_mispred_branches)
        return (btb_miss_pct, branch_mispred_pct)


def get_local_data(data, benchmark, x):
    for y in LOCAL_PRED_SIZES:
        stats_path = f'./output/Local_{x}_BTB_{y}_Pred/{benchmark}/stats.txt'
        stats_data = get_stats(benchmark, stats_path)
        config_name = f'Local_{x}_BTB_Entries_{y}_BP_Size'
        data.append([benchmark, config_name, stats_data[0], stats_data[1]])


def get_bimode_data(data, benchmark, x):
    for y in BIMODE_GLOBAL_PRED_SIZES:
        for z in BIMODE_CHOICE_PREDICTOR_SIZES:
            stats_path = f'./output/BiMode_{x}_BTB_{y}_Global_{z}_Choice/{benchmark}/stats.txt'
            stats_data = get_stats(benchmark, stats_path)
            config_name = f'BiMode_{x}_BTB_Entries_{y}_Global_BP_Size_{z}_Choice_BP_Size'
            data.append([benchmark, config_name, stats_data[0], stats_data[1]])


def get_tournament_data(data, benchmark, x):
    for y in TOURNY_LOCAL_PRED_SIZES:
        for z in TOURNY_GLOBAL_PRED_SIZES:
            for k in TOURNEY_CHOICE_PRED_SIZES:
                stats_path = f'./output/Tournament_{x}_BTB_{y}_Local_{z}_Global_{z}_Choice/{benchmark}/stats.txt'
                stats_data = get_stats(benchmark, stats_path)
                config_name = f'Tournament_{x}_BTB_Entries_{y}_Local_BP_Size_{z}_Global_BP_Size_{z}_Choice_BP_Size'
                data.append([benchmark, config_name,
                            stats_data[0], stats_data[1]])


data = []

for benchmark in ['hmmer', 'sjeng']:
    for bp_type in ['Local', 'BiMode', 'Tournament']:
        for x in BTB_ENTRIES:
            match bp_type:
                case 'Local':
                    get_local_data(data, benchmark, x)
                case 'BiMode':
                    get_bimode_data(data, benchmark, x)
                case 'Tournament':
                    get_tournament_data(data, benchmark, x)

df = pd.DataFrame(data, columns=[
                  'Benchmark', 'Configuration', 'BTB Miss %', 'Branch Misprediction %'])

df.to_excel('output2.xlsx')
