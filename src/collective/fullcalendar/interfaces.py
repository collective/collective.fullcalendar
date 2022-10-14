# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveFullcalendarLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFullcalendarEnabled(Interface):
    """Marker interface for Fullcalendar possibilities."""


class IFullcalenderEnabled(Interface):
    """Marker interface for Fullcalendar possibilities.

    Backward compatibility
    - renaming calender to calendar
    """
