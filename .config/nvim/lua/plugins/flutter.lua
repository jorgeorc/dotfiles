return {
  {
    "dart-lang/dart-vim-plugin",
  },

  {
    "akinsho/flutter-tools.nvim",
    lazy = false,
    dependencies = {
      "nvim-lua/plenary.nvim",
      "stevearc/dressing.nvim",
    },

    config = function()
      require("flutter-tools").setup({
        ui = {
          border = "rounded",
        },

        decorations = {
          statusline = {
            app_version = true,
            device = true,
          },
        },

        widget_guides = {
          enabled = false,
        },

        closing_tags = {
          highlight = "Comment",
          prefix = " // ",
          enabled = true,
        },

        lsp = {
          capabilities = require("cmp_nvim_lsp").default_capabilities(),
          color_renderers = {
            enabled = true,
          },

          on_attach = function(client, bufnr)
            local opts = { buffer = bufnr }

            -- Go to Definition
            vim.keymap.set(
              "n",
              "gd",
              vim.lsp.buf.definition,
              vim.tbl_extend("force", opts, {
                desc = "Go to Definition",
              })
            )

            -- Hover Documentation
            vim.keymap.set(
              "n",
              "K",
              vim.lsp.buf.hover,
              vim.tbl_extend("force", opts, {
                desc = "Hover Documentation",
              })
            )

            -- Code Actions
            vim.keymap.set(
              "n",
              "<leader>ca",
              vim.lsp.buf.code_action,
              vim.tbl_extend("force", opts, {
                desc = "Flutter Code Actions",
              })
            )

            -- Format Dart
            vim.keymap.set(
              "n",
              "<leader>f",
              function()
                vim.lsp.buf.format({ async = true })
              end,
              vim.tbl_extend("force", opts, {
                desc = "Format Dart File",
              })
            )

            -- View error
            vim.keymap.set(
              "n",
              "<leader>d",
              vim.diagnostic.open_float,
              vim.tbl_extend("force", opts, {
                desc = "Show line diagnostics",
              })
            )

          end,
          settings = {
            showTodos = true,
            completeFunctionCalls = true,
          },
        },
      })
    end,
  },
}
