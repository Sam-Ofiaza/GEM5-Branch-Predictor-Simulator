## Using GEM5 to simulate and compare 3 branch predictors with varying configuration sizes

###To get started:

1. Use PuTTY SSH to connect to the host ce6304.utdallas.edu
2. Create a project folder in either ~ or /proj/engclasses/ce6304/YourNetID
3. Navigate to that folder and download GEM5 to it by running cp -rf /usr/local/gem5 .
4. Navigate inside to the gem5 folder and compile the system for X86 architecture using scons build/X86/gem5.opt
5. Navigate to your project folder and run git init; git clone https://github.com/timberjack/Project1_SPEC
6. Navigate to gem5/src/cpu/simple, edit the BaseSimpleCPU.py file, and find the following line near the bottom:

```python
branchPred = Param.BranchPredictor(NULL, "Branch Predictor")
```

7. Replace NULL with either LocalBP(), TournamentBP(), or BiModeBP() and then run the following commands to recompile:
   Navigate to the gem5 folder
   Run the following:

```console
rm -rf build/X86; scons build/X86/gem5.opt
```

8. Run the test HelloWorld program:
   Navigate to the gem5 folder
   Run the following:

```console
./build/X86/gem5.opt ./configs/example/se.py -c ./tests/test-progs/hello/bin/x86/linux/hello
```

9. To see if the compilation was successful, navigate to gem5/m5out and check the branch predictor in config.ini

###Adding extra statistics to gem5/m5out/stats.txt:

- Navigate to src/cpu/pred
- Open bpred_unit.hh and search for 'BTBHitPct'
- Below that line, add the following:

```c
  /** Stat for percent times an entry in the BTB was not found. */
  Stats::Formula BTBMissPct;
```

- Open bpred_unit.cc and search for 'BTBHitPct'
- Below that line, add the following:

```c
BTBMissPct
.name(name() + ".BTBMissPct")
.desc("BTB Miss Percentage")
.precision(6);
BTBMissPct = 100.0 - BTBHitPct;
```

- Navigate to src/cpu/simple
- Open exec_context.hh and search for 'numBranchMispred'
- Below that line, add the following:

```c
/// Branch misprediction percentage
Stats::Formula branchMispredPct;
```

- Open base.cc and search for 'numBranchMispred'
- Below that line, add the following:

```c
t_info.branchMispredPct
.name(thread_str + ".BranchMispredPct")
.desc("Branch misprediction percentage")
.prereq(t_info.branchMispredPct);

t_info.branchMispredPct = (t_info.numBranchMispred / t_info.numBranches) \* 100;
```

###Overview of what will run in the script file

####Running a single benchmark

1. Navigate to Project1_SPEC/456.hmmer/
2. Create a new file runGem5.sh and enter the following code:

```console
   export GEM5_DIR=PATH_TO_GEM5_FOLDER
   export BENCHMARK=./src/benchmark
   export ARGUMENT=./data/FILENAME
   time $GEM5_DIR/build/X86/gem5.opt -d ./m5out $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o "$ARGUMENT" -I 5000000 --cpu-type=timing --caches --12cache --l1d_size=128kB --l1i_size=128kB --l2_size=1MB --l1d_assoc=2 --l1i_assoc=2 --l2_assoc=4 --cacheline_size=64
```

3. Change permissions to allow you to execute with chmod +x runGem5.sh
4. Run with ./runGem5.sh

####All values to try out:
All values used in tests should be powers of 2 (e.g., 1024, 2048, 4096, 8192)\
All BPs - BTB entries - 2048-4096\
Local BP - Local BP size - 1024-2048\
BiMode BP - Global BP size - 2048-8192\
BiMode BP - Choice Predictor size - 2048-8192\
Tournament BP - Local predictor size - 1024-2048\
Tournament BP - Global predictor size - 4096-8192\
Tournament BP - Choice predictor size - 4096-8192

####Possible combinations, total required recompilations
Local BP: 2 possible values for BTB entries \* 2 possible values for local BP size = 4\
BiMode BP: 2 possible values for BTB entries \* 3 possible values for global BP size \* 3 possible values for choice predictor size = 18\
Tourament BP: 2 possible values for BTB entries \* 2 possible values for local predictor size \* 2 possible values for global predictor size \* 2 possible values for choice predictor size = 16\
Total number of recompilations required = 4 + 18 + 16 = 38

####My Directory Structure:

- GEM5_Project
  - gem5
    - runTest.sh
    - recompile.sh
    - build/X86/gem5.opt
    - configs/example/se.py
    - tests/test-progs/hello/bin/x86/linux/hello
    - src/cpu/pred/BranchPredictor.py
  - Project1_SPEC
    - 456.hmmer
      - runGem5.sh
      - src/benchmark
      - data/bombesin.hmm
    - 458.sjeng
      - runGem5.sh
      - src/benchmark
      - data/test.txt
  - script.py
  - script.sh
  - run.sh
  - output.log
  - output
    - Local_2k_BTB_Entries_1k_Local_Pred_Size
      - hmmer
        - stats.txt
        - config.ini
      - sjeng
        - stats.txt
        - config.ini
  - logs
  - builds
    - Local_2k_BTB_Entries_1k_Local_Pred_Size
      - gem5
