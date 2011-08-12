# -*- coding: utf-8 -*-
"""
tiff minimalistic parser
(c)2010 Timothee Groleau
with code taken from PIL
"""

import sys
import struct

from nefarious.constants import *



class EndianMachine:

    def getPrefix(self):
        return "<" if self.mode == "little" else ">"

    def isOrder(self, mode):
        return self.mode == mode

    def __init__(self, mode=sys.byteorder):
        self.mode = mode


class DataParser:
    def __init__(self, em):
        self.em = em

    def load_type(self, zeType, data):
        unitSize, strucPattern, typeName = TYPES[zeType]

        # verify that the data size is sane
        if len(data) % unitSize != 0:
            raise RuntimeError("invalid byte count (%d) to read %s of unitsize %d" % (len(data), typeName, unitSize))

        nUnits = int( len(data) / unitSize )

        return list( struct.unpack(self.em.getPrefix() + strucPattern * nUnits, data) )

    def load_byte(self, data):
        return self.load_type(TYPE_BYTE, data)

    def load_sbyte(self, data):
        return self.load_type(TYPE_SBYTE, data)

    def load_string(self, data):
        if data[-1:] == '\0':
            data = data[:-1]
        return data

    def load_short(self, data):
        return self.load_type(TYPE_SHORT, data)

    def load_sshort(self, data):
        return self.load_type(TYPE_SSHORT, data)

    def load_long(self, data):
        return self.load_type(TYPE_LONG, data)

    def load_slong(self, data):
        return self.load_type(TYPE_SLONG, data)

    def load_rational(self, data, zeType=TYPE_RATIONAL):
        a = self.load_type(zeType, data)
        l = []
        for i in range(0, len(a), 2):
            l.append([a[i], a[i+1]])
        return l

    def load_srational(self, data):
        return self.load_rational(data, TYPE_SRATIONAL)

    def load_float(self, data):
        return self.load_type(TYPE_FLOAT, data)

    def load_double(self, data):
        return self.load_type(TYPE_DOUBLE, data)

    def load_undefined(self, data):
        # Untyped data
        return data

setattr(DataParser, "%d" % (TYPE_BYTE, ),      DataParser.load_byte)
setattr(DataParser, "%d" % (TYPE_ASCII, ),     DataParser.load_string)
setattr(DataParser, "%d" % (TYPE_SHORT, ),     DataParser.load_short)
setattr(DataParser, "%d" % (TYPE_LONG, ),      DataParser.load_long)
setattr(DataParser, "%d" % (TYPE_RATIONAL, ),  DataParser.load_rational)
setattr(DataParser, "%d" % (TYPE_SBYTE, ),     DataParser.load_sbyte)
setattr(DataParser, "%d" % (TYPE_UNDEFINED, ), DataParser.load_undefined)
setattr(DataParser, "%d" % (TYPE_SSHORT, ),    DataParser.load_sshort)
setattr(DataParser, "%d" % (TYPE_SLONG, ),     DataParser.load_slong)
setattr(DataParser, "%d" % (TYPE_SRATIONAL, ), DataParser.load_srational)
setattr(DataParser, "%d" % (TYPE_FLOAT, ),     DataParser.load_float)
setattr(DataParser, "%d" % (TYPE_DOUBLE, ),    DataParser.load_double)


class DataWriter:
    def __init__(self, em):
        self.em = em

    def get_type(self, zeType, data):
        _, strucPattern, _ = TYPES[zeType]

        return struct.pack(self.em.getPrefix() + strucPattern * len(data), *data)

    def get_byte(self, data):
        return self.get_type(TYPE_BYTE, data)

    def get_sbyte(self, data):
        return self.get_type(TYPE_SBYTE, data)

    def get_string(self, data):
        if (data[-1:] != '\0'):
            data += chr(0)
        return data

    def get_short(self, data):
        return self.get_type(TYPE_SHORT, data)

    def get_sshort(self, data):
        return self.get_type(TYPE_SSHORT, data)

    def get_long(self, data):
        return self.get_type(TYPE_LONG, data)

    def get_slong(self, data):
        return self.get_type(TYPE_SLONG, data)

    def get_rational(self, data, zeType=TYPE_LONG):
        l = []
        for pair in data:
            l.append(pair[0])
            l.append(pair[1])
        return self.get_type(zeType, l)

    def get_srational(self, data):
        return self.get_rational(data, TYPE_SLONG)

    def get_float(self, data):
        return self.get_type(TYPE_FLOAT, data)

    def get_double(self, data):
        return self.get_type(TYPE_DOUBLE, data)

    def get_undefined(self, data):
        # Untyped data
        return data

setattr(DataWriter, "%d" % (TYPE_BYTE, ),      DataWriter.get_byte)
setattr(DataWriter, "%d" % (TYPE_ASCII, ),     DataWriter.get_string)
setattr(DataWriter, "%d" % (TYPE_SHORT, ),     DataWriter.get_short)
setattr(DataWriter, "%d" % (TYPE_LONG, ),      DataWriter.get_long)
setattr(DataWriter, "%d" % (TYPE_RATIONAL, ),  DataWriter.get_rational)
setattr(DataWriter, "%d" % (TYPE_SBYTE, ),     DataWriter.get_sbyte)
setattr(DataWriter, "%d" % (TYPE_UNDEFINED, ), DataWriter.get_undefined)
setattr(DataWriter, "%d" % (TYPE_SSHORT, ),    DataWriter.get_sshort)
setattr(DataWriter, "%d" % (TYPE_SLONG, ),     DataWriter.get_slong)
setattr(DataWriter, "%d" % (TYPE_SRATIONAL, ), DataWriter.get_srational)
setattr(DataWriter, "%d" % (TYPE_FLOAT, ),     DataWriter.get_float)
setattr(DataWriter, "%d" % (TYPE_DOUBLE, ),    DataWriter.get_double)


class Tag:
    def __init__(self, code=0, type=0, data=0, offset=None):
        self.code   = code
        self.type   = type
        self.data   = data
        self.offset = offset
        self.parent = None

    def dataSize(self):
        unitSize, _, _ = TYPES[self.type]
        return unitSize * len(self.data)

    def needsDataBlock(self):
        """determines whether a block to hold the tag data must be allocated (data size > 4 bytes)"""
        if len(self.data) > 0 and isinstance(self.data[0], ImageFileDirectory):
            return True
        elif self.type == TYPE_ASCII and self.dataSize()+1 > 4:
            return True
        elif self.dataSize() > 4:
            return True
        else:
            return False

    def toString(self):
        tagname = ''
        if self.parent:
            if TAGS.has_key((self.parent.code, self.code)):
                tagname = TAGS[(self.parent.code, self.code)]

        if not tagname and TAGS.has_key(self.code):
            tagname = TAGS[self.code]

        return "tag: %d (%s), type: %d (%s), count: %d" % (
                self.code
              , tagname if tagname else "unknown"
              , self.type
              , TYPES[self.type][2]
              , len(self.data)
           )



class ImageFileDirectory:
    def __init__(self, parentTag=None):
        self.parentTag = parentTag
        self.tags = []
        self.tags_by_code = {}
        self.ifds = None
        self.offset = None

        self.imageType = None
        self.imageData = None


    def load(self, fp, em, level=0):
        """reads an ifd directory, file pointer must already be at the right location!!"""

        #instanciate a data parser
        parser = DataParser( em )

        # read tag count
        tagcount = getattr(parser, "%d" % TYPE_SHORT)( fp.read(2) )[0]

        # read all tags
        for i in range(tagcount):

            tagBlock = fp.read(12)

            tagCode = getattr(parser, "%d" % TYPE_SHORT)( tagBlock[:2] )[0]
            zeType  = getattr(parser, "%d" % TYPE_SHORT)( tagBlock[2:4] )[0]
            count   = getattr(parser, "%d" % TYPE_LONG)( tagBlock[4:8] )[0]
            rawdata = tagBlock[8:]

            unitSize, _, _ = TYPES[zeType]
            size = count * unitSize

            if size <= 4:
                rawdata = rawdata[:size]
            else:
                oldOffset = fp.tell()
                nextOffset = getattr(parser, "%d" % TYPE_LONG)( rawdata )[0]
                fp.seek( nextOffset )
                rawdata = fp.read( size )
                fp.seek( oldOffset )

            if len(rawdata) != size:
                raise IOError, "not enough data"

            if TYPES.has_key( zeType ):
                data = getattr(parser, "%d" % zeType)( rawdata )
            else:
                data = rawdata

            if tagCode in [TAG_SUBIFD, TAG_EXIFIFD, TAG_GPS_INFO]:
                # read all sub ifds
                oldOffset = fp.tell()
                ifds = []
                tag = Tag(tagCode, zeType, ifds)
                for offset in data:
                    fp.seek( offset )
                    subIfd = ImageFileDirectory(tag)
                    subIfd.load(fp, em, level+1)
                    ifds.append( subIfd )
                fp.seek(oldOffset)

            else:
                tag = Tag(tagCode, zeType, data)


            if self.parentTag:
                tag.parent = self.parentTag

            self.tags.append( tag )
            self.tags_by_code[ tagCode ] = tag

        # all tags have been read, next long is the next ifd offset that will be read used by the CALLER
        # hence, save current offset before fetching image data
        oldOffset = fp.tell()

        if self.tags_by_code.has_key( TAG_SUBIFD ):
            self.ifds = self.tags_by_code[ TAG_SUBIFD ].data

        if self.tags_by_code.has_key( TAG_JPEG_INTERCHANGE_FORMAT ) and self.tags_by_code.has_key( TAG_JPEG_INTERCHANGE_FORMAT_LENGTH ):
            # jpeg images are stored as one blob!
            self.imageType = "JPEG"
            fp.seek( self.tags_by_code[TAG_JPEG_INTERCHANGE_FORMAT].data[0] )
            self.imageData = fp.read( self.tags_by_code[TAG_JPEG_INTERCHANGE_FORMAT_LENGTH].data[0] )

        elif self.tags_by_code.has_key( TAG_STRIPOFFSETS ) and self.tags_by_code.has_key( TAG_STRIPBYTECOUNTS ):
                # tiff data are stored as strips, imageData will contain the strip from the original file...
            if (len(self.tags_by_code[ TAG_STRIPOFFSETS ].data) != len(self.tags_by_code[ TAG_STRIPBYTECOUNTS ].data)):
                raise SyntaxError, "unmatched image data tags"

            self.imageType = "TIFF"
            self.imageData = []
            for i in range(len(self.tags_by_code[ TAG_STRIPOFFSETS ].data)):
                fp.seek( self.tags_by_code[ TAG_STRIPOFFSETS ].data[i] )
                self.imageData.append( fp.read( self.tags_by_code[ TAG_STRIPBYTECOUNTS ].data[i] ) )

        # image data has been read, now return to correct offset before passing the hand back to caller...
        fp.seek( oldOffset )


    def save(self, fp, em):

        keys = self.tags_by_code.keys()
        keys = sorted(keys)

        # first things first, we save image data, if any
        if self.imageType == "JPEG":
            self.tags_by_code[TAG_JPEG_INTERCHANGE_FORMAT].data[0] = fp.tell()
            fp.write(self.imageData)

        elif self.imageType == "TIFF":
            for idx in range(len(self.imageData)):
                self.tags_by_code[ TAG_STRIPOFFSETS ].data[idx] = fp.tell()
                fp.write( self.imageData[idx] )

        # get endian aware writer
        writer = DataWriter(em)

        # then we do a first pass at the other tags that needs data blocks
        for k in keys:
            tag = self.tags_by_code[k]

            if not TYPES.has_key( tag.type ):
                raise SyntaxError, "unrecognized type"

            # if data is larger than 4 bytes, we must write it NOW!
            # TODO: check tiff docs if any padding is necessary when writing data
            if tag.needsDataBlock():
                if isinstance(tag.data[0], ImageFileDirectory):
                    if (len(tag.data) > 1):
                        # there is more than one directory, that means the tag data will be a list of offsets to each directory
                        # we must save all directories to get their file offsets, and then write all the offsets to get the tag data offset
                        offsets = []
                        for directory in tag.data:
                            offsets.append( directory.save(fp, em) )
                        tag.offset = fp.tell()
                        fp.write( getattr(writer, "%d" % (TYPE_LONG, ))( offsets ) ) # offsets are always unsigned longs
                    else:
                        tag.offset = tag.data[0].save(fp, em)
                else:
                    tag.offset = fp.tell()
                    fp.write( getattr(writer, "%d" % (tag.type, ))( tag.data ) )


        # okay, all directory data has been written, now we right the drectory tags themselves, and we record the current file pointer
        IFDStartOffset = fp.tell()

        fp.write( getattr(writer, "%d" % (TYPE_SHORT, ))( [len(self.tags_by_code)] ) )

        # then we do a second pass for the tags themselves
        for k in keys:
            tag = self.tags_by_code[k]
            fp.write( getattr(writer, "%d" % (TYPE_SHORT, ))( [k, tag.type] ) )
            fp.write( getattr(writer, "%d" % (TYPE_LONG, ))( [len(tag.data) if tag.type != TYPE_ASCII else len(tag.data) + 1] ) ) # we need to account for the added zero for strings

            if tag.needsDataBlock():
                fp.write( getattr(writer, "%d" % (TYPE_LONG, ))( [tag.offset] ) )
            else:
                oldOffset = fp.tell()
                fp.write( getattr(writer, "%d" % (TYPE_LONG, ))( [0] ) )
                whenDoneOffset = fp.tell()
                fp.seek(oldOffset)
                fp.write( getattr(writer, "%d" % (tag.type, ))( tag.data ) )
                fp.seek(whenDoneOffset)

        # done, we return the offset where the start of the directory is
        return IFDStartOffset



    def toString(self, level=0):

        identation = '' if level <= 0 else '  '*level

        s = ''

        s += '%sTAG COUNT: %d\n' % (identation, len(self.tags_by_code))

        if (self.imageType):
            s += '%sIMAGE TYPE: %s\n' % (identation, self.imageType)

        for k in sorted(self.tags_by_code.keys()):
            tag = self.tags_by_code[k]
            s += '%s%s' % (identation, tag.toString())

            if tag.code == TAG_SUBIFD:
                s += '\n'
                for idx in range(len(tag.data)):
                    ifd = tag.data[idx]
                    s += '%s+ SUBIFDs #%d:\n' % (identation, idx)
                    s += ifd.toString(level+1)

            elif tag.code in [TAG_EXIFIFD, TAG_GPS_INFO]:
                s += '\n%s' % (tag.data[0].toString(level+1))

            elif tag.type in [TYPE_ASCII, TYPE_RATIONAL, TYPE_SHORT, TYPE_LONG]:
                s += ": %s\n" % (str(tag.data) if len(tag.data) > 1 else str(tag.data[0]))

            else:
                s += '\n'

        return s


class TiffImage:

    em = EndianMachine(sys.byteorder) # default endian machine is system byteorder

    def __init__(self):
        self.frames = []
        self.header = None

    def load(self, filename):
        """Open a TIFF file and import its structure"""

        fp = open(filename, 'r+')

        # Header
        self.header = fp.read(4)

        if self.header not in PREFIXES:
            raise SyntaxError, "not a TIFF file"

        self.em = EndianMachine("little" if self.header[:2] == II else "big")

        parser = DataParser( self.em )

        # a tiff file always has at least one directory!
        while True:
            # reads the next ifd offset...
            offset = getattr(parser, "%d" % TYPE_LONG)( fp.read(4) )[0]
            # print 'offset', offset

            if offset == 0:
                break

            fp.seek( offset )
            ifd = ImageFileDirectory()
            ifd.load(fp, self.em)
            self.frames.append( ifd )

        fp.close()

        # done, we have a tif structure :)

    def save(self, filename):
        """write the tiff structure as a file"""

        fp = open(filename, 'w+')
        fp.write(self.header)

        writer = DataWriter( self.em )

        for frame in self.frames:
            curFrameOffset = fp.tell()
            fp.write( getattr(writer, "%d" % (TYPE_LONG, ))( [0] ) )
            frameDetailsOffset = frame.save(fp, self.em)
            nextFrameOffset = fp.tell()
            fp.seek(curFrameOffset)
            fp.write(getattr(writer, "%d" % (TYPE_LONG, ))( [frameDetailsOffset] ))
            fp.seek(nextFrameOffset)

        # write the final address to indicate that there is nothing left to read
        fp.write( getattr(writer, "%d" % (TYPE_LONG, ))( [0] ) )
        fp.close()

    def toString(self):
        s = ''
        for idx in range(len(self.frames)):
            ifd = self.frames[idx]
            s += 'IFD #%d\n' % idx
            s += ifd.toString()
        return s
