FAQ
---

.. _tiff file format specifications: http://partners.adobe.com/asn/developer/PDFS/TN/TIFF6.pdf
.. _dcraw: http://www.cybercom.net/~dcoffin/dcraw/
.. _rawtherapee: http://www.rawtherapee.com/
.. _nefarious license: https://raw.github.com/timotheeg/nefarious/master/license/license_nefarious.txt
.. _PIL license: https://raw.github.com/timotheeg/nefarious/master/license/license_PIL.txt

Wait... did you say you were manipulating raw files? That's the greatest sin of digital photography!!!! Haven't you read the memo? NO program should ever touch a raw file!! You should rot in hell, along with all your descendants for 10 generations.
    yes. yes. thank you.

    Raw NEF files follow the `tiff file format specifications`_, which means they're reasonably easy to parse and understand. A NEF file basically consists of a bunch of tags and directories, themselves containing more tags and data. What is really precious in that NEF file is the camera's sensor data, which sits in one of the directory. nefarious doesn't alter that in any way.

    Anything else is fair game: change the date, change/add gps location, **update the preview jpeg**, whatever. The aim of nefarious is to spit out nef files in such a way that no nef reader (e.g. dcraw_), and hopefully not even a nef reader from Nikon itself, would realize the nef was not straight out of a Nikon camera. Of course the ability to actually use the sensor data for development in a raw editor like rawtherapee_ is fully retained.

    Just to be clear though, this program comes with *no warranty whatsoever*. If you are religious about your raw nef files, do NOT use this program, it might just give you an ulcer. And please, do not send me any message either to tell me how horrible nefarious is... If you don't like it, just move on and forget about it.

    Now, if you DO try it, please be a good computer user and 1) try first on a few files before running this on your entire image collection. 2) do me and yourself a favour and have your data backed up.

Why was that the first question?
    The first time I submitted the idea of a nef manipulation program to replace the dummy jpeg preview, the first few reactions I received were rather negative. So, the first FAQ question was relevant to:

    #. inform people nefarious is something they might not like, and they can stop right there if they feel offended
    #. "nefarious" as the utility name was chosen because of such people :D

Why the name "nefarious"?
    "nefarious" means nasty, and many people think touching raw files is just that. Additionally, we are manipulating nef files here, and well, there is only one word in the oxford dictionary that starts with "nef", and that's "nefarious" :).

What can nefarious do?
    nefarious is basically a python lib, that allows you to manipulate tiff tags and tiff structure. For example adding a new subdirectory to store additional images or data is possible, modifying the comments, adding your own custom fields in the file, or replacing the jpeg preview image.

    nefarious also has a simple cli tool that can do 2 things: 1) print the structure of a given nef; and 2) replace the preview jpeg by another jpg (jpg should have been jpegtran-ed first).

    nefarious understands tiff tags, so any tag that is stored as a native tiff type (string, shorts, longs, rational, etc.) can be modified easily.

    nefarious can't let you modify things it doesn't understand, for example: the actual pixel data of the jpeg preview; the raw sensor data; the Nikon maker notes

Will nefarious have the ability to edit the tags in the Nikon makernotes, like other tiff tags ?
    Unlikely. I know the makernotes encryption has been cracked and they are now fully readable, but I have no need for editing this myself, and I had enough pain dealing with tiff reading/writing.

Is nefarious cross platform?
    Hopefully. I've used python standard size structs for all reading and writing, which match the tiff specifications, it should work with python on any platform, but I've only tested it on my gentoo amd64 box.

Which nef format/version does nefarious support?
    So far nefarious is tested on my own D300S nef files. It knows how to parse a typical tiff file by being aware of which tiff tags represent tiff directories (only 3 in the D300S).

    nefarious has successfully read and rewritten nefs from my ex-D60 as well, but I haven't attempted to set the jpeg preview for D60 pics (yet).

why are nefarious written nef files smaller than the original nefs?
    Very observant! so I guess you've noticed in plain read-and-write-again, around 100 bytes are missing from the written files... Did nefarious erase something? Actually, I'm not sure myself. I assume this is because the nef file from Nikon must be storing a few extra bytes for padding here and there when writing. nefarious writes the absolute minimum with no consideration for padding. and so saves these few bytes.

    I must admit this has bothered me, especially since I haven't managed to find these extra bytes in some samples nefs (it's not easy to find a 100 bytes in a 15MB file). I have somewhat put my worries to rest after:

    - doing structure prints of the original nef and written nef reported the same data
    - dcraw was able to extract the preview jpeg from the written nef with no complaint whatsoever
    - I could open the written nef in rawtherapee, see all data, including makernotes, and proceed with editing as usual

    That being said, I actually couldn't find whether the (supposedly) padding bytes are supposed to be there or not (i.e. should I write pading bytes when saving the nef?). I'd welcome any information on this.
    
Will nefarious support more nef versions?
    I have nefs from 2 cameras, my ex-D60 and my current D300S. nefarious is only fully tested on the D300S nefs, full test and support for the D60 will ceratinly come soon.

    I haven't researched the nef produced by other Nikon DSLRs like D90, etc. But assuming Nikon sticked to tiff file format for all its cameras, many other might just work with nefarious out of the box. DON'T take my word for it! Backup your data and run a few tests yourself.

    If some nef files from some Nikon cameras don't work with nefarious, contributors are welcome to add support.

Will nefarious support other types of raw files (e.g. from Canon)?
    Unlikely. I don't own any canon cameras. That being said, if raw files from Canon also follow the tiff specifications, perhaps nefarious could understand them with some minor updates. I won't work on that though, but contributors are welcome.

Will nef-cli support more operations than just print-structure, and replace-preview-jpeg?
    Maybe. If there are nef editing tasks than come up often in my workflow, I'll make the sure they exists in nef-cli for convenience.

    For any hadhoc manipulation job, it's very easy to write a one-off custom python program to load a nef file, modify it as needed and save it again.

What's the licence of nefarious?
    nefarious is published under the MIT license, full description in github: `nefarious license`_.

    nefarious uses copy/pasted tiff tags constants from the PIL library. The PIL license is also provided in githug: `PIL license`_.
