## Comparing the Performance of L1I, L1D, and L2 Caches with Varying Sizes and Associativites

### How to set up:

- Create a project directory and navigate inside it\
- Clone the following GitHub repos side-by-side:
  - https://github.com/gem5/gem5 (Used version 23.0.1.0)
  - https://github.com/timberjack/Project1_SPEC
  - https://github.com/Sam-Ofiaza/GEM5-Simulator
- Download and install any dependencies you don't already have
  - https://www.gem5.org/documentation/general_docs/building

### How to run:

- Navigate into GEM5-Simulator/Caches/scripts
- Run the following command:

```console
run.sh <number of cores to be used>
```

### How to collect the data into an excel file:

- Navigate into GEM5-Simulator/Caches/data-collection
- Run the following command:

```console
python3 collect_complete_data.py
```

#### Range of configuration values:

All intermediate values are powers of 2 (e.g., 1, 2, 4, 8, etc.)\
L1I Size - 1-128 KB\
L1D Size - 1-128 KB\
L2 Size - 1-128 KB\
Cacheline - 8-512 bytes\
L1I Associativity - 1-8\
L1D Associativity - 1-8\
L2 Associativity - 1-8

#### All configurations tested

Due to the number of possible configuration combinations (8 \* 8 \* 8 \* 7 \* 8 \* 8 \* 8 = 1,835,008), the exploration is limited to testing each factor independent of the others, reducing the number of tests to 55 (8 + 8 + 8 + 7 + 8 + 8 + 8)

#### Total required recompilations = 1 if GEM5 is not already compiled, else 0

#### Total required benchmark tests = 55 \* 2 = 110

#### Scripts' Expected Directory Structure:

- My-GEM5-Project
  - gem5
  - Project1_SPEC
    - 456.hmmer
    - 458.sjeng
  - GEM5-Simulator
    - Branch-Predictors
    - Caches
      - scripts
      - output
      - data-collection
