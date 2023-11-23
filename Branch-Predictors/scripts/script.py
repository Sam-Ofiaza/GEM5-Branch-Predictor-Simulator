from functools import partial
import subprocess
import sys
import multiprocessing as mp

GEM5_DIR = '../../../gem5'
BP_TYPE_PATH = f'{GEM5_DIR}/src/cpu/simple/BaseSimpleCPU.py'
BP_PARAMS_PATH = f'{GEM5_DIR}/src/cpu/pred/BranchPredictor.py'
LOGS_DIR = '../logs'

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
    '''Locates file with filepath and executes a callback function on it'''
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.readlines()

    callback(data)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(data)


def change_bp_type(data, name=None):
    '''Used as a callback to a modify_file call'''
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


def run_script_serial(output_dir_name):
    '''Compiles one GEM5 configuration, test with the benchmarks, and moves the output to a ../output-serial/output_dir_name folder'''
    subprocess.call(['./serial_helper.sh', output_dir_name, sys.argv[2], '&>>',
                    f'{LOGS_DIR}/{output_dir_name}.log'])


def run_scripts_parallel(pool, output_dir_name):
    '''Two helper scripts are needed: the first ensures that modifying the GEM5 source dode and copying the GEM5 source code into a separate folder happen separately, the second is run asynchronously in a pool of threads managed by Python'''
    # Runs a script to copy the GEM5 source code to a ../builds/output_dir_name folder
    subprocess.call(['./parallel_helper_1.sh', output_dir_name, '&>>',
                    f'{LOGS_DIR}/{output_dir_name}.1.log'])
    # Runs a script to compile the copied code, test with the benchmarks, and move the output to a ../output-parallel/output_dir_name folder
    pool.apply_async(subprocess.Popen, args=(
        ['./parallel_helper_2.sh', output_dir_name, '&>>', f'{LOGS_DIR}/{output_dir_name}.2.log'], ))


def test_serial():
    '''Test a single configuration using serial execution'''
    modify_file(BP_TYPE_PATH, partial(
        change_bp_type, name='LocalBP()'))
    modify_file(BP_PARAMS_PATH, partial(
        change_local_bp_config, btb_entries=2048, local_pred_size=1024))
    output_dir_name = f'Local_{OUTPUT_DIR_NAME_MAP[2048]}_BTB_Entries_{OUTPUT_DIR_NAME_MAP[1024]}_Pred'
    run_script_serial(output_dir_name)


def test_parallel():
    '''Test a single configuration using parallel execution'''
    pool = mp.Pool()

    modify_file(BP_TYPE_PATH, partial(
        change_bp_type, name='LocalBP()'))
    modify_file(BP_PARAMS_PATH, partial(
        change_local_bp_config, btb_entries=2048, local_pred_size=1024))
    output_dir_name = f'Local_{OUTPUT_DIR_NAME_MAP[2048]}_BTB_Entries_{OUTPUT_DIR_NAME_MAP[1024]}_Pred'
    run_scripts_parallel(pool, output_dir_name)

    pool.close()
    pool.join()


def main_serial():
    for x in BTB_ENTRIES:
        for y in LOCAL_PRED_SIZES:
            modify_file(BP_TYPE_PATH, partial(
                change_bp_type, name='LocalBP()'))
            modify_file(BP_PARAMS_PATH, partial(
                change_local_bp_config, btb_entries=x, local_pred_size=y))
            output_dir_name = f'Local_{OUTPUT_DIR_NAME_MAP[x]}_BTB_{OUTPUT_DIR_NAME_MAP[y]}_Pred'
            run_script_serial(output_dir_name)

        for y in BIMODE_GLOBAL_PRED_SIZES:
            for z in BIMODE_CHOICE_PREDICTOR_SIZES:
                modify_file(BP_TYPE_PATH, partial(
                    change_bp_type, name='BiModeBP()'))
                modify_file(BP_PARAMS_PATH, partial(
                    change_bimode_bp_config, btb_entries=x, global_pred_size=y, choice_pred_size=z))
                output_dir_name = f'BiMode_{OUTPUT_DIR_NAME_MAP[x]}_BTB_{OUTPUT_DIR_NAME_MAP[y]}_Global_{OUTPUT_DIR_NAME_MAP[z]}_Choice'
                run_script_serial(output_dir_name)

        for y in TOURNY_LOCAL_PRED_SIZES:
            for z in TOURNY_GLOBAL_PRED_SIZES:
                for k in TOURNEY_CHOICE_PRED_SIZES:
                    modify_file(BP_TYPE_PATH, partial(
                        change_bp_type, name='TournamentBP()'))
                    modify_file(BP_PARAMS_PATH, partial(
                        change_tourny_bp_config, btb_entries=x, local_pred_size=y, global_pred_size=z, choice_pred_size=k))
                    output_dir_name = f'Tournament_{OUTPUT_DIR_NAME_MAP[x]}_BTB_{OUTPUT_DIR_NAME_MAP[y]}_Local_{OUTPUT_DIR_NAME_MAP[z]}_Global_{OUTPUT_DIR_NAME_MAP[k]}_Choice'
                    run_script_serial(output_dir_name)


def main_parallel():
    pool = mp.Pool()

    for x in BTB_ENTRIES:
        for y in LOCAL_PRED_SIZES:
            modify_file(BP_TYPE_PATH, partial(
                change_bp_type, name='LocalBP()'))
            modify_file(BP_PARAMS_PATH, partial(
                change_local_bp_config, btb_entries=x, local_pred_size=y))
            output_dir_name = f'Local_{OUTPUT_DIR_NAME_MAP[x]}_BTB_{OUTPUT_DIR_NAME_MAP[y]}_Pred'
            run_scripts_parallel(pool, output_dir_name)

        for y in BIMODE_GLOBAL_PRED_SIZES:
            for z in BIMODE_CHOICE_PREDICTOR_SIZES:
                modify_file(BP_TYPE_PATH, partial(
                    change_bp_type, name='BiModeBP()'))
                modify_file(BP_PARAMS_PATH, partial(
                    change_bimode_bp_config, btb_entries=x, global_pred_size=y, choice_pred_size=z))
                output_dir_name = f'BiMode_{OUTPUT_DIR_NAME_MAP[x]}_BTB_{OUTPUT_DIR_NAME_MAP[y]}_Global_{OUTPUT_DIR_NAME_MAP[z]}_Choice'
                run_scripts_parallel(pool, output_dir_name)

        for y in TOURNY_LOCAL_PRED_SIZES:
            for z in TOURNY_GLOBAL_PRED_SIZES:
                for k in TOURNEY_CHOICE_PRED_SIZES:
                    modify_file(BP_TYPE_PATH, partial(
                        change_bp_type, name='TournamentBP()'))
                    modify_file(BP_PARAMS_PATH, partial(
                        change_tourny_bp_config, btb_entries=x, local_pred_size=y, global_pred_size=z, choice_pred_size=k))
                    output_dir_name = f'Tournament_{OUTPUT_DIR_NAME_MAP[x]}_BTB_{OUTPUT_DIR_NAME_MAP[y]}_Local_{OUTPUT_DIR_NAME_MAP[z]}_Global_{OUTPUT_DIR_NAME_MAP[k]}_Choice'
                    run_scripts_parallel(pool, output_dir_name)

    pool.close()
    pool.join()


match(sys.argv[1]):
    case 'test-serial':
        if len(sys.argv) < 3 or not str.isnumeric(sys.argv[2]):
            sys.exit(
                'Please enter the number of cores to use as a second argument.')
        test_serial()
    case 'test-parallel':
        test_parallel()
    case 'main-serial':
        if len(sys.argv) < 3 or not str.isnumeric(sys.argv[2]):
            sys.exit(
                'Please enter the number of cores to use as a second argument.')
        main_serial()
    case 'main-parallel':
        main_parallel()
    case _:
        sys.exit(
            'Please enter one of the following arguments: test-serial test-parallel main-serial main-parallel')
