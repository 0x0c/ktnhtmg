#!/bin/sh
cd `dirname $0`
cp -r ./dependencies/dictation-kit/bin/common/* ./sandbox/
cp -r ./dependencies/dictation-kit/bin/osx/* ./sandbox/
chmod +x ./sandbox/*
python compile.py
