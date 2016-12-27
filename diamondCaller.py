### this script reads the input fasta files and calls DIAMOND. The output files are in .m8 format. Script to be run in aegir under SGE environment.

import os,sys

def diamondDBbuilder():

    '''
    this function creates a runner file to be run in aegir under the SGE
    '''

    print 'building the database for DIAMOND...'
    # creating runner file
    inputFile=scratchDir+'databaseBuilder.sh'
    with open(inputFile,'w') as g:
        g.write('#!/bin/bash\n\n')
        g.write('#$ -N dbBuild\n')
        g.write('#$ -o %s/messages_database_DIAMOND.o.txt\n'%scratchDir)
        g.write('#$ -e %s/messages_database_DIAMOND.e.txt\n'%scratchDir)
        g.write('#$ -P Bal_alomana\n')
        g.write('#$ -pe serial %s\n'%threads)
        g.write('#$ -q baliga\n')
        g.write('#$ -S /bin/bash\n\n')
        g.write('cd /users/alomana\n')
        g.write('source .bash_profile\n\n')

        cmd='time '+diamondPath+' makedb --in '+dataBaseFastaFile+' -d '+dataBaseDiamondPath+' --threads '+str(threads)
        g.write('%s\n\n'%cmd)
        
    g.close()

    # submitting to queue
    cmd='qsub %s'%inputFile
    os.system(cmd)

    return None

def runnerCreator(tag):

    '''
    this function creates the runner files of aegir SGE system
    '''
    
    inputFile='{}sgeRunners/nr.{}.sh'.format(scratchDir,tag)
    with open(inputFile,'w') as g:
        g.write('#!/bin/bash\n\n')
        g.write('#$ -N %s\n'%tag)
        g.write('#$ -o %s/messagesDIAMOND.nr.%s.o.txt\n'%(scratchDir,tag))
        g.write('#$ -e %s/messagesDIAMOND.nr.%s.e.txt\n'%(scratchDir,tag))
        g.write('#$ -P Bal_alomana\n')
        g.write('#$ -pe serial %s\n'%threads)
        g.write('#$ -q baliga\n')
        g.write('#$ -S /bin/bash\n\n')
        g.write('cd /users/alomana\n')
        g.write('source .bashrc\n\n')

        cmd='time '+diamondPath+' blastx -d '+dataBaseDiamondPath+' -q '+fastaFilesDir+tag+'.fasta -a '+diamondOutputDir+tag+' --threads '+str(threads)+' --sensitive -e 1e-5' # e-value reference, http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3613424/
        g.write('%s\n\n'%cmd)

        cmd=diamondPath+' view -a '+diamondOutputDir+tag+'.daa -o '+diamondOutputDir+tag+'.m8'
        g.write('%s\n\n'%cmd)

    g.close()

    return None

# 0. user defined variables
threads=40
diamondPath='/proj/omics4tb/alomana/software/diamond-linux64_v0.8.16/diamond'
dataBaseFastaFile='/proj/omics4tb/alomana/software/diamond-linux64_v0.8.16/nr.91680400.20160801.fa'
dataBaseDiamondPath='/proj/omics4tb/alomana/software/diamond-linux64_v0.8.16/nr.91680400.20160801'
scratchDir='/proj/omics4tb/alomana/scratch/diamond/'

fastaFilesDir='/proj/omics4tb/alomana/projects/discovery/data/FASTA/'
diamondOutputDir='/proj/omics4tb/alomana/projects/discovery/data/diamond/'

# 1. building DIAMOND db
#diamondDBbuilder()
#sys.exit()

# 2. define the inputs
inputFiles=os.listdir(fastaFilesDir)

# 3. create launching the SGE calling files
for inputFile in inputFiles:
    tag=inputFile.split('.fasta')[0]
    runnerCreator(tag)

    # 2.1. launching
    cmd='qsub {}sgeRunners/nr.{}.sh'.format(scratchDir,tag)
    os.system(cmd)
    sys.exit()

print '... all done.'
