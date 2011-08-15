Hello nefarious
===============

Installation
------------
1) clone repo
2) python setup.py build install

Note: make sure you have jpegtran installed!


CLI
---
To print a nef structure:

    $ nef-cli -i input.nef


To test nefarious save algorithm and verify written output is sane (without modification):

    $ nef-cli -i input.nef -o out.nef


To replace the preview jpeg by another processed jpeg:

    $ jpegtran -optimize -copy none -outfile processed.stripped.jpg processed.jpeg
    $ nef-cli -i input.nef -p processed.stripped.jpg -o out.nef


Same as above with intent to replace original nef (prompts to confirm):

    $ jpegtran -optimize -copy none -outfile processed.stripped.jpg processed.jpeg
    $ nef-cli -i input.nef -p processed.stripped.jpg


Same as above with intent to replace original nef (auto answers yes at prompt):

    $ jpegtran -optimize -copy none -outfile processed.stripped.jpg processed.jpeg
    $ nef-cli -i input.nef -y -p processed.stripped.jpg




More info
---------
http://nefarious.timotheegroleau.com
