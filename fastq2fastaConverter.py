###
### this script converts in a multithread mode FASTQ files into FASTA files
###

import sys,os
import multiprocessing, multiprocessing.pool

def flexibleConverter(tag):

    '''
    this function uncompress gz files and convert them into FASTA files
    '''
    print()
    # f.1. unzipping the file
    cmd1='gunzip -c {}{}_ALL1.clean.fastq.gz > {}{}_ALL1.clean.fastq'.format(fastqDir,tag,fastaDir,tag)
    cmd2='gunzip -c {}{}_ALL2.clean.fastq.gz > {}{}_ALL2.clean.fastq'.format(fastqDir,tag,fastaDir,tag)
    print(cmd1)
    os.system(cmd1)    
    print(cmd2)
    os.system(cmd2)

    # f.2. checking the quality of the paired-end reads
    cmd='pearf -1 {}{}_ALL1.clean.fastq -2 {}{}_ALL2.clean.fastq > {}{}.pearf.message.txt'.format(fastaDir,tag,fastaDir,tag,scratchDir,tag)
    print(cmd)
    os.system(cmd)
    

    # f.3. actual conversion into FASTA files
    cmd0="awk 'BEGIN{P=1}{if(P==1||P==2){gsub(/^[@]/,\">\");print}; if(P==4)P=0; P++}'"
    cmd1=' {}{}_ALL1.clean.fastq.filtered.fastq > {}{}_ALL1.fasta'.format(fastaDir,tag,fastaDir,tag)
    cmd2=' {}{}_ALL2.clean.fastq.filtered.fastq > {}{}_ALL2.fasta'.format(fastaDir,tag,fastaDir,tag)
    cmd3=cmd0+cmd1
    cmd4=cmd0+cmd2
    print(cmd3)
    os.system(cmd3)
    print(cmd4)
    os.system(cmd4)

    # f.4. separation print
    print()
    
    return None


# 0. user defined variables
fastqDir='/proj/omics4tb/alomana/projects/discovery/data/cleanFASTQ/'
fastaDir='/proj/omics4tb/alomana/projects/discovery/data/FASTA/'
scratchDir='/proj/omics4tb/alomana/scratch/'

numberOfThreads=64 # this should be 64

# 1. detecting all paired tags
print('detecting samples...')
fastqFiles=os.listdir(fastqDir)
tags=[]
for element in fastqFiles:
    if '_ALL' in element:
        tag=element.split('_ALL')[0]
        if tag not in tags:
            tags.append(tag)
tags.sort()
print(tags)
print('{} samples detected.'.format(len(tags)))

# 2. iterating over all files
print('parallel conversion of files...')

hydra=multiprocessing.pool.Pool(numberOfThreads)
output=hydra.map(flexibleConverter,tags)
