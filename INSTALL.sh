#!/bin/bash

dir1='/opt/Pong-py'

function error1() {
  echo 'There was a problem during installation.'
  exit $1
}

echo 'Copying all files.'
if [ `mkdir $dir1` ] ; then
  cp -R images $dir1
  cp main.py $dir1
  echo 'Copy done.'
  
  ln -s $dir1'/main.py' ~/Pong-py
else
  error 1
fi
