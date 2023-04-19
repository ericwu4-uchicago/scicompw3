#!/bin/env python

## SLURM variables

#SBATCH --account=mpcs56430
#SBATCH --job-name=porf
#SBATCH --output=%j_porf.out
#SBATCH --partition=broadwl

#SBATCH --cpus-per-task=3   # cores
#SBATCH --nodes=6            # number of nodes to run on       
#SBATCH --ntasks-per-node=3  # 
#SBATCH --ntasks=18         # total tasks to be launcedd

#SBATCH--exclusive
#SBATCH --time=00:05:00

import multiprocessing
from multiprocessing import Pool
from functools import partial
import time
import sys
import os
import numpy as np
from functools import reduce
from functools import partial
import argparse


def getparse(inputtext, offset):
    '''get characters when using a step size of offset'''
    text = np.array(list(inputtext))
    indexes = np.arange(0, text.size, offset)
    return text[indexes]

def totext(chararray):
    '''convert character array to a string'''
    return reduce(lambda a, b: a+b.lower(), chararray, "")

def getwordsintext(inputtext, wordlist):
    '''returns words in the given list that appear in the text'''
    hits = [word in inputtext for word in wordlist]
    return np.array(wordlist)[hits]

def writelisttofile(file, wordlist):
    '''writes given list of words to given file'''
    f = open(file, 'w')
    for word in wordlist:
        f.write(word + "\n")
    f.close()

def parse(offset, inputtextname, text, wordlist):
    text = np.array(text)
    filtered = getparse(text, offset)
    astext = totext(filtered)
    wordsfound = getwordsintext(astext, wordlist)
    filename = "/project2/mpcs56430/ericwu4/stride-" + str(offset) + "-" + inputtextname
    #filename = "files/stride-" + str(offset) + "-" + inputtextname #this is used for local testing
    writelisttofile(filename, wordsfound)

def prefilter(inputtext):
    '''keep only alphabetical characters'''
    return list(filter(lambda x: x.isalpha(), list(inputtext)))

def readfile(filename):
    '''convert given file to a blob of text'''
    text = ""
    f = open(filename, 'r', encoding = 'utf-8') 
    #https://stackoverflow.com/questions/491921/unicode-utf-8-reading-and-writing-to-files-in-python
    line = f.readline() #https://www.guru99.com/python-file-readline.html
    while line:
        line = line.strip()
        text += line
        line = f.readline()
    f.close()
    return text

def getwordlist(filename):
    '''convert 10000 word file to a list'''
    wordlist = []
    f = open(filename, 'r')
    line = f.readline().strip() #https://www.guru99.com/python-file-readline.html
    while line:
        if (len(line) > 2):
            wordlist.append(line)
        line = f.readline().strip()
    f.close()
    return wordlist


if __name__ == "__main__":
    # necessary to add cwd to path when script run 
    # by slurm (since it executes a copy)
    sys.path.append(os.getcwd()) 

    #job_id = os.environ["SLURM_JOB_ID"]
    nodes = int(os.environ["SLURM_NNODES"])
    #cpus_per_node = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])
    #tasks_per_node =  int(os.environ["SLURM_NTASKS_PER_NODE"])
    #cpus_per_task =  int(os.environ["SLURM_CPUS_PER_TASK"])
    #nprocs =  int(os.environ["SLURM_NPROCS"])

    print("nodes = %d" % int(os.environ["SLURM_NNODES"]))
    #print("cpus_per_node = %s" % os.environ["SLURM_JOB_CPUS_PER_NODE"])
    #print("tasks_per_node = %d" %  int(os.environ["SLURM_NTASKS_PER_NODE"]))
    #print("cpus_per_task =  %d" % int(os.environ["SLURM_CPUS_PER_TASK"]))
    #print("nprocs =  %d" % int(os.environ["SLURM_NPROCS"]))

    print(os.environ)

    SLURM_NPROCS = 6#nodes * cpus_per_task

    print("Number of Processes: %d" % SLURM_NPROCS)
    start = time.time()
    print("Start time: %s" % start)

    wordlist = getwordlist("google-10000-english-usa.txt")
    argParser = argparse.ArgumentParser() #https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    argParser.add_argument("-f ", "--filename", help="name of file to be parsed")
    args = argParser.parse_args()
    filename = args.filename
    text = readfile(filename)
    firstfilter = prefilter(text)
    cuts = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]#np.arange(2,20,1)
    func = partial(parse, inputtextname = filename, text = firstfilter, wordlist = wordlist)
    pool = Pool(processes = 6)
    pool.map(func, cuts)

    print("Run time: %f" % (time.time() - start))