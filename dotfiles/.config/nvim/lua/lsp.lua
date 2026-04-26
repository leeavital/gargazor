
--- TODO: move to a dedicated file
vim.lsp.config('typescript_ls', {
  -- Command and arguments to start the server.
  cmd = { 'typescript-language-server', '--stdio' },
  -- Filetypes to automatically attach to.
  filetypes = { 'ts' },
  -- Sets the "workspace" to the directory where any of these files is found.
  -- Files that share a root directory will reuse the LSP server connection.
  -- Nested lists indicate equal priority, see |vim.lsp.Config|.
  root_markers = { 'package.json' }
})




