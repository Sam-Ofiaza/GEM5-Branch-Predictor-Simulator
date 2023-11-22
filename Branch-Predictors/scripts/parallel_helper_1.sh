#!/bin/sh

OUTPUT_DIR_NAME=$1
GEM5_DIR=../../../gem5
BUILD_PATH=../builds

rm -rf $GEM5_DIR/build/X86
wait
mkdir -p $BUILD_PATH/$OUTPUT_DIR_NAME
wait
cp -rf $GEM5_DIR $BUILD_PATH/$OUTPUT_DIR_NAME
wait