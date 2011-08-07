# -*- coding: utf-8 -*-
# tiff minimalistic parser
# (c)2010 Timothee Groleau
# with code taken from PIL

import array, string, sys, copy, math, struct

#for debugging!
from pprint import pprint


II = "II" # little-endian (intel-style)
MM = "MM" # big-endian (motorola-style)

PREFIXES = ["MM\000\052", "II\052\000", "II\xBC\000"]

TYPE_BYTE      = 1
TYPE_ASCII     = 2
TYPE_SHORT     = 3
TYPE_LONG      = 4
TYPE_RATIONAL  = 5
TYPE_SBYTE     = 6
TYPE_UNDEFINED = 7
TYPE_SSHORT    = 8
TYPE_SLONG     = 9
TYPE_SRATIONAL = 10
TYPE_FLOAT     = 11
TYPE_DOUBLE    = 12

#for each type, determine the size of the data unit, the associated python struct letter, and a string representation of the type
TYPES = {
   TYPE_BYTE:      (1,   "B",  "byte"),
   TYPE_ASCII:     (1,   "c",  "ascii"),
   TYPE_SHORT:     (2,   "H",  "short"),
   TYPE_LONG:      (4,   "L",  "long"),
   TYPE_RATIONAL:  (2*4, "LL", "rational"),
   TYPE_SBYTE:     (1,   "b",  "signed byte"),
   TYPE_UNDEFINED: (1,   "c",  "undefined"),
   TYPE_SSHORT:    (2,   "h",  "signed short"),
   TYPE_SLONG:     (4,   "l",  "signed long"),
   TYPE_SRATIONAL: (2*4, "ll", "signed rational"),
   TYPE_FLOAT:     (4,   "f",  "float"),
   TYPE_DOUBLE:    (8,   "d",  "double")
}

#known tags
TAG_SUBIFD = 330
TAG_IMAGEWIDTH = 256
TAG_IMAGELENGTH = 257
TAG_BITSPERSAMPLE = 258
TAG_COMPRESSION = 259
TAG_PHOTOMETRIC_INTERPRETATION = 262
TAG_FILLORDER = 266
TAG_IMAGEDESCRIPTION = 270
TAG_STRIPOFFSETS = 273
TAG_SAMPLESPERPIXEL = 277
TAG_ROWSPERSTRIP = 278
TAG_STRIPBYTECOUNTS = 279
TAG_X_RESOLUTION = 282
TAG_Y_RESOLUTION = 283
TAG_PLANAR_CONFIGURATION = 284
TAG_RESOLUTION_UNIT = 296
TAG_SOFTWARE = 305
TAG_DATE_TIME = 306
TAG_ARTIST = 315
TAG_PREDICTOR = 317
TAG_COLORMAP = 320
TAG_TILEOFFSETS = 324
TAG_EXTRASAMPLES = 338
TAG_SAMPLEFORMAT = 339
TAG_JPEGTABLES = 347
TAG_COPYRIGHT = 33432
TAG_IPTC_NAA_CHUNK = 33723 # newsphoto properties
TAG_PHOTOSHOP_CHUNK = 34377 # photoshop properties
TAG_ICCPROFILE = 34675
TAG_EXIFIFD = 34665
TAG_XMP = 700
TAG_JPEG_INTERCHANGE_FORMAT = 513
TAG_JPEG_INTERCHANGE_FORMAT_LENGTH = 514
TAG_GPS_INFO = 34853;


TAGS = {

    254: "NewSubfileType",
    255: "SubfileType",
    256: "ImageWidth",
    257: "ImageLength",
    258: "BitsPerSample",

    259: "Compression",
    (259, 1): "Uncompressed",
    (259, 2): "CCITT 1d",
    (259, 3): "Group 3 Fax",
    (259, 4): "Group 4 Fax",
    (259, 5): "LZW",
    (259, 6): "JPEG",
    (259, 32773): "PackBits",

    262: "PhotometricInterpretation",
    (262, 0): "WhiteIsZero",
    (262, 1): "BlackIsZero",
    (262, 2): "RGB",
    (262, 3): "RGB Palette",
    (262, 4): "Transparency Mask",
    (262, 5): "CMYK",
    (262, 6): "YCbCr",
    (262, 8): "CieLAB",
    (262, 32803): "CFA", # TIFF/EP, Adobe DNG
    (262, 32892): "LinearRaw", # Adobe DNG

    263: "Thresholding",
    264: "CellWidth",
    265: "CellHeight",
    266: "FillOrder",
    269: "DocumentName",

    270: "ImageDescription",
    271: "Make",
    272: "Model",
    273: "StripOffsets",
    274: "Orientation",
    277: "SamplesPerPixel",
    278: "RowsPerStrip",
    279: "StripByteCounts",

    280: "MinSampleValue",
    281: "MaxSampleValue",
    282: "XResolution",
    283: "YResolution",
    284: "PlanarConfiguration",
    (284, 1): "Contigous",
    (284, 2): "Separate",

    285: "PageName",
    286: "XPosition",
    287: "YPosition",
    288: "FreeOffsets",
    289: "FreeByteCounts",

    290: "GrayResponseUnit",
    291: "GrayResponseCurve",
    292: "T4Options",
    293: "T6Options",
    296: "ResolutionUnit",
    297: "PageNumber",

    301: "TransferFunction",
    305: "Software",
    306: "DateTime",

    315: "Artist",
    316: "HostComputer",
    317: "Predictor",
    318: "WhitePoint",
    319: "PrimaryChromaticies",

    320: "ColorMap",
    321: "HalftoneHints",
    322: "TileWidth",
    323: "TileLength",
    324: "TileOffsets",
    325: "TileByteCounts",

    330: "SubIFD",

    332: "InkSet",
    333: "InkNames",
    334: "NumberOfInks",
    336: "DotRange",
    337: "TargetPrinter",
    338: "ExtraSamples",
    339: "SampleFormat",

    340: "SMinSampleValue",
    341: "SMaxSampleValue",
    342: "TransferRange",

    347: "JPEGTables",

    # obsolete JPEG tags
    512: "JPEGProc",
    513: "JPEGInterchangeFormat",
    514: "JPEGInterchangeFormatLength",
    515: "JPEGRestartInterval",
    517: "JPEGLosslessPredictors",
    518: "JPEGPointTransforms",
    519: "JPEGQTables",
    520: "JPEGDCTables",
    521: "JPEGACTables",

    529: "YCbCrCoefficients",
    530: "YCbCrSubSampling",
    531: "YCbCrPositioning",
    532: "ReferenceBlackWhite",

    # XMP
    700: "XMP",

    33421: "CFARepeatPattern",
    33422: "CFAPattern",
    33432: "Copyright",

    # Exif
    33434: "ExposureTime",
    33437: "FNumber",
    34850: "ExposureProgram",
    34852: "SpectralSensitivity",
    34855: "IsoSpeed",
    34856: "OECF",
    36864: "ExifVersion",
    36867: "DateTimeOriginal",
    36868: "DateTimeDigitized",
    37121: "ComponentsConfiguration",
    37122: "CompressedBitsPerPixel",
    37377: "ShutterSpeedValue",
    37378: "ApertureValue",
    37379: "BrightnessValue",
    37380: "ExposureBiasValue",
    37381: "MaxApertureValue",
    37383: "MeteringMode",
    37384: "LightSource",
    37385: "Flash",
    37386: "FocalLength",
    37396: "SubjectArea",
    37398: "TIFF/EPStandardID",
    37399: "SensingMethod",
    37500: "MakerNote",
    37510: "UserComment",
    37520: "SubsecTime",
    37521: "SubsecTimeOriginal",
    37522: "SubsecTimeDigitized",
    40960: "FlashpixVersion",
    40961: "ColorSpace",
    40962: "PixelXDimension",
    40963: "PixelYDimension",
    40964: "RelatedSoundFile",
    41483: "FlashEnergy",
    41484: "SpatialFrequencyResponse",
    41486: "FocalPlaneXResolution",
    41487: "FocalPlaneYResolution",
    41488: "FocalPlaneResolutionUnit",
    41492: "SubjectLocation",
    41493: "ExposureIndex",
    41495: "SensingMethod",
    41728: "FileSource",
    41729: "SceneType",
    41730: "CFAPattern",
    41985: "CustomRendered",
    41986: "ExposureMode",
    41987: "WhiteBalance",
    41988: "DigitalZoomRatio",
    41989: "FocalLengthIn35mmFilm",
    41990: "SceneCaptureType",
    41991: "GainControl",
    41992: "Contrast",
    41993: "Saturation",
    41994: "Sharpness",
    41995: "DeviceSettingDescription",
    41996: "SubjectDistanceRange",
    42016: "ImageUniqueID",

    34853: "GPSInfo",
    (34853, 0): "GPSVersionID",
    (34853, 1): "GPSLatitudeRef",
    (34853, 2): "GPSLatitude",
    (34853, 3): "GPSLongitudeRef",
    (34853, 4): "GPSLongitude",
    (34853, 5): "GPSAltitudeRef",
    (34853, 6): "GPSAltitude",
    (34853, 7): "GPSTimeStamp",
    (34853, 8): "GPSSatellites",
    (34853, 18): "GPSMapDatum",
    (34853, 29): "GPSDateStamp",

    # various extensions (should check specs for "official" names)
    33723: "IptcNaaInfo",
    34377: "PhotoshopInfo",

    # Exif IFD
    34665: "ExifIFD",

    # ICC Profile
    34675: "ICCProfile",

    # Adobe DNG
    50706: "DNGVersion",
    50707: "DNGBackwardVersion",
    50708: "UniqueCameraModel",
    50709: "LocalizedCameraModel",
    50710: "CFAPlaneColor",
    50711: "CFALayout",
    50712: "LinearizationTable",
    50713: "BlackLevelRepeatDim",
    50714: "BlackLevel",
    50715: "BlackLevelDeltaH",
    50716: "BlackLevelDeltaV",
    50717: "WhiteLevel",
    50718: "DefaultScale",
    50741: "BestQualityScale",
    50719: "DefaultCropOrigin",
    50720: "DefaultCropSize",
    50778: "CalibrationIlluminant1",
    50779: "CalibrationIlluminant2",
    50721: "ColorMatrix1",
    50722: "ColorMatrix2",
    50723: "CameraCalibration1",
    50724: "CameraCalibration2",
    50725: "ReductionMatrix1",
    50726: "ReductionMatrix2",
    50727: "AnalogBalance",
    50728: "AsShotNeutral",
    50729: "AsShotWhiteXY",
    50730: "BaselineExposure",
    50731: "BaselineNoise",
    50732: "BaselineSharpness",
    50733: "BayerGreenSplit",
    50734: "LinearResponseLimit",
    50735: "CameraSerialNumber",
    50736: "LensInfo",
    50737: "ChromaBlurRadius",
    50738: "AntiAliasStrength",
    50740: "DNGPrivateData",
    50741: "MakerNoteSafety",
}



class EndianMachine:

   def getPrefix(self):
      return "<" if self.mode == "little" else ">"

   def isOrder(self, mode):
      return self.mode == mode

   def __init__(self, mode=sys.byteorder):
      self.mode = mode


class DataParser:
   def __init__(self, em):
      self.em = em;
      
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
      unitSize, strucPattern, typeName = TYPES[zeType]

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
      s = ''
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
      unitSize, structPattern, typeName = TYPES[self.type]
      return unitSize * len(self.data)
      
   def needsDataBlock(self):
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
      "reads an ifd directory, file pointer must already be at the right location!!"
      
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
         
         unitSize, strucPattern, typeName = TYPES[zeType]   
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
      
      #image data has been read, now return to correct offset before passing the hand back to caller...
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
      
      #get endian aware writer
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
      
      # done, we return the offset where the start of the directory 
      return IFDStartOffset;
      
      

   def toString(self, level=0):

      identation = '' if level <= 0 else '  '*level
      
      s = '';
      
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
         
      return s;
         

class TiffImage:

   em = EndianMachine(sys.byteorder) # default endian machine is system byteorder
   
   def __init__(self):
      self.frames = []
      
   def load(self, filename):
      "Open a TIFF file and import its structure"
      
      fp = open(filename, 'r+')

      # Header
      self.header = fp.read(4)
      
      if self.header not in PREFIXES:
         raise SyntaxError, "not a TIFF file"

      self.em = EndianMachine("little" if self.header[:2] == II else "big")
      
      parser = DataParser( self.em )

      # a tiff file always has at least one directory!
      idx = 0
      while True:
         # reads the next ifd offset...
         offset = getattr(parser, "%d" % TYPE_LONG)( fp.read(4) )[0]
         # print 'offset', offset
         
         if offset == 0:
            break

         fp.seek( offset )
         ifd = ImageFileDirectory();
         ifd.load(fp, self.em)
         self.frames.append( ifd )

         idx += 1
      
      fp.close()
      
      # done, we have a tif structure :)
      
   def save(self, filename):
      "write the tiff structure as a file"
      
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
      fp.close
      
   def toString(self):
      s = ''
      for idx in range(len(self.frames)):
         ifd = self.frames[idx]
         s += 'IFD #%d\n' % idx
         s += ifd.toString()
      return s


if __name__ == "__main__":
   
   tiff = TiffImage()
   tiff.load(sys.argv[1])

   if (len(sys.argv) >= 4 and sys.argv[2] == '-r'):
      
      if len(tiff.frames[0].ifds) < 3:
         tiff.frames[0].ifds.append( copy.deepcopy(tiff.frames[0].ifds[0]) )
      
      f = open(sys.argv[3])
      jpeg = f.read()
      f.close()
      
      tiff.frames[0].ifds[0].imageType = "JPEG"
      tiff.frames[0].ifds[0].imageData = jpeg
      tiff.frames[0].ifds[0].tags_by_code[TAG_JPEG_INTERCHANGE_FORMAT_LENGTH].data[0] = len(jpeg)
      
      tiff.save(sys.argv[4])

   else:
      print tiff.toString()
      

   #tiff.save(sys.argv[1] + ".tiff")
   
   #tiff2 = TiffImage()
   #tiff2.load(sys.argv[1] + ".tiff")
   #print tiff2.toString()
   

   # assume this is a nef file...
   # fp = open("%s.thumb.jpg" % sys.argv[1], 'w')
   # fp.write( tiff.frames[0].ifds[0].imageData )
   # fp.close()

   # now injects jpeg and process data into ifd#0subifd#0
