#!/bin/bash

dir1='/opt/Pong-py'
link1="$HOME/Pong-py.desktop"

function error1() {
  echo 'There was a problem during installation.'
  if [ -f $link1 ] ; then rm $link1 ; fi
  if [ -d $dir1 ] ; then rm -R $dir1 ; fi
  exit $1
}

function desktopEntry() {
  cat > $1 << __EOF__
[Desktop Entry]
Name=Pong-py
Comment=Application for play PONG game
Exec="/opt/Pong-py/main.py"
Icon="/opt/Pong-py/images/ball.png"
Categories=Game;Application;
Version=1.0
Type=Application
Terminal=0
__EOF__
  chmod +x $1
}

echo 'Copying all files.'
if [ -d $dir1 ] ; then error1 1 'The directory already exits' ; else mkdir $dir1 ; fi
if [ $? == 0 ] ; then
  cp -R images $dir1
  cp main.py $dir1
  chmod -R 777 "$dir1"
  echo 'Copy done.'
  #ln -s $dir1'/main.py' $link1
  desktopEntry $link1
else
  error 2 'The directory can not be created.'
fi
