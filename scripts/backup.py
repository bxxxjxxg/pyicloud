#!/usr/bin/env python3
import os
import sys
import time
import click
from getpass import getpass
from pyicloud import PyiCloudService


def download_album(name, album):
    os.mkdir(name)
    num = len(album)
    total_start_time = time.time()
    total_amount = 0
    for (i, photo) in zip(range(num), album):
        print('(%d/%d) downloading %s' % (i, num, photo.filename),)
        start_time = time.time()
        amount = photo.save(name)
        amount += photo.save_comp(name)
        elapsed_time = time.time() - start_time
        total_elapsed_time = time.time() - total_start_time
        total_amount += amount
        print('(speed: %.2f MB/s, total speed: %.2f MB/s)' % (
            amount / 1024.0 / 1024.0 / elapsed_time, 
            total_amount / 1024.0 / 1024.0 / total_elapsed_time))


def main():
    iCloud_Account = os.getenv('ACCOUNT', '')
    DownloadFolder = '/Downloads'

    os.chdir(DownloadFolder)
    if len(iCloud_Account) == 0:
        iCloud_Account = input('Enter iCloud Account: ')
    password = getpass('Enter password of "%s": ' % iCloud_Account)
    api = PyiCloudService(iCloud_Account, password)
    if api.requires_2sa:
        if not api.send_verification_code(api.trusted_devices[0]):
            print("Failed to send verification code")
            sys.exit(1)
        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(api.trusted_devices[0], code):
            print("Failed to verify verification code")
            sys.exit(1)

    num = len(api.photos.albums)
    names = dict(zip(range(num), api.photos.albums.keys()))
    albums = dict(zip(range(num), api.photos.albums.values()))
    running = True
    while running:
        print("Found albums:")
        for i in range(num):
            print("%2d) %s" % (i, names[i]))
        option = click.prompt('Please choose an album to download: ')

        try:
            option = int(option)
        except:
            print("Not an integer.")
            sys.exit(1)

        if option < 0 or option >= num:
            running = False
            continue
        download_album(names[option], albums[option])


if __name__ in '__main__':
    main()
