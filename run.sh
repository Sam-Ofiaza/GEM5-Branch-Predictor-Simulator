rm -rf output.log builds/* output/*
nohup python3 script.py $1 $2 &>> output.log &