" Vim with all enhancements
source $VIMRUNTIME/vimrc_example.vim

" Use the internal diff if available.
" Otherwise use the special 'diffexpr' for Windows.
if &diffopt !~# 'internal'
  set diffexpr=MyDiff()
endif
function MyDiff()
  let opt = '-a --binary '
  if &diffopt =~ 'icase' | let opt = opt . '-i ' | endif
  if &diffopt =~ 'iwhite' | let opt = opt . '-b ' | endif
  let arg1 = v:fname_in
  if arg1 =~ ' ' | let arg1 = '"' . arg1 . '"' | endif
  let arg1 = substitute(arg1, '!', '\!', 'g')
  let arg2 = v:fname_new
  if arg2 =~ ' ' | let arg2 = '"' . arg2 . '"' | endif
  let arg2 = substitute(arg2, '!', '\!', 'g')
  let arg3 = v:fname_out
  if arg3 =~ ' ' | let arg3 = '"' . arg3 . '"' | endif
  let arg3 = substitute(arg3, '!', '\!', 'g')
  if $VIMRUNTIME =~ ' '
    if &sh =~ '\<cmd'
      if empty(&shellxquote)
        let l:shxq_sav = ''
        set shellxquote&
      endif
      let cmd = '"' . $VIMRUNTIME . '\diff"'
    else
      let cmd = substitute($VIMRUNTIME, ' ', '" ', '') . '\diff"'
    endif
  else
    let cmd = $VIMRUNTIME . '\diff'
  endif
  let cmd = substitute(cmd, '!', '\!', 'g')
  silent execute '!' . cmd . ' ' . opt . arg1 . ' ' . arg2 . ' > ' . arg3
  if exists('l:shxq_sav')
    let &shellxquote=l:shxq_sav
  endif
endfunction

set nobackup
set nowritebackup
set noundofile
set listchars=eol:$,tab:>-,trail:>,precedes:<,trail:-
set noexpandtab
set linebreak
set shiftwidth=2
set tabstop=2

call plug#begin('~/vimfiles/plug-vim')
	Plug 'haishanh/night-owl.vim'
	Plug 'junegunn/vim-easy-align'
	Plug 'preservim/nerdtree'
	Plug 'scrooloose/nerdtree', { 'on': 'NERDTreeToggle' }
	Plug 'itchyny/lightline.vim'
	Plug 'bluz71/vim-nightfly-guicolors'
	Plug 'preservim/nerdcommenter'
	Plug 'vim-airline/vim-airline'
	"Plug 'valloric/youcompleteme'
	Plug 'tpope/vim-fugitive'
	Plug 'tpope/vim-surround'
	Plug 'vim-airline/vim-airline'
	Plug 'vim-airline/vim-airline-themes'
	Plug 'altercation/vim-colors-solarized'
	Plug 'kien/ctrlp.vim'

call plug#end()

if (has("termguicolors"))
	set termguicolors
endif
syntax enable
set background=dark
colorscheme night-owl
"let g:lightline = { 'colorscheme': 'nightowl' }

if has("gui_win32")
	set lines=29 columns=82
	set guifont=Consolas:h11:cANSI
endif

