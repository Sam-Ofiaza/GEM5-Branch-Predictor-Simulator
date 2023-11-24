#!/bin/sh

GEM5_DIR=../../../gem5
CUR_DIR_FROM_GEM5=../GEM5-Simulator/Caches/scripts
LOGS_PATH=../logs

start_time=`date +%s`

cd $GEM5_DIR
wait
if ! [ -f build/X86/gem5.opt ]; then
  scons build/X86/gem5.opt -j $1 &>> $CUR_DIR_FROM_GEM5/$LOGS_PATH/build.log
fi
wait

echo $(expr `date +%s` - $start_time) s