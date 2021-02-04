# -*- coding: utf-8 -*-

from collective.fullcalendar import _
from DateTime import DateTime
from plone import api
from Products.Five.browser import BrowserView
from plone.app.contenttypes.content import Collection
from plone.app.contenttypes.content import Folder


class FullcalendarView(BrowserView):
    def __call__(self):
        return self.index()

    def getEvents(self):
        typ = type(self.context.aq_base)
        if typ == Collection:
            events = self.context.results()
        elif typ == Folder:
            events = api.content.find(context=self.context, portal_type='Event')
        results = []
        for event in events:
            obj = event.getObject()
            result = {}
            result['uid'] = obj.UID()
            result['title'] = obj.Title()
            result['start'] = obj.start
            result['end'] = obj.end
            result['url'] = obj.absolute_url()
            results.append(result)
        return results

    def renderEvents(self):
        events = self.getEvents()
        caleditable = self.context.caleditable
        result = ''
        result = result+'[\n'
        for event in events:
            result = result+'{\n'
            result = result+'  id: \''+event['uid']+'\',\n'
            result = result+'  title: \''+event['title']+'\',\n'
            result = result+'  start: \''+event['start'].strftime('%Y-%m-%d %H:%M:%S')+'\',\n'
            result = result+'  end: \''+event['end'].strftime('%Y-%m-%d %H:%M:%S')+'\',\n'
            if not caleditable:
                result = result+'  url: \''+event['url']+'\'\n'
            result = result+'},\n'
        result = result+']\n'
        return result

    def getFirstDay(self):
        firstDay = self.context.firstDay
        return firstDay

    def getSlotMinutes(self):
        slotMinutes = self.context.slotMinutes
        if slotMinutes < 1:
            result = '00:01:00'
        elif slotMinutes < 10:
            result = '00:0'+str(slotMinutes)+':00'
        elif slotMinutes < 60:
            result = '00:'+str(slotMinutes)+':00'
        else:
            result = '01:00:00'
        return result

    def getAllDay(self):
        if self.context.allDay:
            return 'true'
        else:
            return 'false'

    def getWeekends(self):
        if self.context.weekends:
            return 'true'
        else:
            return 'false'

    def getFirstHour(self):
        firstHour = self.context.firstHour
        firstHourInt = int(firstHour)
        if '+' in firstHour or '-' in firstHour:  # relative to now
            now = DateTime()
            time = now+firstHourInt/24
            hour = time.hour()
            result = str(hour)+':00:00'
            if hour < 10:
                result = '0'+result
        else:
            if firstHourInt < 10:
                result = '0'+str(firstHour)+':00:00'
            else:
                if firstHourInt > 23:
                    firstHourInt = 23
                result = str(firstHourInt)+':00:00'
        return result

    def getTime(self, time):
        if time.isdigit():  # Volle Stunde
            timeInt = int(time)
            if timeInt < 10:
                result = '0'+time+':00'
            else:
                result = time+':00'
        else:  # Krumme Angabe, z.B. '5:30'
            if len(time) == 4:
                result = '0'+time
            else:
                result = time
        return result

    def getMinTime(self):
        minTime = self.getTime(self.context.minTime)
        return minTime

    def getMaxTime(self):
        maxTime = self.getTime(self.context.maxTime)
        return maxTime

    def getEditable(self):
        if self.context.caleditable:
            return 'true'
        else:
            return 'false'
