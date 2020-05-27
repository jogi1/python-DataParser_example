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
        if parsed_mipheader.numtex != len(parsed_mipheader.offset):
            raise("DataParser: array_length_reference missmatch")
        else:
            print("DataParser 'array_length_reference' ok.")

        # reading offsets manualy
        parsed_offsets = parser.parse('long:__:{}'.format(count), input_bsp_data[header_offset + 4:]).__value
        print(parsed_offsets)
        # useing the DataParser={'array_length_reference': 'numtex'} extension in the comment in bsp.h
        parsed_offsets = parsed_mipheader.offset
        print(parsed_offsets)
        for offset in parsed_offsets:
            parsed_texture = parser.parse('miptex_t', input_bsp_data[header_offset + offset:])
            parsed_texture.prints()

        # just testing vec_t
        l = [0.0, 0.1, 0.2]
        print("testing vec3_t: {}".format(l))
        data = struct.pack("<fff", *l)
        vec3_t = parser.parse('vec3_t', data)
        vec3_t.prints()
        vec3_t.x = 1.123
        vec3_t.prints()
        print(len(data))
        new_data = vec3_t.pack()
        print(len(new_data))
        vec3_t_new_data = parser.parse('vec3_t', new_data)
        vec3_t_new_data.prints()

        # testint array packing
        l = [1, 2]
        data = struct.pack("<ll", *l)
        parsed_longs = parser.parse('long:__:{}'.format(len(l)), data)
        parsed_longs.prints()
        new_data = parsed_longs.pack()
        if new_data != data:
            print("packing didnt work")
        parsed_longs.__value[0] = 4
        parsed_longs.prints()

        new_data = parsed_longs.pack()
        if new_data == data:
            print("packing didnt work")

        print(struct.unpack("<ll", new_data))


if __name__ == '__main__':
    main()


