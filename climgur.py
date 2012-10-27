#!/usr/bin/env python3

# A simple command line imgur uploader, perfect for automatic
# screenshot uploading.
# Just bind any key to
#   scrot --select --exec 'climgur.py $f'
# and you'll share your screen instantly

# Written by Mikolaj Kalinowski <mikolaj.kalinowski@gmail.com>

import os

# Should you run into any problems, get your own key on:
# https://imgur.com/register/api_anon (it takes 10 seconds)
API_KEY = '19131d0c90d429f041b6e61452ed509f'

# All uploads are logged to that file as "<epoch>,<image url>,<delete url>"
DB_FILE = os.getenv('HOME') + '/.climgurdb'


def notify(text, sticky=False, update=None):
    import notify2

    notify2.init("climgur")

    if update:
        notification = update
        notification.update(text)
    else:
        notification = notify2.Notification(text, '', '')

    if sticky:
        notification.set_timeout(notify2.EXPIRES_NEVER)
    else:
        notification.set_timeout(notify2.EXPIRES_DEFAULT)

    notification.show()
    print(text)

    return notification


def set_clipboard(text):
    from subprocess import Popen, PIPE

    pipe = Popen(['xsel', '--primary --input'], shell=True, stdin=PIPE).stdin
    pipe.write(bytes(text, 'ascii'))
    pipe.flush()
    pipe.close()


def update_database(time, original, delete_page):
    with open(DB_FILE, 'a+') as f:
        f.write(str(time) + ',' + original + ',' + delete_page + '\n')


def upload_image(path_to_image):
    from xml.dom import minidom
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import HTTPError
    from base64 import b64encode

    # based on http://api.imgur.com/examples#uploading_python3
    url = 'http://api.imgur.com/2/upload.xml'
    response_keys = ['original', 'delete_page']

    image = b64encode(open(path_to_image, 'rb').read())
    parameters = {'key': API_KEY,
                  'image': image}
    request_data = urlencode(parameters).encode('utf-8')

    try:
        response_data = urlopen(url, request_data).readall()
    except HTTPError as e:
        response_data = e.read()
        response_keys = ['message']

    document = minidom.parseString(response_data.decode())

    response_dict = {}
    for identifier in response_keys:
        el = document.getElementsByTagName(identifier)[0]
        content = el.lastChild.toxml().strip()

        response_dict[identifier] = content

    return response_dict


def main():
    import sys
    from time import time

    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <image path>")
        quit(-1)

    image_name = sys.argv[1]
    image_path = os.path.join(os.getcwd(), image_name)

    n = notify("Uploading " + image_name, sticky=True)

    response_dict = upload_image(image_path)

    if 'message' in response_dict:
        notify("Upload failed: %s" % response_dict['message'], update=n)
    else:
        response_dict['time'] = int(time())
        update_database(**response_dict)

        original = response_dict['original']
        set_clipboard(original)

        notify(("URL copied to the X selection: %s." % original), update=n)


if __name__ == '__main__':
    main()
