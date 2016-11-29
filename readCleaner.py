###
### this script calls Trimmomatic to clean raw reads
###

import os,sys

def trimmomaticCaller(instance):
    
    '''
    this function deals with the trimming of the reads using Trimmomatic. Recommended options, ILLUMINACLIP:path2AdaptersFile:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
    '''

    print('working with file {}',instance)

    logFile=logFilesDir+instance+'.messagesFromTrimming.txt'

    inputFile1=rawReadsDir+instance+'_ALL1.fastq.gz'
    inputFile2=rawReadsDir+instance+'_ALL2.fastq.gz'

    outputFile1a=cleanReadsDir+instance+'_ALL1.clean.fastq.gz'
    outputFile1b=cleanReadsDir+instance+'_ALL1.garbage.fastq.gz'

    outputFile2a=cleanReadsDir+instance+'_ALL2.clean.fastq.gz'
    outputFile2b=cleanReadsDir+instance+'_ALL2.garbage.fastq.gz'

    cmd=javaPath+' -jar '+trimmomaticPath+' PE -threads 4 -phred33 -trimlog %s %s %s %s %s %s %s ILLUMINACLIP:%s:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36'%(logFile,inputFile1,inputFile2,outputFile1a,outputFile1b,outputFile2a,outputFile2b,path2Adapter)  

    print(cmd)
    #os.system(cmd)
    print()

    sys.exit()
    
    return None

### MAIN

# 0. defining user variables
rawReadsDir='/Users/alomana/scratch/FASTQ/'
cleanReadsDir='/Users/alomana/scratch/cleanFASTQ/'
logFilesDir='/Users/alomana/scratch/timmomaticLogs/'
path2Adapter='/Users/alomana/software/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa'

javaPath='/Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'
trimmomaticPath='/Users/alomana/software/Trimmomatic-0.36/trimmomatic-0.36.jar'

# 1. reading the files
tag='_ALL1.fastq.gz'
fastqFiles=os.listdir(rawReadsDir)
readFiles=[element for element in fastqFiles if tag in element]

# 2. calling Trimmomatic
for readFile in readFiles:
    instance=readFile.split(tag)[0]
    trimmomaticCaller(instance)
