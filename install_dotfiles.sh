#/usr/bin/env bash

set -e


echo "Pulling submodules"
git submodule init
git submodule sync

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
ln -s ~/.vim ~/.nvim
ln -s ~/.vimrc ~/.nvimrc
