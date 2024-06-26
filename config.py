# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
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

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [

    # ------------ Movement Configs ------------

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    #Terminal Configuration
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # ------------ Program Configs ------------

    # Menu
    Key([mod], "m", lazy.spawn("rofi -show drun")),
    #Firefox Browser Shortcut
    Key([mod], "b", lazy.spawn("firefox")),
    #Explorador de Archivos
    Key([mod], "e", lazy.spawn("thunar")),
    # Window Nav
    Key([mod, "shift"], "m", lazy.spawn("rofi -show")),
    # Screenshot
    Key([mod], "s", lazy.spawn("scrot")),
    Key([mod, "shift"], "s", lazy.spawn("scrot -s")),

    # ------------ Hardware Configs ------------

    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # BriKeyghtness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
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


groups = [Group(i) for i in [" 󰈹  ", " 󰣇  ", "   ", "   ", " 󰏆  " ,"󰚾 "]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

layout_conf = {
    'border_focus': "#FFFFFF",
    'border_width': 2,
    'margin': 4
}

layouts = [
    layout.Columns(**layout_conf),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="ttf-ubuntu-mono-nerd",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground=["#f1ffff","#f1ffff"],
                    background=["#0f101a","#0f101a"],
                    font='ttf-ubuntu-mono-nerd',
                    fontsize=18,
                    margin_y=3,
                    margin_x=0,
                    padding_y=8,
                    padding_x=5,
                    borderwidth=1,
                    active=["#f1ffff","#f1ffff"],
                    inactive=["#f1ffff","#f1ffff"],
                    rounded=False,
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border=["#4F4C50","#DC6DED"],
                    this_current_screen_border=["#4F4C50","#DC6DED"],
                    this_screen_border=["#353c4a","#353c4a"],
                    other_current_screen_border=["#0f101a","#0f101a"],
                    other_screen_border=["#0f101a","#0f101a"],
                    disable_drag=True
                ),
                widget.WindowName(
                    foreground=["#DC6DED","#DC6DED"],
                    background=["#0f101a","#0f101a"],
                    fontsize=10,
                    padding=5,
                    font='ttf-ubuntu-mono-nerd'
                ),
                widget.TextBox(
                    background=["#F07178","#F07178"],
                    foreground=["#0f101a", "#0f101a"],
                    text="󰀂 ",
                    fontsize=18
                ),
                widget.Net(
                    background=["#F07178","#F07178"],
                    foreground=["#0f101a", "#0f101a"],
                    font='ttf-ubuntu-mono-nerd',
                    format= '{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}',
                    padding= 5
                ),
                widget.TextBox(
                    background=["#ffd47e","#ffd47e"],
                    foreground=["#0f101a", "#0f101a"],
                    text="󰻠 ",
                    fontsize=18
                ),
                widget.CPU(
                    background=["#ffd47e","#ffd47e"],
                    foreground=["#0f101a", "#0f101a"],
                    padding=2,
                    font='ttf-ubuntu-mono-nerd'

                ),
                widget.TextBox(
                    background=["#fb9f7f","#fb9f7f"],
                    foreground=["#0f101a", "#0f101a"],
                    text="󰄌 ",
                    fontsize=15
                ),
                widget.Battery(
                    background=["#fb9f7f","#fb9f7f"],
                    foreground=["#0f101a", "#0f101a"],
                    charge_char="",
                    discharge_char="",
                    empty_char="",
                    format= '{char} {percent:2.0%} {watt:.2f} W',
                    font='ttf-ubuntu-mono-nerd',
                    update_interval=60,
                    padding=5
                ),
                widget.TextBox(
                    foreground=["#0f101a", "#0f101a"],
                    background=["#DC6DED","#DC6DED"],
                    text=" "
                ),
                widget.Clock(
                    foreground=["#0f101a", "#0f101a"],
                    background=["#DC6DED","#DC6DED"],
                    format='%d/%m/%Y - %H:%M ',
                    padding=5),
                widget.Systray(),
            ],
            24,
            opacity=0.7,
            #border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            #border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground=["#f1ffff","#f1ffff"],
                    background=["#0f101a","#0f101a"],
                    font='ttf-ubuntu-mono-nerd',
                    fontsize=18,
                    margin_y=3,
                    margin_x=0,
                    padding_y=8,
                    padding_x=5,
                    borderwidth=1,
                    active=["#f1ffff","#f1ffff"],
                    inactive=["#f1ffff","#f1ffff"],
                    rounded=False,
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border=["#4F4C50","#DC6DED"],
                    this_current_screen_border=["#4F4C50","#DC6DED"],
                    this_screen_border=["#353c4a","#353c4a"],
                    other_current_screen_border=["#0f101a","#0f101a"],
                    other_screen_border=["#0f101a","#0f101a"],
                    disable_drag=True
                ),
                widget.WindowName(
                    foreground=["#DC6DED","#DC6DED"],
                    background=["#0f101a","#0f101a"],
                    fontsize=10,
                    padding=5,
                    font='ttf-ubuntu-mono-nerd'
                ),
                widget.Systray(),
                widget.TextBox(
                    background=["#F07178","#F07178"],
                    foreground=["#0f101a", "#0f101a"],
                    text="󰀂 ",
                    fontsize=18
                ),
                widget.Net(
                    background=["#F07178","#F07178"],
                    foreground=["#0f101a", "#0f101a"],
                    font='ttf-ubuntu-mono-nerd',
                    format= '{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}',
                    padding= 5
                ),
                widget.TextBox(
                    background=["#ffd47e","#ffd47e"],
                    foreground=["#0f101a", "#0f101a"],
                    text="󰻠 ",
                    fontsize=18
                ),
                widget.CPU(
                    background=["#ffd47e","#ffd47e"],
                    foreground=["#0f101a", "#0f101a"],
                    padding=2,
                    font='ttf-ubuntu-mono-nerd'

                ),
                widget.TextBox(
                    background=["#fb9f7f","#fb9f7f"],
                    foreground=["#0f101a", "#0f101a"],
                    text="󰄌 ",
                    fontsize=15
                ),
                widget.Battery(
                    background=["#fb9f7f","#fb9f7f"],
                    foreground=["#0f101a", "#0f101a"],
                    charge_char="",
                    discharge_char="",
                    empty_char="",
                    format= '{char} {percent:2.0%} {watt:.2f} W',
                    font='ttf-ubuntu-mono-nerd',
                    update_interval=60,
                    padding=5
                ),
                widget.TextBox(
                    foreground=["#0f101a", "#0f101a"],
                    background=["#DC6DED","#DC6DED"],
                    text=" "
                ),
                widget.Clock(
                    foreground=["#0f101a", "#0f101a"],
                    background=["#DC6DED","#DC6DED"],
                    format='%d/%m/%Y - %H:%M ',
                    padding=5),
            ],
            24,
            opacity=0.7,
            #border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            #border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
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

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
