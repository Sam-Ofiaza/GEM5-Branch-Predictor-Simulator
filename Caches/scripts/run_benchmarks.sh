#!/bin/sh

OUTPUT_DIR_NAME=$1
GEM5_DIR=../../../gem5
BUILD_PATH=../builds
OUTPUT_PATH=../output
LOGS_PATH=../logs
SIM_PATH=$GEM5_DIR/configs/deprecated/example/se.py
BENCHMARK_PATH=../../../Project1_SPEC
HMMER_BENCHMARK_PATH=$BENCHMARK_PATH/"456.hmmer"/src/benchmark
HMMER_ARG_PATH=$BENCHMARK_PATH/"456.hmmer"/data/bombesin.hmm
SJENG_BENCHMARK_PATH=$BENCHMARK_PATH/"458.sjeng"/src/benchmark
SJENG_ARG_PATH=$BENCHMARK_PATH/"458.sjeng"/data/test.txt
BENCHMARK_ARGS=$2

start_time=`date +%s`

mkdir -p $OUTPUT_PATH/$OUTPUT_DIR_NAME/hmmer $OUTPUT_PATH/$OUTPUT_DIR_NAME/sjeng $LOGS_PATH/$OUTPUT_DIR_NAME
wait
$GEM5_DIR/build/X86/gem5.opt -d $OUTPUT_PATH/$OUTPUT_DIR_NAME/hmmer $SIM_PATH -c $HMMER_BENCHMARK_PATH -o $HMMER_ARG_PATH $BENCHMARK_ARGS &>> $LOGS_PATH/$OUTPUT_DIR_NAME/hmmer.log
wait
$GEM5_DIR/build/X86/gem5.opt -d $OUTPUT_PATH/$OUTPUT_DIR_NAME/sjeng $SIM_PATH -c $SJENG_BENCHMARK_PATH -o $SJENG_ARG_PATH $BENCHMARK_ARGS &>> $LOGS_PATH/$OUTPUT_DIR_NAME/sjeng.log
wait

echo $(expr `date +%s` - $start_time) s