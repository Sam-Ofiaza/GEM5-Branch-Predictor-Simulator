#!/bin/sh

OUTPUT_DIR_NAME=$1
GEM5_DIR=./gem5
BUILD_PATH=./builds
OUTPUT_PATH=./output
HMMER_BENCHMARK_PATH=./Project1_SPEC/"456.hmmer"/src/benchmark
HMMER_ARG_PATH=./Project1_SPEC/"456.hmmer"/data/bombesin.hmm
SJENG_BENCHMARK_PATH=./Project1_SPEC/"458.sjeng"/src/benchmark
SJENG_ARG_PATH=./Project1_SPEC/"458.sjeng"/data/test.txt
BENCHMARK_ARGS="-I 5000000 --cpu-type=timing --caches --l2cache --l1d_size=128kB --l1i_size=128kB --l2_size=1MB --l1d_assoc=2 --l1i_assoc=2 --l2_assoc=4 --cacheline_size=64"

start_time=`date +%s`

mkdir -p $BUILD_PATH/$OUTPUT_DIR_NAME
wait
cp -rf $GEM5_DIR $BUILD_PATH/$OUTPUT_DIR_NAME
wait
mkdir -p $OUTPUT_PATH/$OUTPUT_DIR_NAME/hmmer $OUTPUT_PATH/$OUTPUT_DIR_NAME/sjeng
wait
cd $GEM5_DIR
wait
rm -rf build/X86
wait 
scons ../$BUILD_PATH/$OUTPUT_DIR_NAME/build/X86/gem5.opt &>> ../$OUTPUT_PATH/$OUTPUT_DIR_NAME/build.log
wait
cd ..
wait
$BUILD_DIR/$OUTPUT_DIR_NAME/gem5/build/X86/gem5.opt -d $OUTPUT_PATH/$OUTPUT_DIR_NAME/hmmer $BUILD_DIR/$OUTPUT_DIR_NAME/gem5/configs/example/se.py -c $HMMER_BENCHMARK_PATH -o $HMMER_ARG_PATH $BENCHMARK_ARGS &>> $OUTPUT_PATH/$OUTPUT_DIR_NAME/hmmer.log
wait
$BUILD_DIR/$OUTPUT_DIR_NAME/gem5/build/X86/gem5.opt -d $OUTPUT_PATH/$OUTPUT_DIR_NAME/sjeng $GEM5_DIR/configs/example/se.py -c $SJENG_BENCHMARK_PATH -o $SJENG_ARG_PATH $BENCHMARK_ARGS &>> $OUTPUT_PATH/$OUTPUT_DIR_NAME/sjeng.log
wait
rm -rf $BUILD_PATH/$OUTPUT_DIR_NAME

# mkdir -p $OUTPUT_PATH/$OUTPUT_DIR_NAME/hmmer $OUTPUT_PATH/$OUTPUT_DIR_NAME/sjeng && cd $GEM5_DIR && rm -rf build/X86 && scons build/X86/gem5.opt -j4 &>> ../$OUTPUT_PATH/$OUTPUT_DIR_NAME/build.log && cd .. && $GEM5_DIR/build/X86/gem5.opt -d $OUTPUT_PATH/$OUTPUT_DIR_NAME/hmmer $GEM5_DIR/configs/example/se.py -c $HMMER_BENCHMARK_PATH -o $HMMER_ARG_PATH $BENCHMARK_ARGS &>> $OUTPUT_PATH/$OUTPUT_DIR_NAME/hmmer.log && $GEM5_DIR/build/X86/gem5.opt -d $OUTPUT_PATH/$OUTPUT_DIR_NAME/sjeng $GEM5_DIR/configs/example/se.py -c $SJENG_BENCHMARK_PATH -o $SJENG_ARG_PATH $BENCHMARK_ARGS &>> $OUTPUT_PATH/$OUTPUT_DIR_NAME/sjeng.log

echo $(expr `date +%s` - $start_time) s