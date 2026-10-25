#!/usr/bin/env python3
"""Interactive Terminal Setup & Theme Chooser for Terminator.
Changes themes, transparency and blur in real-time.
"""

import sys
import os
import tty
import termios
import select
from .themes import THEMES, THEME_KEYS, get_theme, apply_theme_to_config
from .config import Config

def get_key():
    """Read a single key or escape sequence from stdin."""
    fd = sys.stdin.fileno()
    ch1 = sys.stdin.read(1)
    if ch1 == '\x1b':
        # Check if more characters are available (escape sequence)
        r, _, _ = select.select([sys.stdin], [], [], 0.05)
        if r:
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 == 'A':
                    return 'UP'
                elif ch3 == 'B':
                    return 'DOWN'
                elif ch3 == 'C':
                    return 'RIGHT'
                elif ch3 == 'D':
                    return 'LEFT'
            return 'ESC'
        return 'ESC'
    elif ch1 in ('\r', '\n'):
        return 'ENTER'
    elif ch1 == '\x03':  # Ctrl+C
        return 'CTRL_C'
    return ch1

def send_live_preview(theme_key, transparency, blur, darkness, save=False):
    """Notify running Terminator instance to update display in real-time."""
    # First update directly via DBus if available
    notified = False
    try:
        from . import ipc
        options = {
            'theme': theme_key,
            'transparency': '1' if transparency else '0',
            'blur': '1' if blur else '0',
            'darkness': str(round(darkness, 2)),
            'save': '1' if save else '0',
        }
        ipc.apply_theme_preview(options)
        notified = True
    except Exception:
        pass

    # If DBus didn't save or was not available, save directly to Config
    if save:
        cfg = Config()
        apply_theme_to_config(cfg, theme_key, transparency, blur, darkness, save=True)

def render_tui(current_idx, transparency, blur, darkness, message=""):
    """Render the TUI to standard output using ANSI escapes."""
    out = []
    out.append("\033[H\033[2J")  # Clear screen and move cursor to top-left
    out.append("\033[1;36m┌─────────────────────────────────────────────────────────────┐\033[0m\n")
    out.append("\033[1;36m│  ✨  Terminator Setup — Sélecteur de Thème & Style Live    │\033[0m\n")
    out.append("\033[1;36m└─────────────────────────────────────────────────────────────┘\033[0m\n")
    out.append("\033[2m  Navigation : [↑/↓] ou [1-9,0] pour changer en direct\033[0m\n")
    out.append("\033[2m  Options    : [T] Transparence | [B] Flou | [+/-] Opacité\033[0m\n")
    out.append("\033[2m  Valider    : [Entrée] Enregistrer | [Échap/Q] Quitter\033[0m\n\n")

    for i, key in enumerate(THEME_KEYS):
        theme = THEMES[key]
        num = (i + 1) % 10
        tag = "[Dark]" if theme['dark'] else "[Light]"
        if i == current_idx:
            # Highlight selected row
            prefix = "\033[1;32m ➜ \033[1;37;42m"
            suffix = "\033[0m"
            line = f"{prefix} [{num}] {theme['name']:<18} {tag:<7} — {theme['badge']:<32} {suffix}"
        else:
            dim_tag = "\033[34m" if theme['dark'] else "\033[33m"
            line = f"    \033[1m[{num}]\033[0m \033[1m{theme['name']:<18}\033[0m {dim_tag}{tag:<7}\033[0m \033[2m— {theme['badge']}\033[0m"
        out.append(line + "\n")

    out.append("\n\033[1;36m───────────────────────────────────────────────────────────────\033[0m\n")
    tr_status = f"\033[1;32mACTIVÉE ({int(darkness * 100)}% opacité)\033[0m" if transparency else "\033[1;31mDÉSACTIVÉE (100% opaque)\033[0m"
    blur_status = "\033[1;32mACTIVÉ\033[0m" if blur else "\033[1;31mDÉSACTIVÉ\033[0m"
    out.append(f"  \033[1mTransparence [T] :\033[0m {tr_status}\n")
    out.append(f"  \033[1mEffet Flou   [B] :\033[0m {blur_status}\n")

    if message:
        out.append(f"\n  {message}\n")
    else:
        out.append("\n  \033[3;33m➜ La fenêtre Terminator s'actualise EN TEMPS RÉEL au fur et à mesure !\033[0m\n")

    sys.stdout.write("".join(out))
    sys.stdout.flush()

def run_setup_tui():
    """Main loop for the interactive setup tool."""
    if not sys.stdin.isatty():
        print("terminator setup must be run in an interactive terminal.")
        return 1

    # Load initial config to detect current settings
    config = Config()
    transparency = (config['background_type'] == 'transparent')
    blur = bool(config.get('background_blur', True))
    darkness = float(config.get('background_darkness', 0.88))

    current_idx = 0
    # Try to detect if a known theme is already selected
    curr_bg = (config.get('background_color') or '').lower()
    for idx, key in enumerate(THEME_KEYS):
        if THEMES[key]['background_color'].lower() == curr_bg:
            current_idx = idx
            break

    # Save terminal settings to restore later
    old_term_settings = termios.tcgetattr(sys.stdin.fileno())
    tty.setcbreak(sys.stdin.fileno())

    # Hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        # Initial live preview
        send_live_preview(THEME_KEYS[current_idx], transparency, blur, darkness, save=False)
        render_tui(current_idx, transparency, blur, darkness)

        while True:
            key = get_key()
            prev_idx = current_idx
            prev_tr = transparency
            prev_blur = blur
            prev_darkness = darkness

            if key in ('UP', 'k', 'K'):
                current_idx = (current_idx - 1) % len(THEME_KEYS)
            elif key in ('DOWN', 'j', 'J'):
                current_idx = (current_idx + 1) % len(THEME_KEYS)
            elif key in ('t', 'T'):
                transparency = not transparency
            elif key in ('b', 'B'):
                blur = not blur
            elif key in ('+', '='):
                darkness = min(1.0, round(darkness + 0.05, 2))
                if not transparency:
                    transparency = True
            elif key in ('-', '_'):
                darkness = max(0.2, round(darkness - 0.05, 2))
                if not transparency:
                    transparency = True
            elif key in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                current_idx = int(key) - 1
            elif key == '0':
                current_idx = 9
            elif key == 'ENTER':
                # Save and exit
                send_live_preview(THEME_KEYS[current_idx], transparency, blur, darkness, save=True)
                theme_name = THEMES[THEME_KEYS[current_idx]]['name']
                render_tui(current_idx, transparency, blur, darkness,
                           message=f"\033[1;32m✓ Thème '{theme_name}' enregistré avec succès !\033[0m")
                print("\n")
                break
            elif key in ('q', 'Q', 'ESC', 'CTRL_C'):
                # Cancel: reload previous config
                config.base.reload()
                terminator = None
                try:
                    from .terminator import Terminator
                    terminator = Terminator()
                    terminator.reconfigure()
                except Exception:
                    pass
                render_tui(current_idx, transparency, blur, darkness,
                           message="\033[1;33mModification annulée.\033[0m")
                print("\n")
                break

            # If state changed, trigger live update
            if (current_idx != prev_idx or transparency != prev_tr or
                blur != prev_blur or darkness != prev_darkness):
                send_live_preview(THEME_KEYS[current_idx], transparency, blur, darkness, save=False)
                render_tui(current_idx, transparency, blur, darkness)

    finally:
        # Restore terminal settings and show cursor
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_term_settings)
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    return 0

if __name__ == '__main__':
    sys.exit(run_setup_tui())
