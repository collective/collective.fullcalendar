# -*- coding: utf-8 -*-

from collective.fullcalendar import _
from Products.Five.browser import BrowserView


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class EditEvent(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('edit_event.pt')

    def __call__(self):
        

        return self.index()
