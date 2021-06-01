# -*- coding: utf-8 -*-

from collective.fullcalendar import _
from DateTime import DateTime
from plone import api
from Products.Five.browser import BrowserView
from plone.app.contenttypes.content import Collection
from plone.app.contenttypes.content import Folder

# Import existing method for getting events
from plone.app.event.base import get_events

# Import JSON to use dumps()
import json


class FullcalendarView(BrowserView):
    def __call__(self):
        return self.index()

    def _get_events(self):
        typ = type(self.context.aq_base)
        if typ == Collection:
            events = self.context.results()
        elif typ == Folder:
            events = get_events(self.context)
        results = []
        for event in events:
            obj = event.getObject()
            result = {}
            result['id'] = obj.UID()
            result['title'] = obj.Title()
            result['start'] = obj.start.strftime('%Y-%m-%d %H:%M:%S')
            result['end'] = obj.end.strftime('%Y-%m-%d %H:%M:%S')
            result['url'] = obj.absolute_url()
            results.append(result)
        return results

    def render_events(self):
        events = self._get_events()
        # caleditable = self.context.caleditable
        result = json.dumps(events)
        # if not caleditable:
        #     result = result + '  url: \'' + event['url'] + '\'\n'
        return result

    def get_first_day(self):
        firstDay = self.context.firstDay
        return firstDay

    def get_slot_minutes(self):
        slotMinutes = self.context.slotMinutes
        if slotMinutes < 1:
            result = '00:01:00'
        elif slotMinutes < 10:
            result = '00:0' + str(slotMinutes) + ':00'
        elif slotMinutes < 60:
            result = '00:' + str(slotMinutes) + ':00'
        else:
            result = '01:00:00'
        return result

    def get_all_day(self):
        if self.context.allDay:
            return 'true'
        else:
            return 'false'

    def get_weekends(self):
        if self.context.weekends:
            return 'true'
        else:
            return 'false'

    def get_first_hour(self):
        firstHour = self.context.firstHour
        firstHourInt = int(firstHour)
        if '+' in firstHour or '-' in firstHour:  # relative to now
            now = DateTime()
            time = now + firstHourInt / 24
            hour = time.hour()
            result = str(hour) + ':00:00'
            if hour < 10:
                result = '0' + result
        else:
            if firstHourInt < 10:
                result = '0' + str(firstHour) + ':00:00'
            else:
                if firstHourInt > 23:
                    firstHourInt = 23
                result = str(firstHourInt) + ':00:00'
        return result

    def get_time(self, time):
        if time.isdigit():  # Volle Stunde
            timeInt = int(time)
            if timeInt < 10:
                result = '0' + time + ':00'
            else:
                result = time + ':00'
        else:  # Krumme Angabe, z.B. '5:30'
            if len(time) == 4:
                result = '0' + time
            else:
                result = time
        return result

    def get_min_time(self):
        minTime = self.get_time(self.context.minTime)
        return minTime

    def get_max_time(self):
        maxTime = self.get_time(self.context.maxTime)
        return maxTime

    def get_editable(self):
        if self.context.caleditable:
            return 'true'
        else:
            return 'false'

    def current_language(self):
        lang = api.portal.get_current_language()
        return lang
