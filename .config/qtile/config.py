# Copyright (c) 2010 Aldo Cortesi Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

import myColors


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call(home)


mod = "mod4"
mod5 = "mod5"  # AltGr
terminal = "kitty"


# Functions
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


# Keybindings
keys = [
    # Window focus
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between columns or up/down
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow/shrink windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Stack and layout switching
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Personalization
    Key([mod, "shift"], "n", lazy.spawn("rofi -show drun")),
    Key(
        [mod], "m", lazy.next_layout(), desc="Toggle between layouts"
    ),  # redundant, could remove one
    Key(
        [mod, "shift"],
        "m",
        minimize_all(),
        desc="Minimize or restore all windows on current group",
    ),
    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 set Master 2- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 set Master 2+ unmute")),
    # Screenshot
    Key(
        [mod],
        "s",
        lazy.spawn(
            "scrot '%Y-%m-%d-%T_$wx$h.png' -e 'mkdir -p ~/Pictures/screenshots && mv $f ~/Pictures/screenshots/'"
        ),
    ),
    # Applications
    Key([mod], "b", lazy.spawn("zen-browser")),
    Key([mod], "e", lazy.spawn("kitty yazi")),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [
    Group(name="u", label=""),  # Using a Nerd Font icon
    Group(name="i", label=""),  # Using a FontAwesome icon
    Group(name="o", label=""),  # Using a FontAwesome icon
    Group(name="p", label=""),  # Using a FontAwesome icon
]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# Theme Dracula
color = myColors.Monokai

layout_theme = {
    "border_width": 2,
    "margin": 2,
    "border_focus": color["blue"],
    "border_normal": color["dark"],
}
layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="NotoSans Nerd Font Propo 13",
    fontsize=18,
    padding=3,
    background=color["dark"],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper=os.path.join(
            os.path.expanduser("~"), ".config/qtile/wallpapers/fedora-night.jpg"
        ),
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                # GroupBox widget with custom colors
                widget.GroupBox(
                    margin_y=3,
                    margin_x=0,
                    padding=5,
                    borderwidth=3,
                    active=color["green"],  # Color of active group
                    inactive=color["red"],  # Color of inactive groups
                    rounded=True,
                    highlight_method="block",
                    this_current_screen_border=color["gray"],  # Border color for the current screen
                    this_screen_border=color["gray"],  # Border color for this screen
                    other_current_screen_border=color["yellow"],  # Border color for other screens
                    other_screen_border=color["red"],  # Border color for other screens
                ),
                widget.Sep(
                    linewidth=1,
                    padding=10,
                    foreground=color["light"],  # Color del separador
                    background=color["dark"],  # Fondo oscuro del separador
                ),
                widget.WindowName(
                    foreground=color["light"],
                ),
                widget.CurrentLayout(
                    foreground=color["dark"], background=color["green"]
                ),
                widget.Systray(foreground=color["dark"], background=color["blue"]),
                widget.Volume(foreground=color["dark"], background=color["blue"]),
                widget.Clock(
                    format="%Y/%m/%d %a %I:%M %p",
                    foreground=color["dark"],
                    background=color["gray"],
                ),
                widget.TextBox(
                    text="󰔛",
                    foreground=color["dark"],
                    background=color["gray"],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=5,
                    background=color["gray"],
                ),
                widget.QuickExit(foreground=color["dark"], background=color["red"]),
            ],
            27,
            # Uncomment the following lines if you want to add borders to the bar
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
