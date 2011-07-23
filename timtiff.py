# -*- coding: utf-8 -*-
# tiff minimalistic parser
# (c)2010 Timothee Groleau
# with code taken from PIL

import array, string, sys

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

#for each type, determine the size of the data unit, and a string representation of the type
TYPES = {
   TYPE_BYTE:      (1,   "byte"),
   TYPE_ASCII:     (1,   "ascii"),
   TYPE_SHORT:     (2,   "short"),
   TYPE_LONG:      (4,   "long"),
   TYPE_RATIONAL:  (2*4, "rational"),
   TYPE_SBYTE:     (1,   "signed byte"),
   TYPE_UNDEFINED: (1,   "undefined"),
   TYPE_SSHORT:    (2,   "signed short"),
   TYPE_SLONG:     (4,   "signed long"),
   TYPE_SRATIONAL: (2*4, "signed rational"),
   TYPE_FLOAT:     (4,   "float"),
   TYPE_DOUBLE:    (8,   "double")
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

   def il16(self, c,o=0):
      return ord(c[o]) + (ord(c[o+1])<<8)
   def il32(self, c,o=0):
      return ord(c[o]) + (ord(c[o+1])<<8) + (ord(c[o+2])<<16) + (ord(c[o+3])<<24)
   def ol16(self, i):
      return chr(i&255) + chr(i>>8&255)
   def ol32(self, i):
      return chr(i&255) + chr(i>>8&255) + chr(i>>16&255) + chr(i>>24&255)

   def ib16(self, c,o=0):
      return ord(c[o+1]) + (ord(c[o])<<8)
   def ib32(self, c,o=0):
      return ord(c[o+3]) + (ord(c[o+2])<<8) + (ord(c[o+1])<<16) + (ord(c[o])<<24)
   def ob16(self, i):
      return chr(i>>8&255) + chr(i&255)
   def ob32(self, i):
      return chr(i>>24&255) + chr(i>>16&255) + chr(i>>8&255) + chr(i&255)

   def __init__(self, mode=sys.byteorder):
      self.mode = mode
      
      if mode == "little":
         self.i16, self.i32 = self.il16, self.il32
         self.o16, self.o32 = self.ol16, self.ol32
      else:
         self.i16, self.i32 = self.ib16, self.ib32
         self.o16, self.o32 = self.ob16, self.ob32


class DataParser:
   def load_byte(self, data):
      l = []
      for i in range(len(data)):
         l.append(ord(data[i]))
      return tuple(l)

   def load_string(self, data):
      if data[-1:] == '\0':
         data = data[:-1]
      return data

   def load_short(self, data):
      l = []
      for i in range(0, len(data), 2):
         l.append(self.em.i16(data, i))
      return tuple(l)

   def load_long(self, data):
      l = []
      for i in range(0, len(data), 4):
         l.append(self.em.i32(data, i))
      return tuple(l)

   def load_rational(self, data):
      l = []
      for i in range(0, len(data), 8):
         l.append((self.em.i32(data, i), self.em.i32(data, i+4)))
      return tuple(l)

   def load_float(self, data):
      a = array.array("f", data)
      if self.prefix != native_prefix:
         a.byteswap()
      return tuple(a)

   def load_double(self, data):
      a = array.array("d", data)
      if self.prefix != native_prefix:
         a.byteswap()
      return tuple(a)

   def load_undefined(self, data):
      # Untyped data
      return data

   def __init__(self, em):
      self.em = em;

setattr(DataParser, "%d" % (TYPE_BYTE, ),      DataParser.load_byte)
setattr(DataParser, "%d" % (TYPE_ASCII, ),     DataParser.load_string)
setattr(DataParser, "%d" % (TYPE_SHORT, ),     DataParser.load_short)
setattr(DataParser, "%d" % (TYPE_LONG, ),      DataParser.load_long)
setattr(DataParser, "%d" % (TYPE_RATIONAL, ),  DataParser.load_rational)
setattr(DataParser, "%d" % (TYPE_SBYTE, ),     DataParser.load_byte)
setattr(DataParser, "%d" % (TYPE_UNDEFINED, ), DataParser.load_undefined)
setattr(DataParser, "%d" % (TYPE_SSHORT, ),    DataParser.load_short)
setattr(DataParser, "%d" % (TYPE_SLONG, ),     DataParser.load_long)
setattr(DataParser, "%d" % (TYPE_SRATIONAL, ), DataParser.load_rational)
setattr(DataParser, "%d" % (TYPE_FLOAT, ),     DataParser.load_float)
setattr(DataParser, "%d" % (TYPE_DOUBLE, ),    DataParser.load_double)

class DataWriter:
   def __init_(self, em):
      self.em = em
      
   #TODO: implementation



class Tag:
   def __init__(self, code=0, type=0, data=0, offset=None):
      self.code = code
      self.type = type
      self.data = data
      self.offset = offset
      
   def toString(self):
      return "tag: %d (%s), type: %d (%s), count: %d" % (
              self.code
            , TAGS[self.code] if (TAGS.has_key(self.code)) else "unknown"
            , self.type
            , TYPES[self.type][1]
            , len(self.data)
         )



class ImageFileDirectory:
   def __init__(self):
      self.tags = []
      self.tags_by_code = {}
      self.ifds = None

      self.imageType = None
      self.imageData = None

      
   def load(self, fp, em, level=0):
      "reads an ifd directory, file pointer must already be at the right location!!"
      
      i16 = em.i16
      i32 = em.i32
      
      #instanciate a data parser
      parser = DataParser( em )
      
      # read tag count
      tagcount = i16( fp.read(2) )
      
      # read all tags
      for i in range(tagcount):
         
         tag = fp.read( 12 )
         tagCode, typ, count, rawdata = i16(tag), i16(tag, 2), i32(tag, 4), tag[8:]

         unitSize, typeName = TYPES[typ]
         size = count * unitSize
         
         if size <= 4:
               rawdata = rawdata[:size]
         else:
            curOffset = fp.tell()
            fp.seek( i32(rawdata) )
            rawdata = fp.read( size )
            fp.seek( curOffset )
            
         if len(rawdata) != size:
            raise IOError, "not enough data"
            
         if TYPES.has_key( typ ):
            data = getattr(parser, "%d" % (typ, ))( rawdata )
         else:
            data = rawdata

         if tagCode in [TAG_SUBIFD, TAG_EXIFIFD, TAG_GPS_INFO]:
            # read all sub ifds
            oldOffset = fp.tell()
            ifds = []
            for offset in data:
               fp.seek( offset )
               subIfd = ImageFileDirectory()
               subIfd.load(fp, em, level+1)
               ifds.append( subIfd )
            fp.seek(oldOffset)
            tag = Tag(tagCode, typ, ifds)
   
         else:
            tag = Tag(tagCode, typ, data)

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
            
            self.imageType="TIFF"
            self.imageData = []
            for i in range(len(self.tags_by_code[ TAG_STRIPOFFSETS ].data)):
               fp.seek( self.tags_by_code[ TAG_STRIPOFFSETS ].data[i] )
               self.imageData.append( fp.read( self.tags_by_code[ TAG_STRIPBYTECOUNTS ].data[i] ) )
      
      #image data has been read, now return to correct offset before passing the hand back to caller...
      fp.seek( oldOffset )


   def save(self, fp, em):
      keys = self.tags_by_code.keys()
      keys.sorted()
      for k in keys:
         pass
      #first pass, save all data that needs to be offseted...
      #secondpass, save directory itself
      #success!

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
      ifh = fp.read(4)
      
      if ifh not in PREFIXES:
         raise SyntaxError, "not a TIFF file"

      print "Opening %s - byte order header: %s" % (filename, ifh[:2])
      
      em = EndianMachine("little" if ifh[:2] == II else "big")

      # a tiff file always has at least one directory!
      idx = 0
      while True:
         # reads the next ifd offset...
         offset = em.i32( fp.read(4) )
         
         if offset == 0:
            break

         fp.seek( offset )
         ifd = ImageFileDirectory();
         ifd.load(fp, em)
         self.frames.append(ifd)

         idx += 1
      
      fp.close()
      
      # done, we have a tif structure :)
      
   def save(self, filename):
      "write the tiff structure as a file"
      
      fp.open(filename, 'w+')
      # write header
      # save offset to write start offset
      # iniate write of ifd0
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
   
   print tiff.toString()

   # assume this is a nef file...
   fp = open("%s.thumb.jpg" % sys.argv[1], 'w')
   fp.write( tiff.frames[0].ifds[0].imageData )
   fp.close()

   # now injects jpeg and process data into ifd#0subifd#0
