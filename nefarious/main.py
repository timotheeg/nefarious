import optparse
# import copy
import nefarious


def confirmSave(tiff, input_file, output_file, force=False):

    if output_file != input_file:
        tiff.save(output_file)
        return 0

    else:
        msg = "This will overwrite your input nef. Are you sure? (y/n) "
        if force:
            print "%s%s" % (msg, 'y')
            overwrite = True
        else:
            overwrite = raw_input(msg).strip().lower() == 'y'

        if overwrite:
            tiff.save(input_file)
            return 0
        else:
            return 1



def main():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--input-file",   dest="input",   help="Specify the input nef file")
    parser.add_option("-o", "--output-file",  dest="output",  help="Specify the file to write to")
    parser.add_option("-p", "--preview-jepg", dest="preview", help="Specify the jpeg file to use as nef preview")
    parser.add_option("-y", "--yes",          dest="yes",     help="Automatically answer yes when prompted to overwrite input", action="store_true", default=False)

    parser.usage = "nef-cli -i in.nef [-p preview.jpg] [-o out.nef]"
    opts, _ = parser.parse_args()


    if not opts.input:
        parser.error("please specify input file with the -i option")

    tiff = nefarious.core.TiffImage()
    tiff.load(opts.input)

    if opts.preview:
        # make a backup of the original preview image as a new ifd in the same nef
        # need some smarter logic here and options here...
        # if len(tiff.frames[0].ifds) < 3:
        #    tiff.frames[0].ifds.append( copy.deepcopy(tiff.frames[0].ifds[0]) )

        f = open(opts.preview)
        jpeg = f.read()
        f.close()

        tiff.frames[0].ifds[0].imageType = "JPEG"
        tiff.frames[0].ifds[0].imageData = jpeg
        tiff.frames[0].ifds[0].tags_by_code[nefarious.constants.TAG_JPEG_INTERCHANGE_FORMAT_LENGTH].data[0] = len(jpeg)

        if opts.output:
            return confirmSave(tiff, opts.input, opts.output, opts.yes)
        else:
            return confirmSave(tiff, opts.input, opts.input, opts.yes)


    elif opts.output:
        return confirmSave(tiff, opts.input, opts.output, opts.yes)

    else:
        print tiff.toString()
        return 0


if __name__ == "__main__":
    main()
