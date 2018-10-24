#/usr/bin/env bash

set -euo pipefail

echo "Pulling submodules"
git submodule init
git submodule sync

old_git_email=$(git config --global user.email)
if (( $? != )); then
  old_git_email=leeavital@gmail.com
fi

echo "Installing files to: $HOME"

cd dotfiles
for file in $(ls -a)
do
   if [ -f $file ]
   then
      install -v $file $HOME
   elif [[ -d $file && $file != "." && $file != ".." ]]
   then
      echo "copying directory: " $file
      cp -R $file $HOME
   fi

done


# symlinks for neovim
echo "Symlinking neovim config"
ln -sf ~/.vim ~/.nvim
ln -sf ~/.vimrc ~/.nvimrc

echo "restoring machine specific git config"
git config --global user.email "$old_git_email"
