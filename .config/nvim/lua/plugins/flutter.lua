return {
  'nvim-flutter/flutter-tools.nvim',
  lazy = false,
  dependencies = {
    'nvim-lua/plenary.nvim',
    'stevearc/dressing.nvim',
  },
  config = function()
    require('flutter-tools').setup({})

    -- Show hover
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, { desc = 'LSP Hover' })

    -- Jump to definition
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, { desc = 'Go to Definition' })

    -- Code actions
    vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, { desc = 'Code Action' })
    vim.keymap.set('x', '<leader>ca', vim.lsp.buf.code_action, { desc = 'Code Action' })
  end,
}
