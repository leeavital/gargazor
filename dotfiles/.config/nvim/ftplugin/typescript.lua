vim.lsp.config('typescript_ls', {
  cmd = { 'typescript-language-server', '--stdio' },
  filetypes = { 'typescript' },
  root_markers = { '.git', 'package.json' }
})


vim.lsp.enable('typescript_ls')

