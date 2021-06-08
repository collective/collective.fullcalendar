# -*- coding: utf-8 -*-

from collective.fullcalendar import _
from DateTime import DateTime
from plone import api
from Products.Five.browser import BrowserView
from plone.app.contenttypes.content import Collection
from plone.app.contenttypes.content import Folder

# Import existing method for getting events
from plone.app.event.base import get_events
from plone.app.event.base import RET_MODE_OBJECTS

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
            events = get_events(self.context, ret_mode=RET_MODE_OBJECTS, expand=True)
        results = []
        for event in events:
            try:
                obj = event.getObject()
            except AttributeError:
                obj = event
            caleditable = self.context.caleditable
            result = {}
            result['id'] = obj.UID()
            result['title'] = obj.Title()
            result['start'] = obj.start.strftime('%Y-%m-%d %H:%M:%S')
            result['end'] = obj.end.strftime('%Y-%m-%d %H:%M:%S')
            if caleditable:
                result['url'] = obj.absolute_url()
            results.append(result)
        return results

    # def render_events(self):
    #     events = self._get_events()
    #     # caleditable = self.context.caleditable
    #     result = json.dumps(events)
    #     # if not caleditable:
    #     #     result = result + '  url: \'' + event['url'] + '\'\n'
    #     return result

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

    def calendar_config(self):
        configuration = {
            "timeZone": "UTC",
            "slotDuration": self.get_slot_minutes(),
            "allDaySlot": self.get_all_day(),
            "initialView": self.context.defaultCalendarView,
            "locale": self.current_language(),
            "firstDay": self.get_first_day(),
            "headerToolbar": {
                "left": self.context.headerLeft,
                "center": "title",
                "right": self.context.headerRight,
            },
            "weekends": self.get_weekends(),
            "scrollTime": self.get_first_hour(),
            "slotMinTime": self.get_min_time(),
            "slotMaxTime": self.get_max_time(),
            "height": self.context.calendarHeight if self.context.calendarHeight else 750,
            "editable": self.get_editable(),
            "selectable": self.get_editable(),
            "events": self._get_events(),
        }
        return configuration
