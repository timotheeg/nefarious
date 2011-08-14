samples
-------

Below is the typical structure printout that nefarious spits when inspecting a nef::

	$ nef-cli -i dsc_2317.nef
	
	IFD #0
	TAG COUNT: 27
	IMAGE TYPE: TIFF
	tag: 254 (NewSubfileType), type: 4 (long), count: 1: 1
	tag: 256 (ImageWidth), type: 4 (long), count: 1: 160
	tag: 257 (ImageLength), type: 4 (long), count: 1: 120
	tag: 258 (BitsPerSample), type: 3 (short), count: 3: [8, 8, 8]
	tag: 259 (Compression), type: 3 (short), count: 1: 1
	tag: 262 (PhotometricInterpretation), type: 3 (short), count: 1: 2
	tag: 271 (Make), type: 2 (ascii), count: 17: NIKON CORPORATION
	tag: 272 (Model), type: 2 (ascii), count: 11: NIKON D300S
	tag: 273 (StripOffsets), type: 4 (long), count: 1: 111424
	tag: 274 (Orientation), type: 3 (short), count: 1: 1
	tag: 277 (SamplesPerPixel), type: 3 (short), count: 1: 3
	tag: 278 (RowsPerStrip), type: 4 (long), count: 1: 120
	tag: 279 (StripByteCounts), type: 4 (long), count: 1: 57600
	tag: 282 (XResolution), type: 5 (rational), count: 1: [300, 1]
	tag: 283 (YResolution), type: 5 (rational), count: 1: [300, 1]
	tag: 284 (PlanarConfiguration), type: 3 (short), count: 1: 1
	tag: 296 (ResolutionUnit), type: 3 (short), count: 1: 2
	tag: 305 (Software), type: 2 (ascii), count: 9: Ver.1.01 
	tag: 306 (DateTime), type: 2 (ascii), count: 19: 2011:02:27 17:03:27
	tag: 315 (Artist), type: 2 (ascii), count: 36:                                     
	tag: 330 (SubIFD), type: 4 (long), count: 2
	+ SUBIFDs #0:
	  TAG COUNT: 8
	  IMAGE TYPE: JPEG
	  tag: 254 (NewSubfileType), type: 4 (long), count: 1: 1
	  tag: 259 (Compression), type: 3 (short), count: 1: 6
	  tag: 282 (XResolution), type: 5 (rational), count: 1: [300, 1]
	  tag: 283 (YResolution), type: 5 (rational), count: 1: [300, 1]
	  tag: 296 (ResolutionUnit), type: 3 (short), count: 1: 2
	  tag: 513 (JPEGInterchangeFormat), type: 4 (long), count: 1: 169408
	  tag: 514 (JPEGInterchangeFormatLength), type: 4 (long), count: 1: 1528209
	  tag: 531 (YCbCrPositioning), type: 3 (short), count: 1: 2
	+ SUBIFDs #1:
	  TAG COUNT: 17
	  IMAGE TYPE: TIFF
	  tag: 254 (NewSubfileType), type: 4 (long), count: 1: 0
	  tag: 256 (ImageWidth), type: 4 (long), count: 1: 4352
	  tag: 257 (ImageLength), type: 4 (long), count: 1: 2868
	  tag: 258 (BitsPerSample), type: 3 (short), count: 1: 14
	  tag: 259 (Compression), type: 3 (short), count: 1: 34713
	  tag: 262 (PhotometricInterpretation), type: 3 (short), count: 1: 32803
	  tag: 273 (StripOffsets), type: 4 (long), count: 1: 1697632
	  tag: 277 (SamplesPerPixel), type: 3 (short), count: 1: 1
	  tag: 278 (RowsPerStrip), type: 4 (long), count: 1: 2868
	  tag: 279 (StripByteCounts), type: 4 (long), count: 1: 14902291
	  tag: 282 (XResolution), type: 5 (rational), count: 1: [300, 1]
	  tag: 283 (YResolution), type: 5 (rational), count: 1: [300, 1]
	  tag: 284 (PlanarConfiguration), type: 3 (short), count: 1: 1
	  tag: 296 (ResolutionUnit), type: 3 (short), count: 1: 2
	  tag: 33421 (CFARepeatPattern), type: 3 (short), count: 2: [2, 2]
	  tag: 33422 (CFAPattern), type: 1 (byte), count: 4
	  tag: 37399 (SensingMethod), type: 3 (short), count: 1: 2
	tag: 532 (ReferenceBlackWhite), type: 5 (rational), count: 6: [[0, 1], [255, 1], [0, 1], [255, 1], [0, 1], [255, 1]]
	tag: 33432 (Copyright), type: 2 (ascii), count: 54:                                                       
	tag: 34665 (ExifIFD), type: 4 (long), count: 1
	  TAG COUNT: 32
	  tag: 33434 (ExposureTime), type: 5 (rational), count: 1: [10, 2500]
	  tag: 33437 (FNumber), type: 5 (rational), count: 1: [71, 10]
	  tag: 34850 (ExposureProgram), type: 3 (short), count: 1: 4
	  tag: 34855 (IsoSpeed), type: 3 (short), count: 1: 400
	  tag: 36867 (DateTimeOriginal), type: 2 (ascii), count: 19: 2011:02:27 17:03:27
	  tag: 36868 (DateTimeDigitized), type: 2 (ascii), count: 19: 2011:02:27 17:03:27
	  tag: 37380 (ExposureBiasValue), type: 10 (signed rational), count: 1
	  tag: 37381 (MaxApertureValue), type: 5 (rational), count: 1: [36, 10]
	  tag: 37383 (MeteringMode), type: 3 (short), count: 1: 5
	  tag: 37384 (LightSource), type: 3 (short), count: 1: 0
	  tag: 37385 (Flash), type: 3 (short), count: 1: 0
	  tag: 37386 (FocalLength), type: 5 (rational), count: 1: [180, 10]
	  tag: 37500 (MakerNote), type: 7 (undefined), count: 110048
	  tag: 37510 (UserComment), type: 7 (undefined), count: 44
	  tag: 37520 (SubsecTime), type: 2 (ascii), count: 2: 00
	  tag: 37521 (SubsecTimeOriginal), type: 2 (ascii), count: 2: 00
	  tag: 37522 (SubsecTimeDigitized), type: 2 (ascii), count: 2: 00
	  tag: 41495 (SensingMethod), type: 3 (short), count: 1: 2
	  tag: 41728 (FileSource), type: 7 (undefined), count: 1
	  tag: 41729 (SceneType), type: 7 (undefined), count: 1
	  tag: 41730 (CFAPattern), type: 7 (undefined), count: 8
	  tag: 41985 (CustomRendered), type: 3 (short), count: 1: 0
	  tag: 41986 (ExposureMode), type: 3 (short), count: 1: 0
	  tag: 41987 (WhiteBalance), type: 3 (short), count: 1: 0
	  tag: 41988 (DigitalZoomRatio), type: 5 (rational), count: 1: [1, 1]
	  tag: 41989 (FocalLengthIn35mmFilm), type: 3 (short), count: 1: 27
	  tag: 41990 (SceneCaptureType), type: 3 (short), count: 1: 0
	  tag: 41991 (GainControl), type: 3 (short), count: 1: 1
	  tag: 41992 (Contrast), type: 3 (short), count: 1: 0
	  tag: 41993 (Saturation), type: 3 (short), count: 1: 0
	  tag: 41994 (Sharpness), type: 3 (short), count: 1: 0
	  tag: 41996 (SubjectDistanceRange), type: 3 (short), count: 1: 0
	tag: 34853 (GPSInfo), type: 4 (long), count: 1
	  TAG COUNT: 11
	  tag: 0 (GPSVersionID), type: 1 (byte), count: 4
	  tag: 1 (GPSLatitudeRef), type: 2 (ascii), count: 1: N
	  tag: 2 (GPSLatitude), type: 5 (rational), count: 3: [[1, 1], [192042, 10000], [0, 1]]
	  tag: 3 (GPSLongitudeRef), type: 2 (ascii), count: 1: E
	  tag: 4 (GPSLongitude), type: 5 (rational), count: 3: [[103, 1], [517791, 10000], [0, 1]]
	  tag: 5 (GPSAltitudeRef), type: 1 (byte), count: 1
	  tag: 6 (GPSAltitude), type: 5 (rational), count: 1: [110, 1]
	  tag: 7 (GPSTimeStamp), type: 5 (rational), count: 3: [[9, 1], [3, 1], [4231, 100]]
	  tag: 8 (GPSSatellites), type: 2 (ascii), count: 2: 09
	  tag: 18 (GPSMapDatum), type: 2 (ascii), count: 9:          
	  tag: 29 (GPSDateStamp), type: 2 (ascii), count: 10: 2011:02:27
	tag: 36867 (DateTimeOriginal), type: 2 (ascii), count: 19: 2011:02:27 17:03:27
	tag: 37398 (TIFF/EPStandardID), type: 1 (byte), count: 4
	
