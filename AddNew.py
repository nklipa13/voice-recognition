import sys
from Recording import record_to_file

WAVE_OUTPUT_FILENAME = str(sys.argv[1])

#print WAVE_OUTPUT_FILENAME

record_to_file(WAVE_OUTPUT_FILENAME, 2)

