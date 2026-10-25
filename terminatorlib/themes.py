# Terminator - Modern Themes Definition & Manager
"""Modern themes and styling manager for Terminator"""

THEMES = {
    'claude_dark': {
        'name': 'Claude Dark',
        'badge': 'Anthropic warm carbon & amber',
        'dark': True,
        'background_color': '#181816',
        'foreground_color': '#eae7df',
        'cursor_color': '#d97706',
        'palette': '#262624:#e05252:#5eb87a:#d97706:#5a9ee8:#ad6be6:#2bbac5:#d5d0c7:#54524c:#f06a6a:#74d492:#f59e0b:#7cb4f8:#c084fc:#4dd0e1:#ffffff',
        'title_transmit_bg_color': '#2a2825',
        'title_transmit_fg_color': '#ffffff',
        'title_receive_bg_color': '#22201d',
        'title_receive_fg_color': '#d5d0c7',
        'title_inactive_bg_color': '#1e1c1a',
        'title_inactive_fg_color': '#8c877d',
    },
    'claude_light': {
        'name': 'Claude Light',
        'badge': 'Anthropic clean paper & amber',
        'dark': False,
        'background_color': '#faf8f5',
        'foreground_color': '#2d2b28',
        'cursor_color': '#d97706',
        'palette': '#e8e4dc:#d13b3b:#2d8a4e:#b45309:#2563eb:#8b5cf6:#0891b2:#57534e:#9c9689:#ef4444:#22c55e:#f59e0b:#3b82f6:#a855f7:#06b6d4:#1c1917',
        'title_transmit_bg_color': '#ebe6df',
        'title_transmit_fg_color': '#1c1917',
        'title_receive_bg_color': '#f2ede6',
        'title_receive_fg_color': '#44403c',
        'title_inactive_bg_color': '#f7f4ef',
        'title_inactive_fg_color': '#a8a29e',
    },
    'catppuccin_mocha': {
        'name': 'Catppuccin Mocha',
        'badge': 'Modern pastel & deep violet dark',
        'dark': True,
        'background_color': '#1e1e2e',
        'foreground_color': '#cdd6f4',
        'cursor_color': '#f5e0dc',
        'palette': '#45475a:#f38ba8:#a6e3a1:#f9e2af:#89b4fa:#f5c2e7:#94e2d5:#bac2de:#585b70:#f38ba8:#a6e3a1:#f9e2af:#89b4fa:#f5c2e7:#94e2d5:#a6adc8',
        'title_transmit_bg_color': '#313244',
        'title_transmit_fg_color': '#cdd6f4',
        'title_receive_bg_color': '#28293d',
        'title_receive_fg_color': '#a6adc8',
        'title_inactive_bg_color': '#181825',
        'title_inactive_fg_color': '#6c7086',
    },
    'catppuccin_latte': {
        'name': 'Catppuccin Latte',
        'badge': 'Modern soft & soothing light',
        'dark': False,
        'background_color': '#eff1f5',
        'foreground_color': '#4c4f69',
        'cursor_color': '#dc8a78',
        'palette': '#5c5f77:#d20f39:#40a02b:#df8e1d:#1e66f5:#ea76cb:#179299:#acb0be:#6c6f85:#d20f39:#40a02b:#df8e1d:#1e66f5:#ea76cb:#179299:#bcc0cc',
        'title_transmit_bg_color': '#ccd0da',
        'title_transmit_fg_color': '#4c4f69',
        'title_receive_bg_color': '#dce0e8',
        'title_receive_fg_color': '#5c5f77',
        'title_inactive_bg_color': '#e6e9ef',
        'title_inactive_fg_color': '#8c8fa1',
    },
    'tokyo_night': {
        'name': 'Tokyo Night',
        'badge': 'Tokyo neon midnight blue',
        'dark': True,
        'background_color': '#1a1b26',
        'foreground_color': '#c0caf5',
        'cursor_color': '#c0caf5',
        'palette': '#15161e:#f7768e:#9ece6a:#e0af68:#7aa2f7:#bb9af7:#7dcfff:#a9b1d6:#414868:#f7768e:#9ece6a:#e0af68:#7aa2f7:#bb9af7:#7dcfff:#c0caf5',
        'title_transmit_bg_color': '#24283b',
        'title_transmit_fg_color': '#c0caf5',
        'title_receive_bg_color': '#1f2335',
        'title_receive_fg_color': '#9aa5ce',
        'title_inactive_bg_color': '#16161e',
        'title_inactive_fg_color': '#565f89',
    },
    'dracula': {
        'name': 'Dracula',
        'badge': 'Vibrant purple & neon dark',
        'dark': True,
        'background_color': '#282a36',
        'foreground_color': '#f8f8f2',
        'cursor_color': '#f8f8f2',
        'palette': '#21222c:#ff5555:#50fa7b:#f1fa8c:#bd93f9:#ff79c6:#8be9fd:#f8f8f2:#6272a4:#ff6e6e:#69ff94:#ffffa5:#d6acff:#ff92df:#a4ffff:#ffffff',
        'title_transmit_bg_color': '#44475a',
        'title_transmit_fg_color': '#f8f8f2',
        'title_receive_bg_color': '#383a59',
        'title_receive_fg_color': '#bd93f9',
        'title_inactive_bg_color': '#1e1f29',
        'title_inactive_fg_color': '#6272a4',
    },
    'one_dark_pro': {
        'name': 'One Dark Pro',
        'badge': 'VS Code & Atom iconic dark',
        'dark': True,
        'background_color': '#21252b',
        'foreground_color': '#abb2bf',
        'cursor_color': '#528bff',
        'palette': '#282c34:#e06c75:#98c379:#e5c07b:#61afef:#c678dd:#56b6c2:#abb2bf:#5c6370:#e06c75:#98c379:#e5c07b:#61afef:#c678dd:#56b6c2:#ffffff',
        'title_transmit_bg_color': '#2c313a',
        'title_transmit_fg_color': '#d7dae0',
        'title_receive_bg_color': '#252930',
        'title_receive_fg_color': '#abb2bf',
        'title_inactive_bg_color': '#1b1d23',
        'title_inactive_fg_color': '#5c6370',
    },
    'nord': {
        'name': 'Nord',
        'badge': 'Arctic cold blue & clean aesthetic',
        'dark': True,
        'background_color': '#2e3440',
        'foreground_color': '#d8dee9',
        'cursor_color': '#d8dee9',
        'palette': '#3b4252:#bf616a:#a3be8c:#ebcb8b:#81a1c1:#b48ead:#88c0d0:#e5e9f0:#4c566a:#bf616a:#a3be8c:#ebcb8b:#81a1c1:#b48ead:#8fbcbb:#eceff4',
        'title_transmit_bg_color': '#3b4252',
        'title_transmit_fg_color': '#eceff4',
        'title_receive_bg_color': '#353b49',
        'title_receive_fg_color': '#d8dee9',
        'title_inactive_bg_color': '#242933',
        'title_inactive_fg_color': '#616e88',
    },
    'gruvbox_dark': {
        'name': 'Gruvbox Dark',
        'badge': 'Warm earthy retro groove',
        'dark': True,
        'background_color': '#282828',
        'foreground_color': '#ebdbb2',
        'cursor_color': '#ebdbb2',
        'palette': '#282828:#cc241d:#98971a:#d79921:#458588:#b16286:#689d6a:#a89984:#928374:#fb4934:#b8bb26:#fabd2f:#83a598:#d3869b:#8ec07c:#ebdbb2',
        'title_transmit_bg_color': '#3c3836',
        'title_transmit_fg_color': '#ebdbb2',
        'title_receive_bg_color': '#32302f',
        'title_receive_fg_color': '#d5c4a1',
        'title_inactive_bg_color': '#1d2021',
        'title_inactive_fg_color': '#7c6f64',
    },
    'rose_pine': {
        'name': 'Rosé Pine',
        'badge': 'Minimalist warm pine & rose',
        'dark': True,
        'background_color': '#191724',
        'foreground_color': '#e0def4',
        'cursor_color': '#56526e',
        'palette': '#26233a:#eb6f92:#31748f:#f6c177:#9ccfd8:#c4a7e7:#ebbcba:#e0def4:#6e6a86:#eb6f92:#31748f:#f6c177:#9ccfd8:#c4a7e7:#ebbcba:#e0def4',
        'title_transmit_bg_color': '#2a273f',
        'title_transmit_fg_color': '#e0def4',
        'title_receive_bg_color': '#211f35',
        'title_receive_fg_color': '#c4a7e7',
        'title_inactive_bg_color': '#14131d',
        'title_inactive_fg_color': '#6e6a86',
    }
}

THEME_KEYS = list(THEMES.keys())

def get_theme(theme_key):
    return THEMES.get(theme_key, THEMES['claude_dark'])

def apply_theme_to_config(config, theme_key, transparency=True, blur=True, darkness=0.88, save=False):
    """Apply a theme's settings to the active profile in Config"""
    theme = get_theme(theme_key)
    profile = config.get_profile()

    config['background_color'] = theme['background_color']
    config['foreground_color'] = theme['foreground_color']
    config['palette'] = theme['palette']
    config['cursor_color_default'] = False
    config['cursor_bg_color'] = theme['cursor_color']
    config['cursor_fg_color'] = theme['background_color']
    config['use_theme_colors'] = False

    config['title_transmit_bg_color'] = theme['title_transmit_bg_color']
    config['title_transmit_fg_color'] = theme['title_transmit_fg_color']
    config['title_receive_bg_color'] = theme['title_receive_bg_color']
    config['title_receive_fg_color'] = theme['title_receive_fg_color']
    config['title_inactive_bg_color'] = theme['title_inactive_bg_color']
    config['title_inactive_fg_color'] = theme['title_inactive_fg_color']

    if transparency:
        config['background_type'] = 'transparent'
        config['background_darkness'] = darkness
        config['background_blur'] = blur
    else:
        config['background_type'] = 'solid'
        config['background_darkness'] = 1.0
        config['background_blur'] = False

    if save:
        config.save()
