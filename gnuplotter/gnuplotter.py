from __main__ import *

#-----maintaining backward compatibility----
try: out_folder 
except NameError: out_folder='auto'
#--------------------------------------------
import Pranay.files_structure.filenameGen as fileGen
from Pranay.gnuplotter.gnuplotter_basic import *

#------------main program-------------------
valid_file_blocks = fileGen.parameter_generator(all_parameters,vary_parameter,
              for_all_fixed,constant_parameter,base,fileStructure,out_folder)

if(len(valid_file_blocks)==0):
    print '\nNo files to be plotted'
else:
    script = open('script.plt', 'w')
    scriptHead(script)
    for outfile, title, fileData in valid_file_blocks:
        script.write( 'set output "%s.%s" \n'%(outfile,ext) )
        script.write( 'set title "%s" \n'%title )
        script.write( plotStatement(fileData,filenameClause) )
        script.write( '\n\n' )
    script.write( '\n' )
    script.write( 'unset output ; exit gnuplot \n' )
    script.close()
    if(plot):
        os.system('gnuplot script.plt')
        os.remove('script.plt')
#-----------------------------------------
