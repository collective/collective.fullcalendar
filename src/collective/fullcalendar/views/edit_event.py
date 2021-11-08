# -*- coding: utf-8 -*-
from dateutil.parser import parse
from plone import api
from Products.Five.browser import BrowserView

import transaction


class EditEvent(BrowserView):
    def __call__(self):
        return self.index()

    def process(self):
        form = self.request.form
        result = {}
        if "uid" not in form.keys():
            result["status"] = "ERROR"
            result["msg"] = "Keine UID übergeben."
            return result
        uid = form["uid"]
        brains = api.content.find(UID=uid)
        if not brains:
            result["status"] = "ERROR"
            result["msg"] = "Kein Termin mit dieser UID gefunden."
            return result
        obj = brains[0].getObject()
        if "method" not in form.keys():
            result["status"] = "ERROR"
            result["msg"] = "Keine Methode (resize oder move) ausgewählt."
            return result
        method = form["method"]
        if method not in ["resize", "move"]:
            result["status"] = "ERROR"
            result["msg"] = "Methode ist weder resize noch move."
            return result
        if "new_end" not in form.keys():
            result["status"] = "ERROR"
            result["msg"] = "Kein neuer Endzeitpunkt des Termins übergeben."
            return result
        new_end_form = form["new_end"]
        try:
            # new_end = datetime.strptime(new_end_form, '%Y-%m-%dT%H:%M:%S.%f')
            new_end = self.parse_date(new_end_form)
        except ValueError as e:
            result["status"] = "ERROR"
            result[
                "msg"
            ] = f"Datumsformat des neuen Endzeitpunkt des Termins unbekannt. {e}"
            return result
        if method == "move":
            new_start_form = form["new_start"]
            try:
                new_start = self.parse_date(new_start_form)
            except ValueError as e:
                result["status"] = "ERROR"
                result[
                    "msg"
                ] = f"Datumsformat des neuen Startzeitpunkt des Termins unbekannt. {e}"
                return result
            obj.start = new_start
        obj.end = new_end
        transaction.commit()
        self.request.response.redirect(self.request["HTTP_REFERER"])

    def parse_date(self, date_str):
        dt = parse(date_str)
        # dt is now: datetime.datetime(2017, 3, 8, 15, 18, 52, 000000, tzinfo=tzutc())

        from plone.app.event.base import default_timezone
        from plone.event import utils

        tz = default_timezone()  # E.g.: 'Europe/Vienna'
        dt = utils.dt_to_zone(dt, tz)
        # dt is now: datetime.datetime(2017, 3, 8, 16, 18, 52, tzinfo=<DstTzInfo 'Europe/Vienna' CET+1:00:00 STD>)

        # Converting to utc before
        dt = utils.utc(dt)
        # dt is now: datetime.datetime(2017, 3, 8, 15, 18, 52, tzinfo=<UTC>)

        dt.isoformat()  # '2017-03-08T15:18:52+00:00'

        return dt
