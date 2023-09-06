#!/bin/sh

./basm.py $1 && ./basm.py $1 | head -n 1 | xclip -sel c
