# SSH Scheme Handler for freedesktop.org/XDG-compliant desktop environments

## Overview

Handle `ssh://[user@]host[:port]` scheme links with your preferred terminal emulator in any freedesktop.org/XDG-compliant desktop environment, including Gnome, OpenBox, KDE & Xfce.

### Supported Schemes

* [ssh](https://www.openssh.com/): `ssh://[user@]host[:port]`
* [mosh](https://mosh.org/): `mosh://[user@]host[:port]`

### Supported Terminal Emulators

* [gnome-terminal](https://wiki.gnome.org/Apps/Terminal): opens a new tab titled `[user]@host`
* [xfce4-terminal](https://docs.xfce.org/apps/terminal/): opens a new tab titled `[user]@host`
* [tmux](https://github.com/tmux/tmux): opens a new window named `[user]@host`
* [kitty](https://sw.kovidgoyal.net/kitty/): opens a new tab titled `[user]@host`; requires [remote control](https://sw.kovidgoyal.net/kitty/remote-control.html) be enabled
* [urxvt](http://software.schmorp.de/pkg/rxvt-unicode.html): opens a new window titled `[user]@host`
* [xterm](https://linux.die.net/man/1/xterm): opens a new window titled `[user]@host`

## Requirements

* A supported terminal emulator (`xfce4-terminal` recommended)
* [openssh-client](https://www.openssh.com/)
* [xdg-utils](https://www.freedesktop.org/wiki/Software/xdg-utils/)

## Installation

```sh
sudo make install
make activate
```

## Configuration

By default, the handler will try to pick the first available terminal emulator from the `TERMINAL_SEARCH_ORDER` list in `ssh-scheme-handler.py`:

1. `xfce4-terminal`
2. `gnome-terminal`
3. `urxvt`
4. `xterm`

Alternatively, the terminal emulator may be explicitly specified by:

* either, adding the `-t/--terminal` argument to the `Exec=` line in `ssh-scheme-handler.desktop`, e.g. `Exec=/usr/local/bin/ssh-scheme-handler %u -t tmux`.
* or, setting the `PREFERRED_TERMINAL_EMULATOR` environment variable, e.g. `echo export PREFERRED_TERMINAL_EMULATOR=tmux >> ~/.xsessionrc` (Xorg restart required).
