#!/usr/bin/env python2
#
# Python version of 3D-ICE-Emulator
#
# Based on 3D-ICE-Emulator.c from ESL @ EPFL
# Author: David Brenner (http://www.nano.ce.rit.edu)

import sys
import optparse
import time

# Import 3D-ICE module
import swig_3dice

EXIT_FAILURE = 1
EXIT_SUCCESS = 0

# main function
def main ():
    stkd     = swig_3dice.StackDescription()
    analysis = swig_3dice.Analysis()
    tdata    = swig_3dice.ThermalData()

    #emulate = swig_3dice.SimResult_t()

    #// Checks if there are the all the arguments
    #////////////////////////////////////////////////////////////////////////////
    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', action='store_true', default=False, help='verbose output')
    (options, args) = parser.parse_args()

    if( len(args) != 1 ):

        sys.stderr.write("Usage: \"%s file.stk\"\n" % (sys.argv[0]))
        return EXIT_FAILURE


    #// Init StackDescription and parse the input file
    #////////////////////////////////////////////////////////////////////////////

    #fprintf (stdout, "Preparing stk data ... ") ; fflush (stdout) ;
    print ("Preparing stk data ... ")

    swig_3dice.init_stack_description (stkd)
    swig_3dice.init_analysis          (analysis)

    error = swig_3dice.fill_stack_description (stkd, analysis, args[0])
    
    if (error != swig_3dice.TDICE_SUCCESS): return EXIT_FAILURE

    if ( analysis.AnalysisType == swig_3dice.TDICE_ANALYSIS_TYPE_TRANSIENT):

        emulate = swig_3dice.emulate_step

    elif (analysis.AnalysisType == swig_3dice.TDICE_ANALYSIS_TYPE_STEADY):

        emulate = swig_3dice.emulate_steady ;

    else:

        #fprintf (stderr, "unknown analysis type!\n ");
        sys.stderr.write("unknown analysis type!\n")

        swig_3dice.free_stack_description (stkd)

        return EXIT_FAILURE ;

    #fprintf (stdout, "done !\n") ;
    print "done !"

    #// Generate output files
    #////////////////////////////////////////////////////////////////////////////

    #// We use "% " as prefix for matlab compatibility (header will be a comment)

    error = swig_3dice.generate_analysis_headers (analysis, stkd.Dimensions, "% ")
    
    if (error != swig_3dice.TDICE_SUCCESS):
        #fprintf (stderr, "error in initializing output files \n ");
        sys.stderr.write("error in initializing output file \n")

        swig_3dice.free_stack_description (stkd) ;

        return EXIT_FAILURE ;

    #// Init thermal data and fill it using the StackDescription
    #////////////////////////////////////////////////////////////////////////////

    print "Preparing thermal data ... "

    swig_3dice.init_thermal_data (tdata)

    error = swig_3dice.fill_thermal_data (tdata, stkd, analysis)
    
    if (error != swig_3dice.TDICE_SUCCESS):
        
        swig_3dice.free_analysis          (analysis)
        swig_3dice.free_stack_description (stkd)

        return EXIT_FAILURE ;

    print "done !"

    #// Run the simulation and print the output
    #////////////////////////////////////////////////////////////////////////////

    start = time.time()

    #SimResult_t sim_result ;
    #sim_result = swig_3dice.SimResult_t()

    while True:
        sim_result = emulate (tdata, stkd, analysis)

        if (sim_result == swig_3dice.TDICE_STEP_DONE or sim_result == swig_3dice.TDICE_SLOT_DONE):
            print "%.3f " % ( swig_3dice.get_simulated_time (analysis) )

            swig_3dice.generate_analysis_output (analysis, stkd.Dimensions, tdata.Temperatures, swig_3dice.TDICE_OUTPUT_INSTANT_STEP) ;
        if (sim_result == swig_3dice.TDICE_SLOT_DONE):
            print ""

            swig_3dice.generate_analysis_output (analysis, stkd.Dimensions, tdata.Temperatures, swig_3dice.TDICE_OUTPUT_INSTANT_SLOT) ;
        if (sim_result == swig_3dice.TDICE_END_OF_SIMULATION):
            break

    swig_3dice.generate_analysis_output (analysis, stkd.Dimensions, tdata.Temperatures, swig_3dice.TDICE_OUTPUT_INSTANT_FINAL)

    #fprintf (stdout, "emulation took %.3f sec\n", ( (double)clock() - Time ) / CLOCKS_PER_SEC ) ;
    print "emulation took %.3f sec" % (time.time() - start)

    #// free all data
    #////////////////////////////////////////////////////////////////////////////

    swig_3dice.free_thermal_data      (tdata)
    swig_3dice.free_analysis          (analysis)
    swig_3dice.free_stack_description (stkd)

    return EXIT_SUCCESS ;


if __name__ == "__main__":
    main()
