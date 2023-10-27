#!/bin/bash

cd /usr/lib64/chromium-browser
sudo rm chromium-browser-backup
sudo mv chromium-browser chromium-browser-backup
sudo cp /home/jason/rpmbuild/BUILD/chromium-117.0.5938.132/out/Release/chrome /usr/lib64/chromium-browser/chromium-browser
sudo strip chromium-browser
