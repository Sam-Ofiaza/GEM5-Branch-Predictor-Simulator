from functools import partial
import subprocess
import os
import sys
import multiprocessing as mp

GEM5_DIR = './gem5'
BP_TYPE_PATH = f'{GEM5_DIR}/src/cpu/simple/BaseSimpleCPU.py'
BP_PARAMS_PATH = f'{GEM5_DIR}/src/cpu/pred/BranchPredictor.py'
LOGS_DIR = './logs'

OUTPUT_DIR_NAME_MAP = {1024: '1k', 2048: '2k', 4096: '4k', 8192: '8k'}

# All BPs
BTB_ENTRIES = [2048, 4096]

# Local BP
LOCAL_PRED_SIZES = [1024, 2048]

# BiMode BP
BIMODE_GLOBAL_PRED_SIZES = [2048, 4096, 8192]
BIMODE_CHOICE_PREDICTOR_SIZES = [2048, 4096, 8192]

# Tournament BP
TOURNY_LOCAL_PRED_SIZES = [1024, 2048]
TOURNY_GLOBAL_PRED_SIZES = [4096, 8192]
TOURNEY_CHOICE_PRED_SIZES = [4096, 8192]

BP_TYPES = {
    40: lambda x: f'    branchPred = Param.BranchPredictor({x}, "Branch Predictor")'
}

BP_PARAMS = {
    65: lambda x: f'    BTBEntries = Param.Unsigned({x}, "Number of BTB entries")\n',
    81: lambda x: f'    localPredictorSize = Param.Unsigned({x}, "Size of local predictor")\n',
    104: lambda x: f'    globalPredictorSize = Param.Unsigned({x}, "Size of global predictor")\n',
    106: lambda x: f'    choicePredictorSize = Param.Unsigned({x}, "Size of choice predictor")\n',
    90: lambda x: f'    localPredictorSize = Param.Unsigned({x}, "Size of local predictor")\n',
    93: lambda x: f'    globalPredictorSize = Param.Unsigned({x}, "Size of global predictor")\n',
    95: lambda x: f'    choicePredictorSize = Param.Unsigned({x}, "Size of choice predictor")\n',
}


def modify_file(filepath, callback):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.readlines()

    callback(data)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(data)


def change_bp_type(data, name=None):
    data[40] = BP_TYPES[40](name)
    print(name, end=' ')


def change_local_bp_config(data, btb_entries=None, local_pred_size=None):
    data[65] = BP_PARAMS[65](btb_entries)
    data[81] = BP_PARAMS[81](local_pred_size)
    print(f'{btb_entries=} {local_pred_size=}')


def change_bimode_bp_config(data, btb_entries=None, global_pred_size=None, choice_pred_size=None):
    data[65] = BP_PARAMS[65](btb_entries)
    data[104] = BP_PARAMS[104](global_pred_size)
    data[106] = BP_PARAMS[106](choice_pred_size)
    print(f'{btb_entries=} {global_pred_size=} {choice_pred_size=}')


def change_tourny_bp_config(data, btb_entries=None, local_pred_size=None, global_pred_size=None, choice_pred_size=None):
    data[65] = BP_PARAMS[65](btb_entries)
    data[90] = BP_PARAMS[90](local_pred_size)
    data[93] = BP_PARAMS[93](global_pred_size)
    data[95] = BP_PARAMS[95](choice_pred_size)
    print(f'{btb_entries=} {local_pred_size=} {global_pred_size=} {choice_pred_size=}')


def test():
    modify_file(BP_TYPE_PATH, partial(
        change_bp_type, name='LocalBP()'))
    modify_file(BP_PARAMS_PATH, partial(
        change_local_bp_config, btb_entries=2048, local_pred_size=1024))
    output_dir_name = f'Local_{OUTPUT_DIR_NAME_MAP[2048]}_BTB_Entries_{OUTPUT_DIR_NAME_MAP[1024]}_Pred_Size'
    subprocess.Popen(['./script.sh', output_dir_name,
                      '&>>', f'{LOGS_DIR}/{output_dir_name}.log'])


def main():
    pool = mp.Pool()

    for x in BTB_ENTRIES:
        for y in LOCAL_PRED_SIZES:
            modify_file(BP_TYPE_PATH, partial(
                change_bp_type, name='LocalBP()'))
            modify_file(BP_PARAMS_PATH, partial(
                change_local_bp_config, btb_entries=x, local_pred_size=y))
            output_dir_name = f'Local_{OUTPUT_DIR_NAME_MAP[x]}_BTB_Entries_{OUTPUT_DIR_NAME_MAP[y]}_Pred_Size'
            # subprocess.Popen(['./script.sh', output_dir_name, '&>>', f'{LOGS_DIR}/{output_dir_name}.log'])
            pool.apply_async(subprocess.Popen, args=(
                ['./script.sh', output_dir_name, '&>>', f'{LOGS_DIR}/{output_dir_name}.log'], ))

        for y in BIMODE_GLOBAL_PRED_SIZES:
            for z in BIMODE_CHOICE_PREDICTOR_SIZES:
                modify_file(BP_TYPE_PATH, partial(
                    change_bp_type, name='BiModeBP()'))
                modify_file(BP_PARAMS_PATH, partial(
                    change_bimode_bp_config, btb_entries=x, global_pred_size=y, choice_pred_size=z))
                output_dir_name = f'BiMode_{OUTPUT_DIR_NAME_MAP[x]}_BTB_Entries_{OUTPUT_DIR_NAME_MAP[y]}_Global_Pred_Size_{OUTPUT_DIR_NAME_MAP[z]}_Choice_Pred_Size'
                # subprocess.Popen(['./script.sh', output_dir_name, '&>>', f'{LOGS_DIR}/{output_dir_name}.log'])
                pool.apply_async(subprocess.Popen, args=(
                    ['./script.sh', output_dir_name, '&>>', f'{LOGS_DIR}/{output_dir_name}.log'], ))

        for y in TOURNY_LOCAL_PRED_SIZES:
            for z in TOURNY_GLOBAL_PRED_SIZES:
                for k in TOURNEY_CHOICE_PRED_SIZES:
                    modify_file(BP_TYPE_PATH, partial(
                        change_bp_type, name='TournamentBP()'))
                    modify_file(BP_PARAMS_PATH, partial(
                        change_tourny_bp_config, btb_entries=x, local_pred_size=y, global_pred_size=z, choice_pred_size=k))
                    output_dir_name = f'Tournament_{OUTPUT_DIR_NAME_MAP[x]}_BTB_Entries_{OUTPUT_DIR_NAME_MAP[y]}_Local_Pred_Size_{OUTPUT_DIR_NAME_MAP[z]}_Global_Pred_Size_{OUTPUT_DIR_NAME_MAP[k]}_Choice_Pred_Size'
                    # subprocess.Popen(['./script.sh', output_dir_name, '&>>', f'{LOGS_DIR}/{output_dir_name}.log'])
                    pool.apply_async(subprocess.Popen, args=(
                        ['./script.sh', output_dir_name, '&>>', f'{LOGS_DIR}/{output_dir_name}.log'], ))

    pool.close()
    pool.join()


if len(sys.argv) > 1:
    test()  # Enter any arguments to run a single test for Local_2k_BTB_Entries_1k_Pred_Size
else:
    main()  # Enter no arguments to run all tests
