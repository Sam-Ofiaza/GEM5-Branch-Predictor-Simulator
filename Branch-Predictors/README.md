## Comparing the Performance of Local BPs, BiMode BPs, and Tournament BPs with Varying Configurations

### How to set up:

- Create a project directory and navigate inside it\
- Clone the following GitHub repos side-by-side:
  - https://github.com/gem5/gem5 (Used version 23.0.1.0)
  - https://github.com/timberjack/Project1_SPEC
  - https://github.com/Sam-Ofiaza/GEM5-Simulator
- Download and install any dependencies you don't already have
  - https://www.gem5.org/documentation/general_docs/building
- Replace the following GEM5 source files with the modified ones in modified-src-files to add the extra BTBMissPct and branchMispredPct statistics:
  - gem5/src/cpu/simple/exec_context.hh
  - gem5/src/cpu/pred/bpred_unit.cc
  - gem5/src/cpu/pred/bpred_unit.hh

### How to run sequentially:

- Navigate into GEM5-Simulator/Branch-Predictors/scripts
- Run the following command:

```console
./run.sh main-serial <number of cores to be used>
```

### How to run in parallel:

- Navigate into GEM5-Simulator/Branch-Predictors/scripts
- Run the following command:

```console
./run.sh main-parallel
```

### How to collect the data into an excel file:

- Navigate into GEM5-Simulator/Branch-Predictors/data-collection
- Run the following command:

```console
python3 collect_complete_data.py <serial/parallel>
```

#### Range of configuration values:

All intermediate values are powers of 2 (e.g., 1024, 2048, 4096, 8192)\
All BPs - BTB entries - 2048-4096\
Local BP - Local BP size - 1024-2048\
BiMode BP - Global BP size - 2048-8192\
BiMode BP - Choice Predictor size - 2048-8192\
Tournament BP - Local predictor size - 1024-2048\
Tournament BP - Global predictor size - 4096-8192\
Tournament BP - Choice predictor size - 4096-8192

#### All combinations tested

Local BP: 2 possible values for BTB entries \* 2 possible values for local BP size = 4\
BiMode BP: 2 possible values for BTB entries \* 3 possible values for global BP size \* 3 possible values for choice predictor size = 18\
Tourament BP: 2 possible values for BTB entries \* 2 possible values for local predictor size \* 2 possible values for global predictor size \* 2 possible values for choice predictor size = 16

#### Total required recompilations = 4 + 18 + 16 = 38

#### Total required benchmark tests = 38 \* 2 = 76

#### Scripts' Expected Directory Structure:

- My-GEM5-Project
  - gem5
  - Project1_SPEC
    - 456.hmmer
    - 458.sjeng
  - GEM5-Simulator
    - Branch-Predictors
      - modified-src-files
      - scripts
      - builds
      - output-serial
      - output-parallel
      - data-collection
    - Caches
