vim.keymap.set('i', 'jk', '<Esc>', { desc = 'Salir del modo insert' })

local function move_with_wrap(dir, fallback)
  return function()
    local current = vim.api.nvim_get_current_win()

    vim.cmd("wincmd " .. dir)

    local after = vim.api.nvim_get_current_win()

    if current == after then
      vim.cmd("wincmd " .. fallback)
    end
  end
end

vim.keymap.set("n", "<leader>l", move_with_wrap("l", "h"))
vim.keymap.set("n", "<leader>h", move_with_wrap("h", "l"))
vim.keymap.set("n", "<leader>j", move_with_wrap("j", "k"))
vim.keymap.set("n", "<leader>k", move_with_wrap("k", "j"))
