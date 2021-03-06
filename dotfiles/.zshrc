# Set up the prompt


alias ll="ls -lagG"

MANPATH=$MATHPATH:/usr/local/opt/erlang/lib/erlang/man
MAHPATH=$MANPATH:/usr/local/Cellar

alias grep="grep --color=auto"
alias egrep="egrep --color=auto"

# new shells open up in zsh
export SHELL=zsh

set -o vi
bindkey "^R" history-incremental-search-backward

# so I can use ggrep :)
export PATH=/usr/local/bin:/usr/local/sbin:$PATH:/usr/local/Cellar
export PATH=$PATH:/Users/lee/bin


export SBT_OPTS="-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,address=4000,server=y,suspend=n"


function ads_ssh() { ssh -i ~/.ssh/key-adsymp adsymp@"$1"; }



unsetopt beep


function prompt_char {
   br=`git branch >/dev/null 2>/dev/null && git branch | grep "\*.*" | sed -e 's/^..//' && return`
   case "$br" in
      "")
         echo ""
         ;;
      *)
         echo "on $fg[blue]$br$reset_color"
         ;;
   esac
   return
}

function nice_pwd {
 # pwd | sed 's/\([a-z]\)[a-z]*\//\1\//gi'
 pwd | sed 's/\([^\\/]\)[^\\/]*\//\1\//gi'
}

function gen_jvm_project {
   mkdir -p src/main/$1
   mkdir -p src/test/$1

}


autoload -Uz promptinit 
autoload -U colors && colors
promptinit
setopt prompt_subst


# PROMPT="$fg[green]%n$reset_color at $fg[red]%m $reset_color %U%B(%d)%b%u $ "
# PROMPT="$fg[green]%n$reset_color at $fg[red]%m $reset_color %U%B(%d)%b%u 
# $ "




PS1='$fg[green]%n$reset_color at $fg[red]%m $reset_color %U%B(%d)%b%u $(prompt_char)
$ '


# PROMPT="$fg[green]%n$reset_color at $fg[red]%m $reset_color %U%B(${nice_pwd})%b%u 
# $ "


setopt histignorealldups sharehistory

set -o vi


# Keep 1000 lines of history within the shell and save it to ~/.zsh_history:
HISTSIZE=1000
SAVEHIST=1000
HISTFILE=~/.zsh_history

# Use modern completion system
autoload -Uz compinit
compinit

zstyle ':completion:*' auto-description 'specify: %d'




ffs (){
  find . | egrep -i "$@"
}






zstyle ':completion:*' completer _expand _complete _correct _approximate
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' group-name ''
zstyle ':completion:*' menu select=2
# eval "$(dircolors -b)"
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s
zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'
zstyle ':completion:*' menu select=long
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ':completion:*' use-compctl false
zstyle ':completion:*' verbose true

zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'
zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'

if [[ -f ~/.zprofile ]]
then
  source ~/.zprofile
fi

function markdown()
{
  pandoc -s -f markdown -t html "${1}" | sed 's/^<pre class/<p><\/p><pre class/' | lynx -stdin
}
