rm -rf ../logs/script.log ../output
nohup python3 script.py $1 &>> ../logs/script.log &