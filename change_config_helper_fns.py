BP_TYPES = {
    50: lambda x: f'    branchPred = Param.BranchPredictor({x}, "Branch Predictor")'
}

BP_PARAMS = {
    39: lambda x: f'    BTBEntries = Param.Unsigned({x}, "Number of BTB entries")\n',
    50: lambda x: f'    localPredictorSize = Param.Unsigned({x}, "Size of local predictor")\n',
    73: lambda x: f'    globalPredictorSize = Param.Unsigned({x}, "Size of global predictor")\n',
    75: lambda x: f'    choicePredictorSize = Param.Unsigned({x}, "Size of choice predictor")\n',
    59: lambda x: f'    localPredictorSize = Param.Unsigned({x}, "Size of local predictor")\n',
    62: lambda x: f'    globalPredictorSize = Param.Unsigned({x}, "Size of global predictor")\n',
    64: lambda x: f'    choicePredictorSize = Param.Unsigned({x}, "Size of choice predictor")\n',
}


def modify_file(filepath, callback):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.readlines()

    callback(data)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(data)


def change_bp_type(data, name=None):
    data[50] = BP_TYPES[50](name)
    # print(name, end=' ')


def change_local_bp_config(data, btb_entries=None, local_pred_size=None):
    data[39] = BP_PARAMS[39](btb_entries)
    data[50] = BP_PARAMS[50](local_pred_size)
    # print(f'{btb_entries=} {local_pred_size=}')


def change_bimode_bp_config(data, btb_entries=None, global_pred_size=None, choice_pred_size=None):
    data[39] = BP_PARAMS[39](btb_entries)
    data[73] = BP_PARAMS[73](global_pred_size)
    data[75] = BP_PARAMS[75](choice_pred_size)
    # print(f'{btb_entries=} {global_pred_size=} {choice_pred_size=}')


def change_tourny_bp_config(data, btb_entries=None, local_pred_size=None, global_pred_size=None, choice_pred_size=None):
    data[39] = BP_PARAMS[39](btb_entries)
    data[59] = BP_PARAMS[59](local_pred_size)
    data[62] = BP_PARAMS[62](global_pred_size)
    data[64] = BP_PARAMS[64](choice_pred_size)
    # print(f'{btb_entries=} {local_pred_size=} {global_pred_size=} {choice_pred_size=}')
