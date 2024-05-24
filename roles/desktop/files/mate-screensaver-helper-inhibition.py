#!/usr/bin/python3
import os
import sys
import time

import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
from gi.repository import GObject as gobject

# DBus connection information for MATE screensaver
DBUS_MSCR_WAIT = 60
DBUS_MSCR_DBUS = dbus.SessionBus()
DBUS_MSCR_NAME = "org.mate.ScreenSaver"
DBUS_MSCR_PATH = "/"
DBUS_MSCR_IFACE_MAIN = "org.mate.ScreenSaver"

# DBus listening information for the Idle Inhibition Spec
DBUS_IIS_DBUS = dbus.SessionBus()
DBUS_IIS_NAME = "org.freedesktop.ScreenSaver"
DBUS_IIS_PATH = "/org/freedesktop/ScreenSaver"
DBUS_IIS_PATH2= "/ScreenSaver"
DBUS_IIS_IFACE_MAIN = "org.freedesktop.ScreenSaver"

# Connect to the system and session bus
bus_system  = dbus.SystemBus()
bus_session = dbus.SessionBus()

# Connect to MATE screensaver
print("Waiting for screensaver...")
for i in range(DBUS_MSCR_WAIT):
	try:
		mate_screensaver = dbus.Interface(
				bus_session.get_object(DBUS_MSCR_NAME, DBUS_MSCR_PATH),
				DBUS_MSCR_IFACE_MAIN
		)
	except dbus.exceptions.DBusException:
		# Screensaver not running yet
		if i < (DBUS_MSCR_WAIT - 1):
			time.sleep(1)
		else:
			print("MATE screensaver not running, aborting!", file=sys.stderr)
			sys.exit(2)
	else:
		print("MATE screensaver connected!")
		break


class IdleInhibitor(object):
	"""
	Represents a single client that inhibits the screensaver
	"""
	def __init__(self, screensaver, name, reason, cookie, unique_name):
		self.screensaver = screensaver

		self.name        = name
		self.reason      = reason
		self.cookie      = cookie
		self.unique_name = unique_name

		# Tell MATE screensaver about the application we are proxying
		self._cookie = self.screensaver.Inhibit(name, reason)

	def destroy(self):
		# Stop bothering MATE screensaver
		self.screensaver.UnInhibit(self._cookie)


# Create DBus interface
class IdleInhibitionService(dbus.service.Object):
	def __init__(self, mate_screensaver):
		# Store connection to screensaver
		self.screensaver = mate_screensaver

		# Counter for inhibition requests (used for cookies)
		self.counter = 1

		# Storage for clients
		self.inhibitors = []

		# Store constants
		self.bus   = DBUS_IIS_DBUS
		self.path  = DBUS_IIS_PATH
		self.path2 = DBUS_IIS_PATH2

		# Claim bus name with both paths used by GNOME
		dbus.service.Object.__init__(self,
				self.bus, self.path, dbus.service.BusName(DBUS_IIS_NAME, self.bus)
		)
		dbus.service.Object.__init__(self,
                self.bus, self.path2, dbus.service.BusName(DBUS_IIS_NAME, self.bus)
        )

	def on_name_change(self, sender, unique_name):
		print("mate-screensaver-helper-inhibition: on_name_change: '%s', '%s'" % (sender, unique_name))

		if sender != unique_name:
			for inhibitor in self.inhibitors:
				if inhibitor.unique_name == sender:
					self.UnInhibit(inhibitor.cookie, sender)

	@dbus.service.method(DBUS_IIS_IFACE_MAIN, "ss", "u", sender_keyword="sender")
	def Inhibit(self, application_name, reason_for_inhibit, sender):
		print("mate-screensaver-helper-inhibition: Inhibit: '%s', '%s' -> %d (from '%s')"
				% (application_name, reason_for_inhibit, self.counter + 1, sender))

		# Create new cookie
		self.counter += 1

		# Add inhibitor
		self.inhibitors.append(IdleInhibitor(
			self.screensaver,
			application_name,
			reason_for_inhibit,
			self.counter,
			sender
		))

		# Watch if bus name owner disappears
		self.bus.watch_name_owner(sender, lambda name: self.on_name_change(sender, name))

		return self.counter

	@dbus.service.method(DBUS_IIS_IFACE_MAIN, "u", "", sender_keyword="sender")
	def UnInhibit(self, cookie, sender):
		print("mate-screensaver-helper-inhibition: UnInhibit: %d (from '%s')" % (cookie, sender))

		for inhibitor in self.inhibitors:
			if inhibitor.cookie == cookie and inhibitor.unique_name == sender:
				# Stop inhibiting
				inhibitor.destroy()

				# Remove inhibitor from list
				self.inhibitors.remove(inhibitor)


# Create service
service = IdleInhibitionService(mate_screensaver)

# Wait for stuff to happen
gobject.MainLoop().run()
