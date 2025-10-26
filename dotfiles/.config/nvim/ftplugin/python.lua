vim.lsp.config('python-ls', {
  cmd = { 'pylsp' },
  filetypes = { 'python' },
  root_markers = { '.git', 'pyproject.toml' }
})


vim.lsp.enable('python-ls')
