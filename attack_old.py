import subprocess
from time import perf_counter_ns
from subprocess import Popen, PIPE , STDOUT
import multiprocessing
import psutil
import os
import sys
import re
from math import inf
import matplotlib.pyplot as plt
bin = "./vuln"
MAX_STRING_SIZE = 30
BATCH_SIZE = 15
THREADS = 10




def test_for_input(inp: str, num):
    sum = 0
    min = inf
    for i in range(num):
        cmd = f"echo {inp} | valgrind --tool=callgrind    --callgrind-out-file=cg.out {bin}"
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        p.wait()
        out = p.communicate()
        out = out[1].decode("utf-8")
        out = out.split("\n")
        ins = 0
        for line in out:
            if "Collected" in line:
                ins = int(line.split(" ")[3])
                break
        sum += ins
        if ins < min:
            min = ins
    ins = sum / num
    return (ins,min)


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"



char_time = {}
pool = multiprocessing.Pool(processes=THREADS)
##test for size
inputs = []
for i in range(1, MAX_STRING_SIZE):
    inputs.append('A' * i)

results = pool.starmap(test_for_input, [(inp, BATCH_SIZE) for inp in inputs])
maxtime = 0

avg_or_min = 0
probable_len = 0
for i in range(len(results)):
    print(f"Size: {i + 1} Average: {results[i][avg_or_min]} Min: {results[i][avg_or_min]}")
    if i >0 and i < len(results) - 1:
        if results[i-1][avg_or_min] < results[i][avg_or_min] and results[i][avg_or_min] > results[i+1][avg_or_min]:
            probable_len = i+1


    
print(f"Probable length: {probable_len}")
plt.plot(range(1, MAX_STRING_SIZE), [x[avg_or_min] for x in results])
plt.show()

length = probable_len
##test for characters]
known = ""
for i in range(length):
    char_time = {}
    for char in alphabet:
        inp = known + char + 'A' * (length - len(known) - 1)
        results = pool.starmap(test_for_input, [(inp, BATCH_SIZE)])
        char_time[char] = results[0][avg_or_min]
    maxtime = 0
    maxchar = ""
    for char in char_time:
        if char_time[char] > maxtime:
            maxtime = char_time[char]
            maxchar = char
    known += maxchar
    print(known)
    print(f"Time: {maxtime}")
    print("")
