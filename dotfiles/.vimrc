" tab stuff
set tabstop=2
set shiftwidth=2
set softtabstop=2
set expandtab

set tw=0
colorscheme github

set smartindent

set nocompatible

set noerrorbells
set novisualbell
set vb t_vb=
" pattern has an upper case letter
set ignorecase
set smartcase

" menu for common commands in ex mode
set wildmenu
set wildmode=list:longest,full

set smarttab

set number

" highlight search results
set hlsearch

" nowrap
set nowrap

set cursorline


nore ; :
nore , ;

" useful when editing partial tex files
" http://tex.stackexchange.com/questions/55397/vim-syntax-highlighting-of-partial-tex-file-used-with-include-is-incorrect
let g:tex_flavor = "latex"

syntax on

set cc=80

" aspectJ
au BufNewFile,BufRead *.aj set filetype=java

au BufNewFile,BufRead *.sbt set filetype=scala

" JSON
au BufNewFile, BufRead *.json set filetype=js

execute pathogen#infect()
filetype plugin on
filetype plugin indent on

set ruler

autocmd InsertEnter * :set number
autocmd InsertLeave * :set relativenumber

au BufRead *.coffee set filetype=coffee

fun! JsPretty()
   "let lineNo = getline(".")
   execute '%!js-beautify --type js -s 2 -f - '
   "call setline(".", lineNo)
endfunction

fun! HtmlPretty()
   execute '%!js-beautify --type html -s 2 -f -'
endfun

fun! DeDupWs()
  " de-duplicate white space
  execute "%!cat -s"
endfun

" press f8 to open tagbar
nmap <F8> :TagbarToggle<CR>

" open tagbar when supported
" autocmd VimEnter * nested :call tagbar#autoopen(1)

set foldmethod=syntax
set foldlevelstart=100

" alt- ] to vsplit a definition
map <A-]> :vsp <CR>:exec("tag ".expand("<cword>"))<CR>

" search up the tree for tags
set tags=./tags;/

" Show trailing whitespace:
highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$/

noremap tn  :tabnext<CR>
noremap tp  :tabprev<CR>
noremap ts  :tab split<CR>

" ignore stuff for ctrl-p
let g:ctrlp_custom_ignore = {
  \ 'dir':  '\.git$\|\.yardoc\|public$|log\|tmp$',
  \ 'file': '\.so$\|\.dat$|\.DS_Store$'
  \ }

" get airline to show up. Not sure why this is necessary
" https://github.com/bling/vim-airline/wiki/FAQ
set laststatus=2



autocmd BufRead,BufNewFile  *.fun set syntax=sml
autocmd BufRead,BufNewFile  *.ll set syntax=llvm
