from __main__ import *

#---------generate filenames------------
if(fileStructure=='raw'):
    from Pranay.files_structure.filepath import raw_file_path as file_path
elif(fileStructure=='lib'):
    from Pranay.files_structure.filepath import lib_file_path as file_path
from Pranay.files_structure.filenameGen import *
def generate_parameters():
    return parameter_generator(all_parameters,vary_parameter,
            for_all_fixed,constant_parameter,base,file_path)
#-----------------------------------------


import os

def filenameClause(filepath,curve_title,colm):
    s =  '"%s" u %s '%(filepath,colm)
    s += 'w %s title "%s" '%(plot_With,curve_title)
    return s

def plotStatement(fileData,plotClause):
    filepath,curve_title = fileData[0]
    using_colms = colmGen()
    colm = using_colms.next()
    s = 'plot %s'%plotClause(filepath,curve_title,colm)
    for filepath,curve_title in fileData[1:]:
        colm = using_colms.next()
        s+= ', \t \\\n     '
        s+= plotClause(filepath,curve_title,colm)
    return s

#-----terminal--------
if(terminal=='jpeg') : ext = 'jpg'
if(terminal== 'png') : ext = 'png'
if(terminal== 'eps')  :
    ext = 'eps'
    terminal = 'postscript enhanced color font "Helvetica,24"'

def scriptHead(scriptfile):
    scriptfile.write( 'set terminal %s \n\n'%terminal )
    if(set_grid): scriptfile.write( 'set grid \n\n' )

    scriptfile.write( 'set xlabel "%s" \n'%xlabel )
    scriptfile.write( 'set ylabel "%s" \n'%ylabel )
    if(xRangeflag == True): scriptfile.write( 'set xrange [%s:%s] \n\n'%xRange )
    if(yRangeflag == True): scriptfile.write( 'set yrange [%s:%s] \n\n'%yRange )
    scriptfile.write( '\n' )


#------------------------------------------------------------
# parameter format - list of [   plotFilename_wihtout_ext,
#                                        curve_title,
#                               [ (filepath1, title1),
#                                 (filepath2, title2),  ]   ]
def generate_script(parameters,outFolder,plotBlock):
    script = open('script.plt', 'w')
    scriptHead(script)
    for outfile, title, fileData in parameters:
        script.write( 'set output "%s/%s.%s" \n'%(outFolder,outfile,ext) )
        script.write( 'set title "%s" \n'%title )
        script.write( plotBlock(fileData) )
        script.write( '\n\n' )
    script.write( '\n' )
    script.write( 'unset output ; exit gnuplot \n' )
    script.close()
#-----------------------------------------------------------------------

def plotBlock(fileData):
    return plotStatement(fileData,filenameClause)


#------------main program-------------------
valid_file_blocks = generate_parameters()
if(len(valid_file_blocks)>0):
    folderName = all_parameters[vary_parameter][0]
    folderName = folderName.split('=')[0]
    folderName = 'varying '+folderName

    if(not os.path.isdir(folderName) ):
        os.mkdir(folderName)
    generate_script(valid_file_blocks,folderName,plotBlock)

    if(plot):
        os.system('gnuplot script.plt')
        os.remove('script.plt')
else:
    print '\nNo files found'
#-----------------------------------------
