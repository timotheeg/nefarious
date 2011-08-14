why?
----
.. _KPhotoAlbum: http://www.kphotoalbum.org/

I've looked at several sofftware for image management (and I do NOT mean image retouching). I've settled some years back on KPhotoAlbum_ and I have invested a significant of time with it in filesystem arrangement and photo tagging.

Still, I'm rather old school in trusting only myself as far as 1) backups and 2) knowledge of my pics are concerned. I don't want to rely on any software to know that a nef and a same-named jpeg in some other folder are the actual same image. In the end, there are 2 files (or more) on the file system. To view, I want to see the jpeg, processed version. To edit, I want to start from the raw sensor data. How can I manage that?

I need to have some sort of mapping, If I delete a file purposefully, both files must disappear. During a backup, I must make sure I backup both files.

I longed for a way to have just one file in the filesystem that would solve all my problems. That one file would contain both the raw sensor data and all metadata, the final processed output file (most likely a jpeg I am happy with), and possibly the settings for a given software to go from sensor data to final oputput so I can continue editing where I left off if I needed to.

I considered a zip file, but that would kill the OS/File Manager ability to display the image: a zip file may contain anything.

Then I realized that NEF files follow the TIFF file format specifications; that and the TIFF file format is just a container, with a well-defined, a well-understood tag-based format. Tiff files, and therefore nefs that can hold just about anything. In fact, a NEF file from my Nikon D300S contains:

   1. a small thumbnail of the pic (160x120)
   2. a full size, low quality jpeg preview (4288x2848)
   3. the raw sensor data (4352x2868)
   4. various metadata in standard (exif, gps), and non-standard format (Nikon's "maker notes")

It rapidly became obvious that with a suitable utility, I should be able to replace the low-quality jpeg with whatever I considered to be the final processed look of the raw data.

Lots of procrastination, and some work later, nefarious was finaly born.

I'm only started to use it myself for my own use, but I'd figured I'd release it open source in case it might help someone else.

For now, I'm pretty happy with my setup: in KPhotoalbum, thumbnails and full size view are now displaying the processed jpeg. All the kipi plugin that publish pics to various online services (picasa, facebook) do the same. When I right click on a pic and select "open with rawtherapee", it opens rawtherapee nicely, and since rawtherapee stored the processing parametersnext to the nef, rawtherappe already loads whetever settings I had from my .previous session. If I need to print, I select the pics I want and use dcraw to extract the embedded jpeg.

What is still needed are a few scripts to automatically merge my RAW+FINE pics into one nef right away (I'm working on that); and possibly some automated way to handle editing and saving to automatically replace the jpeg everytime. At the moment, After I edit in rawtherapee, I use nefarious manualy to inject the processed jpeg into the nef again. That's not hard, but less than ideal.
