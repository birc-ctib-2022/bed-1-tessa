"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from bed import (
    BedLine, parse_line, print_line
)
from query import Table


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(
        description="Extract regions from a BED file")
    argparser.add_argument('bed', type=argparse.FileType('r'))
    argparser.add_argument('query', type=argparse.FileType('r'))

    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                           metavar='output',  # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work

    table = Table() #make an empty table

    for line in args.bed: #for every line in the bed input file
        new_line= parse_line(line) #parse line
        table.add_line(new_line) # add it to table 
    #now input is tab seperated and ready to extract

    for index_query in args.query: 
    #for every line in query input file 
        query_setup = index_query.split("\t")
        #make it tab seperated (because it should come in as 
        #bedfile)
        query_chrom = query_setup [0]
        #assign query_chrom to index 0 
        query_chrom_start = query_setup [1] 
        #assign query_chrom_start to index 1 
        query_chrom_end = query_setup [2]
        #assign query_chrom_end to index 2 

        chromosome_list= table.get_chrom(query_chrom) 
        # REMINDER from query.py this was set up: 
        #  def get_chrom(self, chrom: str) -> list[BedLine]:
        #"""Get all the lines that sits on chrom"""
        # return self.tbl[chrom]
        #so now chromosome_list is a table with all of the lines 
        #that sit on the chromosome identified in query[0]
        
       
        for index_bed in chromosome_list: 
        #for every line in chromosome_list which is table 
        #with all of the lines that sit on the desired chromosomes 
        #identified in query file 
            bed_chrom = index_bed[0]
            #assign bed_chrom to index [0]
            bed_chrom_start = index_bed[1]
            #assgin bed_chrom_start to index [1]
            bed_chrom_end = index_bed[2]
            #assign bed_chrom_end to index [2]

            if int(query_chrom_start) <= int(bed_chrom_start) and int(query_chrom_end)>= int(bed_chrom_end):
            #if line in chromosome list is in the correct interval, add it to output     
                print_line(index_bed, args.outfile)


 

if __name__ == '__main__':
    main()
