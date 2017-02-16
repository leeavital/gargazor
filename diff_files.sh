#!/usr/bin/env bash

cd dotfiles

for file in $(find .  -not -type d)
do
  installed="$HOME/$file"
  actual=$file

  if [[ "$(md5 -q $actual)" == "$(md5 -q $installed)" ]]
  then
    echo "$installed in sync"
  else
    vimdiff $installed $actual
  fi
done
