set number
set cc=100
set cursorline
set cursorcolumn

nore ; :


" required for LSP to detect filetypes
filetype on
filetype plugin on

call plug#begin()
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
call plug#end()


set shiftwidth=2


lua vim.lsp.enable('typescript_ls')


" persist marks between files
set viminfo='100,f1


