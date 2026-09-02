return {
  "rose-pine/neovim",
  config = function()
    require("rose-pine").setup({
      styles = {
        italic = false,
        transparency = false,
      }
    })
  end
}
