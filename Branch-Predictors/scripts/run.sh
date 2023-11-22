rm -rf script.log ../builds/* ../output-serial/* ../output-parallel/*
nohup python3 script.py $1 $2 &>> script.log &