#!/usr/bin/python
# vim: set fileencoding=utf-8
import pprint
import struct
import sys
from DataParser.DataParser import HeaderParser, DataParser

def main():
    if len(sys.argv) < 1:
        raise(ValueError("you need to point to a bsp file"))
        sys.exit(1)

    # Read a header with the definitions
    header_parser = HeaderParser("bsp.h")
    pp = pprint.PrettyPrinter()
    pp.pprint(header_parser.get_definitions())

    # create a parser with created definitions
    parser = DataParser(header_parser.get_definitions())

    with open(sys.argv[1], 'rb') as input_bsp_file:
        print("Reading in a \"{}\" and printing the header and textures".format(sys.argv[1]))
        input_bsp_data = input_bsp_file.read()
        # give the parser a chunk of data and the type you want to parse
        parsed_header = parser.parse('dheader_t', input_bsp_data)
        if parsed_header.version != 29:
            raise(ValueError("map version != 29 ({})".format(parsed_header.version)))
        parsed_header.prints()

        # this shit needs to change
        header_offset = parsed_header.miptex.offset
        parsed_mipheader = parser.parse('mipheader_t', input_bsp_data[header_offset:])
        # this shit needs to change
        count = parsed_mipheader.numtex
        offset = parsed_mipheader.offset

        for i in range(0, count-1):
            parsed_texture = parser.parse('miptex_t', input_bsp_data[header_offset + offset:])
            parsed_texture.prints()
            # read next offset
            parsed_new_offset = parser.parse('long', input_bsp_data[header_offset + (i) * 4:])
            # this somewhat still sucks, that you need to call __value on basetypes
            offset = parsed_new_offset.__value

        # just testing vec_t
        l = [0.0, 0.1, 0.2]
        print("testing vec3_t: {}".format(l))
        data = struct.pack("<fff", *l)
        parsed = parser.parse('vec3_t', data)
        parsed.prints()


if __name__ == '__main__':
    main()


