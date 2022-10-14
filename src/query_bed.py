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

    for line in args.bed: #for every line in the bed file
        new_line= parse_line(line)
        table.add_line(new_line)
    
    for index_query in args.query: 
        query_setup = index_query.split("\t")
        query_chrom = query_setup [0]
        query_chrom_start = query_setup [1] 
        query_chrom_end = query_setup [2]

        chromosome_list= table.get_chrom(query_chrom) 
        # REMINDER from query.py this was set up: 
        #  def get_chrom(self, chrom: str) -> list[BedLine]:
        #"""Get all the lines that sits on chrom"""
        # return self.tbl[chrom]
       
        for index_bed in args.bed: 
            bed_setup = index_bed.split("\t")
            bed_chrom = bed_setup[0]
            bed_chrom_start = bed_setup[1]
            bed_chrom_end = bed_setup[2]

            if int(query_chrom_start) <= int(bed_chrom_start) and int(query_chrom_end)>= int(bed_chrom_end):
                print_line(chromosome_list, args.outfile)


 

if __name__ == '__main__':
    main()
