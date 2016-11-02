#!/bin/bash

dir1='/opt/Pong-py'

echo 'Copying all files.'
mkdir $dir1
cp -R images $dir1
cp main.py $dir1
echo 'Copy done'

ln -s $dir1'/main.py' ~/Pong-py
