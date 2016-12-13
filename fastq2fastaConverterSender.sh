#!/bin/bash

#$ -N discovery
#$ -o /proj/omics4tb/alomana/scratch/messages.discovery.o.txt
#$ -e /proj/omics4tb/alomana/scratch/messages.discovery.e.txt
#$ -P Bal_alomana
#$ -pe serial 64
#$ -q baliga
#$ -S /bin/bash

cd /users/alomana
source .bash_profile

cd /proj/omics4tb/alomana/projects/discovery/deployment
time python fastq2fastaConverter.py > messages.discovery.txt
