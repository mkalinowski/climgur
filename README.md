climgur
=======

A simple command line imgur uploader, perfect for automatic
screenshot uploading.
Just bind any key combination to

    scrot --select --exec 'climgur.py $f'

and you'll share your screen instantly.

Uploaded URLs are copied to the X selection (middle mouse button).
Database of uploaded files and deletion links is in "$HOME/.climgurdb"

Requirements:
* python3
* [notify2](http://pypi.python.org/pypi/notify2)

