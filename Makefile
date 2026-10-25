PYTHON ?= python3
PREFIX ?= /usr/local
MANIFEST ?= install-files.txt
DESTDIR ?=

# Detect if msgfmt is present; if not, pass --without-gettext
HAVE_MSGFMT := $(shell which msgfmt 2>/dev/null)
SETUP_FLAGS := $(if $(HAVE_MSGFMT),,--without-gettext)

INSTALL_ARGS := --prefix=$(PREFIX) --single-version-externally-managed --record=$(MANIFEST)
ifneq ($(DESTDIR),)
INSTALL_ARGS += --root=$(DESTDIR)
endif

VERSION ?= 2.1.7
DEB_NAME ?= terminator_$(VERSION)_all.deb
APPIMAGE_NAME ?= Terminator-$(VERSION)-x86_64.AppImage
APPIMAGETOOL ?= /tmp/appimagetool

.PHONY: all build install uninstall clean test deb appimage dist help

all: build

build:
	$(PYTHON) setup.py $(SETUP_FLAGS) build

install: build
	$(PYTHON) setup.py $(SETUP_FLAGS) install $(INSTALL_ARGS)
	@if [ -z "$(DESTDIR)" ] && which gtk-update-icon-cache >/dev/null 2>&1; then \
		echo "Updating icon cache..."; \
		gtk-update-icon-cache -q -f $(PREFIX)/share/icons/hicolor || true; \
	fi
	@if [ -z "$(DESTDIR)" ] && which update-desktop-database >/dev/null 2>&1; then \
		echo "Updating desktop database..."; \
		update-desktop-database $(PREFIX)/share/applications 2>/dev/null || true; \
	fi
	@echo "Terminator installed successfully."

uninstall:
	@if [ -f $(MANIFEST) ]; then \
		$(PYTHON) setup.py uninstall --manifest=$(MANIFEST); \
		rm -f $(MANIFEST); \
	else \
		echo "Manifest $(MANIFEST) not found, performing direct cleanup of $(PREFIX)..."; \
		rm -f $(PREFIX)/bin/terminator $(PREFIX)/bin/remotinator; \
		rm -rf $(PREFIX)/lib/python*/dist-packages/terminator* $(PREFIX)/lib/python*/site-packages/terminator*; \
		rm -rf $(PREFIX)/share/terminator; \
		rm -f $(PREFIX)/share/applications/terminator.desktop; \
		rm -f $(PREFIX)/share/pixmaps/terminator.png; \
		rm -f $(PREFIX)/share/metainfo/terminator.metainfo.xml $(PREFIX)/share/appdata/terminator.appdata.xml; \
		rm -f $(PREFIX)/share/man/man1/terminator.1* $(PREFIX)/share/man/man5/terminator_config.5*; \
		find $(PREFIX)/share/icons -name "*terminator*" -delete 2>/dev/null || true; \
	fi
	@if [ -z "$(DESTDIR)" ] && which gtk-update-icon-cache >/dev/null 2>&1; then \
		echo "Updating icon cache..."; \
		gtk-update-icon-cache -q -f $(PREFIX)/share/icons/hicolor || true; \
	fi
	@if [ -z "$(DESTDIR)" ] && which update-desktop-database >/dev/null 2>&1; then \
		echo "Updating desktop database..."; \
		update-desktop-database $(PREFIX)/share/applications 2>/dev/null || true; \
	fi
	@echo "Terminator uninstalled successfully from $(PREFIX)."

clean:
	@rm -rf build dist .pytest_cache 2>/dev/null || true
	@rm -rf *.egg-info 2>/dev/null || true
	@rm -f data/terminator.desktop data/terminator.metainfo.xml 2>/dev/null || true
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name '*.pyc' -delete 2>/dev/null || true

test:
	PYTHONPATH=. $(PYTHON) tests/test_borg.py
	PYTHONPATH=. $(PYTHON) tests/test_signalman.py
	PYTHONPATH=. $(PYTHON) tests/test_window_title.py
	PYTHONPATH=. $(PYTHON) tests/test_terminal_popup_menu.py

deb: build
	@echo "Creating Debian package $(DEB_NAME)..."
	@rm -rf /tmp/terminator-deb-build
	@mkdir -p /tmp/terminator-deb-build/DEBIAN
	$(PYTHON) setup.py $(SETUP_FLAGS) install --root=/tmp/terminator-deb-build --prefix=/usr --install-layout=deb --single-version-externally-managed --record=/tmp/terminator-deb-files.txt
	@echo "Package: terminator" > /tmp/terminator-deb-build/DEBIAN/control
	@echo "Version: $(VERSION)" >> /tmp/terminator-deb-build/DEBIAN/control
	@echo "Section: x11" >> /tmp/terminator-deb-build/DEBIAN/control
	@echo "Priority: optional" >> /tmp/terminator-deb-build/DEBIAN/control
	@echo "Architecture: all" >> /tmp/terminator-deb-build/DEBIAN/control
	@echo "Depends: python3, python3-gi, python3-gi-cairo, gir1.2-gtk-3.0, gir1.2-vte-2.91, gir1.2-pango-1.0, gir1.2-glib-2.0, python3-cairo, python3-configobj, python3-psutil" >> /tmp/terminator-deb-build/DEBIAN/control
	@echo "Maintainer: Terminator Community" >> /tmp/terminator-deb-build/DEBIAN/control
	@echo "Description: Multiple GNOME terminals in one window (Enhanced Edition)" >> /tmp/terminator-deb-build/DEBIAN/control
	@echo " Terminator is a program that allows you to fill a grid with terminals." >> /tmp/terminator-deb-build/DEBIAN/control
	@echo " Features modern themes, interactive setup, layout saving and wide separators." >> /tmp/terminator-deb-build/DEBIAN/control
	dpkg-deb -b /tmp/terminator-deb-build $(DEB_NAME)
	@rm -rf /tmp/terminator-deb-build /tmp/terminator-deb-files.txt
	@echo "Package created: $(DEB_NAME)"

appimage: build
	@echo "Creating AppImage $(APPIMAGE_NAME)..."
	@if [ ! -f $(APPIMAGETOOL) ]; then \
		echo "Downloading appimagetool..."; \
		curl -sL -o $(APPIMAGETOOL) "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage" && chmod +x $(APPIMAGETOOL); \
	fi
	@rm -rf /tmp/terminator-appdir
	@mkdir -p /tmp/terminator-appdir/usr/lib/python3/dist-packages /tmp/terminator-appdir/usr/bin /tmp/terminator-appdir/usr/share
	@cp -r terminatorlib /tmp/terminator-appdir/usr/lib/python3/dist-packages/
	@cp terminator remotinator /tmp/terminator-appdir/usr/bin/
	@chmod +x /tmp/terminator-appdir/usr/bin/*
	@cp -r data/icons /tmp/terminator-appdir/usr/share/
	@cp -r data/terminator /tmp/terminator-appdir/usr/share/ 2>/dev/null || true
	@cp data/terminator.desktop /tmp/terminator-appdir/terminator.desktop
	@cp data/icons/hicolor/48x48/apps/terminator.png /tmp/terminator-appdir/terminator.png
	@printf '#!/bin/bash\nHERE="$$(dirname "$$(readlink -f "$${0}")")"\nexport PATH="$${HERE}/usr/bin:$${PATH}"\nexport PYTHONPATH="$${HERE}/usr/lib/python3/dist-packages:$${PYTHONPATH}"\nexport XDG_DATA_DIRS="$${HERE}/usr/share:$${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"\nexec python3 "$${HERE}/usr/bin/terminator" "$$@"\n' > /tmp/terminator-appdir/AppRun
	@chmod +x /tmp/terminator-appdir/AppRun
	ARCH=x86_64 $(APPIMAGETOOL) /tmp/terminator-appdir $(APPIMAGE_NAME)
	@rm -rf /tmp/terminator-appdir
	@echo "AppImage created: $(APPIMAGE_NAME)"

dist: deb appimage

help:
	@echo "Available make targets:"
	@echo "  make (or make build)   - Build Terminator"
	@echo "  make install           - Install Terminator (default PREFIX=/usr/local)"
	@echo "  make uninstall         - Uninstall Terminator using manifest"
	@echo "  make test              - Run test suite"
	@echo "  make appimage          - Build portable standalone Terminator-x86_64.AppImage"
	@echo "  make deb               - Build ready-to-install Debian/Ubuntu .deb package"
	@echo "  make dist              - Build both AppImage and .deb packages"
	@echo "  make clean             - Remove build artifacts"
