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

# tags we care about about in nefarious
TAG_SUBIFD = 330
TAG_STRIPOFFSETS = 273
TAG_STRIPBYTECOUNTS = 279
TAG_EXIFIFD = 34665
TAG_JPEG_INTERCHANGE_FORMAT = 513
TAG_JPEG_INTERCHANGE_FORMAT_LENGTH = 514
TAG_GPS_INFO = 34853


# Waaaay more tags than we care about :p, but copied from PIL for completeness, with some additions (GPS)
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
