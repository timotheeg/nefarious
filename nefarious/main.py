import optparse
import copy
import nefarious

def main():   
    parser = optparse.OptionParser()
    
    parser.add_option("-f","--input-file",dest="input")
    parser.add_option("-t","--thumbnail", dest="thumb")
    parser.add_option("-i","--info",dest="info", action="store_true")
    parser.usage = "nef-cli -f filename.nef -t thumb.jpg filename.tiff"
    opts, args = parser.parse_args()
    
    tiff = nefarious.core.TiffImage()
    
    if not opts.input:
        parser.error("please specify input file with the -f option")
    if opts.input and (not opts.thumb or not len(args)==1) and not opts.info:
        parser.error("please specify thumbnail image (-t) and output filename")
   
    tiff.load(opts.input)
    if opts.info:
        print tiff.toString()
    else:
        if len(tiff.frames[0].ifds) < 3:
            tiff.frames[0].ifds.append( copy.deepcopy(tiff.frames[0].ifds[0]) )
            
            f = open(opts.thumb)
            jpeg = f.read()
            f.close()
            
            tiff.frames[0].ifds[0].imageType = "JPEG"
            tiff.frames[0].ifds[0].imageData = jpeg
            tiff.frames[0].ifds[0].tags_by_code[nefarious.constants.TAG_JPEG_INTERCHANGE_FORMAT_LENGTH].data[0] = len(jpeg)
            
            tiff.save(args[0])
    
    
    #tiff.save(sys.argv[1] + ".tiff")
    
    #tiff2 = TiffImage()
    #tiff2.load(sys.argv[1] + ".tiff")
    #print tiff2.toString()
    
    
    # assume this is a nef file...
    # fp = open("%s.thumb.jpg" % sys.argv[1], 'w')
    # fp.write( tiff.frames[0].ifds[0].imageData )
    # fp.close()
    
    # now injects jpeg and process data into ifd#0subifd#0
if __name__ == "__main__":
    main()