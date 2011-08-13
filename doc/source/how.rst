how?
----

.. _libjpeg: http://en.wikipedia.org/wiki/Libjpeg


first, download nefarious from github and install it::

    $ python setup.py build install

Now... sorry... nefarious has no real documentation yet, but ali is teaching me some really funky tools and hopefully we'll have doc teom the code itself soonish.

For now, basically for using nefarious as a lib, I recommend reading the code itself as well as the cli tool (main.py) . Aslo using the cli tool, you can print the nef structure, which will let you understand what you can modify

For using the cli tool, below are some examples. Assume that

-  **input.nef** is the input nef file you want to manipulate
-  **processed.jpeg** is the developed and processed jpeg you want to inject i nyour nef to replace the dumb preview jpeg.

Note: as a prerequisite for replacing the preview jpeg with another file, that file should have all metadata stripped. That can be achieved easily with the jpegtran utility from libjpeg_.

Things you can do:

::

    $ nef-cli -i input.nef
    
Will print the nef structure

::

    $ nef-cli -i input.nef -o out.nef
    
Will parse the input nef, and just save it again with its own tiff save algorithm, with no data modification. The command basically lets you test if out.nef is still usable in your favorite nef reader (basically the data should be identical amd no nef reader should be able to tell the difference)
Note that while the data and nef structure is identical, the file byte layout is NOT. nefarious does not necessarily save tags and directories in the same file location as the original nef, but that should be of no consequence for a nef reader.

::

    $ jpegtran -optimize -copy none -outfile processed.stripped.jpg processed.jpeg
    $ nef-cli -i input.nef -p processed.stripped.jpg -o out.nef
    
The jpegtran command above prepares the jpeg file by stripping it of any unecessary metadata
The second command uses the stripped jpeg to replace the preview jpeg of the input nef, and save the resulting nef in out.nef

::

    $ jpegtran -optimize -copy none -outfile processed.stripped.jpg processed.jpeg
    $ nef-cli -i input.nef -p processed.stripped.jpg
    
Same as above, but will overwrite the input nef with new data. It will prompt you to be sure you are ok with overwriting

::

    $ jpegtran -optimize -copy none -outfile processed.stripped.jpg processed.jpeg
    $ nef-cli -i input.nef -y -p processed.stripped.jpg
    
Same as above, but automatically answers 'yes' when prompted to overwrite (use with care!)
