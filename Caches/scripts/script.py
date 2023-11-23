import subprocess
import sys
import multiprocessing as mp

GEM5_DIR = '../../../gem5'
LOGS_DIR = '../logs'


def reset_bp():
    '''Sets the simulator branch predictor to NULL'''
    with open(f'{GEM5_DIR}/src/cpu/pred/BranchPredictor.py', 'r', encoding='utf-8') as file:
        data = file.readlines()

    data[40] = '    branchPred = Param.BranchPredictor(NULL, "Branch Predictor")'

    with open(f'{GEM5_DIR}/src/cpu/pred/BranchPredictor.py', 'w', encoding='utf-8') as file:
        file.writelines(data)


reset_bp()
subprocess.call(['./recompile.sh', sys.argv[1],
                '&>>', f'{LOGS_DIR}/recompile.log'])
