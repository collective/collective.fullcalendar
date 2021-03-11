# -*- coding: utf-8 -*-

from collective.fullcalendar import _
from Products.Five.browser import BrowserView
from plone import api
from datetime import datetime
import transaction


class EditEvent(BrowserView):

    def __call__(self):
        return self.index()

    def process(self):
        form = self.request.form
        result = {}
        if 'uid' not in form.keys():
            result['status'] = 'ERROR'
            result['msg'] = 'Keine UID übergeben.'
            return result
        uid = form['uid']
        brains = api.content.find(UID=uid)
        if not brains:
            result['status'] = 'ERROR'
            result['msg'] = 'Kein Termin mit dieser UID gefunden.'
            return result
        obj = brains[0].getObject()
        if 'method' not in form.keys():
            result['status'] = 'ERROR'
            result['msg'] = 'Keine Methode (resize oder move) ausgewählt.'
            return result
        method = form['method']
        if method not in ['resize', 'move']:
            result['status'] = 'ERROR'
            result['msg'] = 'Methode ist weder resize noch move.'
            return result
        if 'new_end' not in form.keys():
            result['status'] = 'ERROR'
            result['msg'] = 'Kein neuer Endzeitpunkt des Termins übergeben.'
            return result
        new_end_form = form['new_end']
        try:
            new_end = datetime.strptime(new_end_form, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError as e:
            result['status'] = 'ERROR'
            result['msg'] = 'Datumsformat des neuen Endzeitpunkt des Termins unbekannt.'
            return result
        if method == 'move':
            new_start_form = form['new_start']
            try:
                new_start = datetime.strptime(new_start_form, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError as e:
                result['status'] = 'ERROR'
                result['msg'] = 'Datumsformat des neuen Startzeitpunkt des Termins unbekannt.'
                return result
            obj.start = new_start
        obj.end = new_end
        transaction.commit()
        self.request.response.redirect('./@@fullcalendar-view')
