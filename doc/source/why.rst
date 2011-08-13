Why
---
.. _KPhotoAlbum: http://www.kphotoalbum.org/

I've looked at several sofftware for image management (and I do NOT mean image retouching). I've settled some years back on KPhotoalbum_. and I have invested a significant of time with it in filesystem arrangement and photo tagging.

Still, I'm rather old school in trusting only myself as far as 1) backups and 2) knowledge of my pics are concerned. I don't want to rely on any software to know that a nef and a same-named jpeg in some other folder are the actual same image. In the end, there are 2 files (or more) on the file system. To view, I want to see the jpeg, processed version. To edit, I want to start from the raw sensor data. How can I manage that?

I need to have some sort of mapping, If I delete a file purposefully, both files must disappear. During a backup, I must make sure I backup both files.

I longed for a way to have just one file in the filesystem that would solve all my problems. That one file would contain both the raw sensor data and all metadata, the final processed output file (most likely a jpeg I am happy with), and possibly the settings for a given software to go from sensor data to final oputput so I can continue editing where I left off.

I considered a zip file, but that would kill the os ability to display the image: a zip file may contain anything.

Then I realized that NEF files are just TIFF files; and the TIFF file format is just a container, with a well-defined, a well-understood tag-based format, that can hold just about anything. In fact, a NEF file from my Nikon D300S contains:

#. a small thumbnail of the pic
#. a full size, low quality jpeg preview
#. the raw sensor data
#. various metadata in standard (exif), and non-standard format (nikon's "maker notes")

It rapidly became obvious that with a suitable utility, I should be able to replace the low -quality jpeg with whatever I considered to be the final processed look of the raw data.

Lots of procrastination later, nefarious was finaly born.

