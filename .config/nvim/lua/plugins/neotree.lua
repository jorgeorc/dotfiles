local function toggle_neotree_focus()
  local manager = require("neo-tree.sources.manager")
  local state = manager.get_state("filesystem")

  if state and state.winid and vim.api.nvim_win_is_valid(state.winid) then
    if vim.api.nvim_get_current_win() == state.winid then
      vim.cmd("wincmd p")
    else
      vim.api.nvim_set_current_win(state.winid)
    end
  else
    vim.cmd("Neotree focus")
  end
end

return {
  {
    "nvim-neo-tree/neo-tree.nvim",
    branch = "v3.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "MunifTanjim/nui.nvim",
      "nvim-tree/nvim-web-devicons",
    },
    lazy = false,

    keys = {
      {
        "<leader>e",
        "<cmd>Neotree toggle<cr>",
        desc = "NeoTree toggle",
      },
      {
        "<leader>o",
        toggle_neotree_focus,
        desc = "NeoTree / buffer",
      },
    },

    opts = {
      window = {
        mappings = {
          ["h"] = "close_node",
          ["l"] = "open",
        },
      },
    },
  },
}
