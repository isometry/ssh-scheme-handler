install:
	install --mode=0755 ssh-scheme-handler.py /usr/local/bin/ssh-scheme-handler
	install --mode=0644 ssh-scheme-handler.desktop /usr/share/applications/

activate:
	xdg-desktop-menu install /usr/share/applications/ssh-scheme-handler.desktop
	xdg-mime default ssh-scheme-handler.desktop x-scheme-handler/ssh x-scheme-handler/mosh
