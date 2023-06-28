# -*- coding: utf-8 -*-
from collective.fullcalendar.browser.fullcalendar import IIFullcalendarSettings
from DateTime import DateTime
from datetime import timedelta
from plone import api
from plone.app.contenttypes.behaviors.collection import ISyndicatableCollection
from plone.app.event.base import get_events
from plone.app.event.base import RET_MODE_BRAINS
from plone.dexterity.interfaces import IDexterityContainer
from plone.event.interfaces import IEvent
from Products.Five.browser import BrowserView


class FullcalendarView(BrowserView):
    def __call__(self):
        return self.index()

    def get_settings(self):
        return IIFullcalendarSettings(self.context)._data

    def add_link(self):
        settings = self.get_settings()
        target_folder = settings.get("target_folder", None)
        event_type = self.event_type
        if target_folder:
            url = target_folder.to_object.absolute_url()
        else:
            context_state = api.content.get_view(
                "plone_context_state", self.context, self.request
            )
            url = context_state.folder().absolute_url()
        url += f"/++add++{event_type}?ajax_load=1"
        return url

    @property
    def event_type(self):
        settings = self.get_settings()
        event_type = settings.get("event_type", "Event")
        return event_type

    def _get_events(self):
        if ISyndicatableCollection.providedBy(self.context):
            # Filter out non-events. Assume all event-types provde IEvent
            # Do not limit and batch results...
            custom_query = {'object_provides': IEvent.__identifier__}
            brains = self.context.results(batch=False, custom_query=custom_query, limit=10000)
        elif IDexterityContainer.providedBy(self.context):
            path = "/".join(self.context.getPhysicalPath())
            brains = get_events(self.context, expand=True, path=path)
        results = []
        for brain in brains:
            result = {}
            obj = brain.getObject()
            result["id"] = obj.UID()
            result["title"] = obj.Title()
            result["url"] = obj.absolute_url()
            result["className"] = "state-{}".format(api.content.get_state(obj))
            if obj.whole_day:
                result["start"] = obj.start.strftime("%Y-%m-%d")
                # Fullcalendar counts to end date 00:00
                end = obj.end + timedelta(days=1)
                result["end"] = end.strftime("%Y-%m-%d")
            else:
                result["start"] = obj.start.strftime("%Y-%m-%d %H:%M:%S")
                result["end"] = obj.end.strftime("%Y-%m-%d %H:%M:%S")
            results.append(result)
        return results

    def get_slot_minutes(self):
        settings = self.get_settings()
        slotMinutes = settings.get("slotMinutes")
        if slotMinutes < 1:
            result = "00:01:00"
        elif slotMinutes < 10:
            result = "00:0" + str(slotMinutes) + ":00"
        elif slotMinutes < 60:
            result = "00:" + str(slotMinutes) + ":00"
        else:
            result = "01:00:00"
        return result

    def get_all_day(self):
        settings = self.get_settings()
        if settings.get("allDay"):
            return "true"
        else:
            return "false"

    def get_weekends(self):
        settings = self.get_settings()
        if settings.get("weekends"):
            return "true"
        else:
            return "false"

    def get_first_hour(self):
        settings = self.get_settings()
        firstHour = settings.get("firstHour")
        firstHourInt = int(firstHour)
        if "+" in firstHour or "-" in firstHour:  # relative to now
            now = DateTime()
            time = now + firstHourInt / 24
            hour = time.hour()
            result = str(hour) + ":00:00"
            if hour < 10:
                result = "0" + result
        else:
            if firstHourInt < 10:
                result = "0" + str(firstHour) + ":00:00"
            else:
                if firstHourInt > 23:
                    firstHourInt = 23
                result = str(firstHourInt) + ":00:00"
        return result

    def get_time(self, time):
        if time.isdigit():  # full hour
            timeInt = int(time)
            if timeInt < 10:
                result = "0" + time + ":00"
            else:
                result = time + ":00"
        else:  # half hour or other datetimes, e.g. '5:30'
            if len(time) == 4:
                result = "0" + time
            else:
                result = time
        return result

    def get_editable(self):
        settings = self.get_settings()
        if settings.get("caleditable"):
            return "true"
        else:
            return "false"

    def current_language(self):
        lang = api.portal.get_current_language()
        return lang

    def calendar_config(self):
        settings = self.get_settings()
        configuration = {
            "events": self._get_events(),
            "initialView": settings.get("defaultCalendarView"),
            "headerToolbar": {
                "left": settings.get("headerLeft"),
                "center": "title",
                "right": settings.get("headerRight"),
            },
            "editable": self.get_editable(),
            "selectable": self.get_editable(),
            "locale": self.current_language(),
            "timeZone": "UTC",
            "firstDay": settings.get("firstDay"),
            "slotDuration": self.get_slot_minutes(),
            "allDaySlot": self.get_all_day(),
            "weekends": self.get_weekends(),
            "scrollTime": self.get_first_hour(),
            "slotMinTime": settings.get("minTime"),
            "slotMaxTime": settings.get("maxTime"),
            "height": settings.get("calendarHeight")
            if settings.get("calendarHeight")
            else 750,
        }
        return configuration
