# Terminator by Chris Jones <cmsj@tenshu.net>
# GPL v2 only
"""titlebar.py - classes necessary to provide a terminal title bar"""

from gi.repository import Gtk, Gdk
from gi.repository import GObject
from gi.repository import Pango

from .version import APP_NAME
from .util import dbg
from .terminator import Terminator
from .editablelabel import EditableLabel
from .translation import _

# pylint: disable-msg=R0904
# pylint: disable-msg=W0613
class Titlebar(Gtk.EventBox):
    """Class implementing the Titlebar widget"""

    terminator = None
    terminal = None
    config = None
    oldtitle = None
    termtext = None
    sizetext = None
    label = None
    ebox = None
    groupicon = None
    grouplabel = None
    groupentry = None
    bellicon = None
    btn_zoom = None
    btn_split_h = None
    btn_split_v = None
    btn_layout_3 = None
    icon_zoom = None

    __gsignals__ = {
            'clicked': (GObject.SignalFlags.RUN_LAST, None, ()),
            'edit-done': (GObject.SignalFlags.RUN_LAST, None, ()),
            'create-group': (GObject.SignalFlags.RUN_LAST, None,
                (GObject.TYPE_STRING,)),
    }

    def __init__(self, terminal):
        """Class initialiser"""
        GObject.GObject.__init__(self)

        self.terminator = Terminator()
        self.terminal = terminal
        self.config = self.terminal.config

        self.label = EditableLabel()
        self.label.connect('edit-done', self.on_edit_done)
        self.ebox = Gtk.EventBox()
        grouphbox = Gtk.HBox()
        self.grouplabel = Gtk.Label(ellipsize='end')
        self.groupicon = Gtk.Image()
        self.bellicon = Gtk.Image()
        self.bellicon.set_no_show_all(True)

        self.groupentry = Gtk.Entry()
        self.groupentry.set_no_show_all(True)
        self.groupentry.connect('focus-out-event', self.groupentry_cancel)
        self.groupentry.connect('activate', self.groupentry_activate)
        self.groupentry.connect('key-press-event', self.groupentry_keypress)

        groupsend_type = self.terminator.groupsend_type
        if self.terminator.groupsend == groupsend_type['all']:
            icon_name = 'all'
        elif self.terminator.groupsend == groupsend_type['group']:
            icon_name = 'group'
        elif self.terminator.groupsend == groupsend_type['off']:
            icon_name = 'off'
        self.set_from_icon_name('_active_broadcast_%s' % icon_name, 
                Gtk.IconSize.MENU)

        grouphbox.pack_start(self.groupicon, False, True, 2)
        grouphbox.pack_start(self.grouplabel, False, True, 2)
        grouphbox.pack_start(self.groupentry, False, True, 2)

        self.ebox.add(grouphbox)
        self.ebox.show_all()

        self.bellicon.set_from_icon_name('terminal-bell', Gtk.IconSize.MENU)

        viewport = Gtk.Viewport(hscroll_policy='natural')
        viewport.add(self.label)

        # Quick action buttons on the right side of the titlebar
        actions_box = Gtk.HBox()
        actions_box.set_spacing(1)

        def create_titlebar_btn(icon_name, fallback_icon, tooltip_text, on_click_callback):
            btn = Gtk.Button()
            btn.set_relief(Gtk.ReliefStyle.NONE)
            btn.set_can_focus(False)
            btn.set_tooltip_text(tooltip_text)
            btn.get_style_context().add_class('terminator-titlebar-btn')
            img = Gtk.Image()
            theme = Gtk.IconTheme.get_default()
            actual_icon = icon_name if theme.has_icon(icon_name) else fallback_icon
            img.set_from_icon_name(actual_icon, Gtk.IconSize.MENU)
            btn.add(img)
            btn.connect('clicked', lambda _btn: on_click_callback())
            return btn, img

        self.btn_zoom, self.icon_zoom = create_titlebar_btn(
            'window-maximize-symbolic', 'view-fullscreen',
            _('Maximiser / Restaurer le terminal'),
            lambda: self.terminal.key_toggle_zoom()
        )
        self.btn_split_h, btn_img_h = create_titlebar_btn(
            'terminator_horiz', 'object-flip-vertical-symbolic',
            _('Scinder horizontalement'),
            lambda: self.terminal.key_split_horiz()
        )
        self.btn_split_v, btn_img_v = create_titlebar_btn(
            'terminator_vert', 'object-flip-horizontal-symbolic',
            _('Scinder verticalement'),
            lambda: self.terminal.key_split_vert()
        )
        self.btn_layout_3, btn_img_3 = create_titlebar_btn(
            'terminator_layout_three', 'view-grid-symbolic',
            _('Disposition 3 panneaux (2 haut, 1 bas)'),
            lambda: self.terminal.split_layout_three()
        )

        actions_box.pack_start(self.btn_zoom, False, False, 0)
        actions_box.pack_start(self.btn_split_h, False, False, 0)
        actions_box.pack_start(self.btn_split_v, False, False, 0)
        actions_box.pack_start(self.btn_layout_3, False, False, 0)

        hbox = Gtk.HBox()
        hbox.pack_start(self.ebox, False, True, 0)
        hbox.pack_start(Gtk.VSeparator(), False, True, 0)
        hbox.pack_start(viewport, True, True, 0)
        hbox.pack_end(actions_box, False, False, 2)
        hbox.pack_end(self.bellicon, False, False, 2)

        self.add(hbox)
        hbox.show_all()
        self.set_no_show_all(True)
        self.show()

        self.connect('button-press-event', self.on_clicked)

    def connect_icon(self, func):
        """Connect the supplied function to clicking on the group icon"""
        self.ebox.connect('button-press-event', func)

    def update(self, other=None):
        """Update our contents"""
        default_bg = False

        temp_heldtext_str = ''
        temp_sizetext_str = ''

        if self.terminal.is_held_open:
            temp_heldtext_str = _('[INACTIVE: Right-Click for Relaunch option] ')
        if not self.config['title_hide_sizetext']:
            temp_sizetext_str = " %s" % (self.sizetext)
        self.label.set_text("%s%s%s" % (temp_heldtext_str, self.termtext, temp_sizetext_str))

        if (not self.config['title_use_system_font']) and self.config['title_font']:
            title_font = Pango.FontDescription(self.config['title_font'])
        else:
            title_font = Pango.FontDescription(self.config.get_system_prop_font())
        self.label.modify_font(title_font)
        self.grouplabel.modify_font(title_font)

        if other:
            term = self.terminal
            terminator = self.terminator
            if other == 'window-focus-out':
                title_fg = self.config['title_inactive_fg_color']
                title_bg = self.config['title_inactive_bg_color']
                icon = '_receive_off'
                default_bg = True
                group_fg = self.config['title_inactive_fg_color']
                group_bg = self.config['title_inactive_bg_color']
            elif term != other and term.group and term.group == other.group:
                if terminator.groupsend == terminator.groupsend_type['off']:
                    title_fg = self.config['title_inactive_fg_color']
                    title_bg = self.config['title_inactive_bg_color']
                    icon = '_receive_off'
                    default_bg = True
                else:
                    title_fg = self.config['title_receive_fg_color']
                    title_bg = self.config['title_receive_bg_color']
                    icon = '_receive_on'
                group_fg = self.config['title_receive_fg_color']
                group_bg = self.config['title_receive_bg_color']
            elif term != other and not term.group or term.group != other.group:
                if terminator.groupsend == terminator.groupsend_type['all']:
                    title_fg = self.config['title_receive_fg_color']
                    title_bg = self.config['title_receive_bg_color']
                    icon = '_receive_on'
                else:
                    title_fg = self.config['title_inactive_fg_color']
                    title_bg = self.config['title_inactive_bg_color']
                    icon = '_receive_off'
                    default_bg = True
                group_fg = self.config['title_inactive_fg_color']
                group_bg = self.config['title_inactive_bg_color']
            else:
                # We're the active terminal
                title_fg = self.config['title_transmit_fg_color']
                title_bg = self.config['title_transmit_bg_color']
                if terminator.groupsend == terminator.groupsend_type['all']:
                    icon = '_active_broadcast_all'
                elif terminator.groupsend == terminator.groupsend_type['group']:
                    icon = '_active_broadcast_group'
                else:
                    icon = '_active_broadcast_off'
                group_fg = self.config['title_transmit_fg_color']
                group_bg = self.config['title_transmit_bg_color']

            self.label.modify_fg(Gtk.StateType.NORMAL,
                    Gdk.color_parse(title_fg))
            self.grouplabel.modify_fg(Gtk.StateType.NORMAL,
                    Gdk.color_parse(group_fg))
            self.modify_bg(Gtk.StateType.NORMAL, 
                    Gdk.color_parse(title_bg))
            if not self.get_desired_visibility():
                if default_bg == True:
                    color = term.get_style_context().get_background_color(Gtk.StateType.NORMAL)  # VERIFY FOR GTK3
                else:
                    color = Gdk.color_parse(title_bg)
            self.update_visibility()
            self.ebox.modify_bg(Gtk.StateType.NORMAL,
                    Gdk.color_parse(group_bg))
            self.set_from_icon_name(icon, Gtk.IconSize.MENU)

        # Update zoom/restore button icon state
        if self.icon_zoom and hasattr(self.terminal, 'is_zoomed'):
            try:
                is_zoomed = self.terminal.is_zoomed()
                zoom_icon_name = 'window-restore-symbolic' if is_zoomed else 'window-maximize-symbolic'
                theme = Gtk.IconTheme.get_default()
                if not theme.has_icon(zoom_icon_name):
                    zoom_icon_name = 'view-restore' if is_zoomed else 'view-fullscreen'
                self.icon_zoom.set_from_icon_name(zoom_icon_name, Gtk.IconSize.MENU)
            except Exception:
                pass

    def update_visibility(self):
        """Make the titlebar be visible or not"""
        if not self.get_desired_visibility():
            dbg('hiding titlebar')
            self.hide()
            self.label.hide()
        else:
            dbg('showing titlebar')
            self.show()
            self.label.show()

    def get_desired_visibility(self):
        """Returns True if the titlebar is supposed to be visible. False if
        not"""
        if self.editing() == True or self.terminal.group:
            dbg('implicit desired visibility')
            return(True)
        else:
            dbg('configured visibility: %s' % self.config['show_titlebar'])
            return(self.config['show_titlebar'])

    def set_from_icon_name(self, name, size = Gtk.IconSize.MENU):
        """Set an icon for the group label"""
        if not name:
            self.groupicon.hide()
            return
        
        self.groupicon.set_from_icon_name(APP_NAME + name, size)
        self.groupicon.show()

    def update_terminal_size(self, width, height):
        """Update the displayed terminal size"""
        self.sizetext = "%sx%s" % (width, height)
        self.update()

    def set_terminal_title(self, widget, title):
        """Update the terminal title"""
        self.termtext = title
        self.update()
        # Return False so we don't interrupt any chains of signal handling
        return False

    def set_group_label(self, name):
        """Set the name of the group"""
        if name:
            self.grouplabel.set_text(name)
            self.grouplabel.show()
        else:
            self.grouplabel.set_text('')
            self.grouplabel.hide()
        self.update_visibility()

    def on_clicked(self, widget, event):
        """Handle a click on the label"""
        self.show()
        self.label.show()
        self.emit('clicked')

    def on_edit_done(self, widget):
        """Re-emit an edit-done signal from an EditableLabel"""
        self.emit('edit-done')

    def editing(self):
        """Determine if we're currently editing a group name or title"""
        return(self.groupentry.get_property('visible') or self.label.editing())

    def create_group(self):
        """Create a new group"""
        if self.terminal.group:
            self.groupentry.set_text(self.terminal.group)
        else:
            self.groupentry.set_text(self.terminator.new_random_group())
        self.groupentry.show()
        self.grouplabel.hide()
        self.groupentry.grab_focus()
        self.update_visibility()

    def groupentry_cancel(self, widget, event):
        """Hide the group name entry"""
        self.groupentry.set_text('')
        self.groupentry.hide()
        self.grouplabel.show()
        self.get_parent().grab_focus()

    def groupentry_activate(self, widget):
        """Actually cause a group to be created"""
        groupname = self.groupentry.get_text() or None
        dbg('creating group: %s' % groupname)
        self.groupentry_cancel(None, None)
        last_focused_term=self.terminator.last_focused_term
        if self.terminal.targets_for_new_group:
            [term.titlebar.emit('create-group', groupname) for term in self.terminal.targets_for_new_group]
            self.terminal.targets_for_new_group = None
        else:
            self.emit('create-group', groupname)
        last_focused_term.grab_focus()
        self.terminator.focus_changed(last_focused_term)

    def groupentry_keypress(self, widget, event):
        """Handle keypresses on the entry widget"""
        key = Gdk.keyval_name(event.keyval)
        if key == 'Escape':
            self.groupentry_cancel(None, None)

    def icon_bell(self):
        """A bell signal requires we display our bell icon"""
        self.bellicon.show()
        GObject.timeout_add(1000, self.icon_bell_hide)

    def icon_bell_hide(self):
        """Handle a timeout which means we now hide the bell icon"""
        self.bellicon.hide()
        return(False)

    def get_custom_string(self):
        """If we have a custom string set, return it, otherwise None"""
        if self.label.is_custom():
            return(self.label.get_text())
        else:
            return(None)

    def set_custom_string(self, string):
        """Set a custom string"""
        self.label.set_text(string)
        self.label.set_custom()

GObject.type_register(Titlebar)
