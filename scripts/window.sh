# Window hook for .github/scripts/capture-windows.sh: kitty runs the shared session
# from docs/PREVIEWS.md with each theme.
# Requires: kitty, fastfetch, eza.
# shellcheck shell=bash
name=kitty

launch() {
  printf 'kitty --config NONE --title kanagawa -o include=%s -o "font_family=%s" -o font_size=11 -o tab_bar_min_tabs=1 -o tab_title_template=kanagawa -o window_padding_width=8 -o linux_display_server=wayland %s %s' \
    "$root/themes/kanagawa-$1.conf" "$font" "$session" "$1"
}
