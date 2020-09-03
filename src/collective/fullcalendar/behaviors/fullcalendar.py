# -*- coding: utf-8 -*-

from collective.fullcalendar import _
from plone import schema
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser import BrowserView
from z3c.relationfield.schema import RelationChoice
from zope.component import adapter
from zope.interface import implementer, Interface, provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

class IFullcalendarMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IFullcalendar(model.Schema):
    """
    """
    model.fieldset(
        'fullcalendar',
        label=_(u"Fullcalendar"),
        fields=['slotMinutes', 'allDay','defaultCalendarView','headerLeft','headerRight','weekends','firstDay','firstHour','minTime','maxTime','target_folder','calendarHeight','caleditable']
    )

    slotMinutes = schema.Int(
        title=_(u'Slot length'),
        description=_(u'Slot length in minutes'),
        required=True,
        default=30
    )
    allDay = schema.Bool(
        title=_(u'All day'),
        description=_(u'Display \"All day\" option for timeGridWeek-View'),
        required=False,
        default=True
    )
    defaultCalendarView = schema.Choice(
        title=_(u'Standard-Ansicht'),
        description=_(u'Standard-Ansicht'),
        required=True,
        vocabulary=SimpleVocabulary.fromValues(['dayGridMonth','timeGridWeek','listWeek','dayGridWeek']),
        default='dayGridMonth'
    )
    # Possible for headerLeft/headerRight: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek
    headerLeft = schema.TextLine(
        title=_(u'Kopfbereich links'),
        description=_(u'Mögliche Werte: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek'),
        required=False,
        default = 'prev,next today'
    )
    headerRight = schema.TextLine(
        title=_(u'Kopfbereich rechts'),
        description=_(u'Mögliche Werte: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek'),
        required=False,
        default = 'dayGridMonth timeGridWeek listWeek'
    )
    weekends = schema.Bool(
        title=_(u'Wochenenden anzeigen'),
        description=_(u'Wochenenden anzeigen'),
        required=False,
        default=True
    )
    firstDay = schema.Choice(
        title=_(u'Erster Wochentag'),
        description=_(u'Erster Wochentag'),
        required=True,
        vocabulary=SimpleVocabulary([SimpleTerm(value=pair[0],token=pair[0],title=pair[1]) for pair in [(0,u'sunday'),(1,u'monday'),(2,u'tuesday'),(3,u'wednesday'),(4,u'thursday'),(5,u'friday'),(6,u'saturday')]]),
        default=1
    )
    firstHour = schema.TextLine(
        title=_(u'Erste angezeigte Stunde'),
        description=_(u'Legen Sie die anfängliche Scrollposition der Kalender-Tagesansicht fest (eine Zahl zwischen 0 und 23). Wenn vor dieser Zahl ein "+" oder "-" steht, wird die Zahl mit der aktuellen Zeit addiert bzw. substrahiert.'),
        required=True,
        default='6'
    )
    minTime = schema.TextLine(
        title=_(u'Erste sichtbare Stunde'),
        description=_(u'Wählen Sie die erste sichtbare Stunde des Kalenders (z.B. \'5\' oder \'5:30\').'),
        required=True,
        default='0'
    )
    maxTime = schema.TextLine(
        title=_(u'Letzte sichtbare Stunde'),
        description=_(u'Wählen Sie die letzte sichtbare Stunde des Kalenders (z.B. \'5\' oder \'5:30\').'),
        required=True,
        default='24'
    )
    # Zielordner für neue Termine
    target_folder = RelationChoice(
        title=u"Zielordner für neue Termine",
        description=_(u'Zielordner für neue Termine'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "target_folder",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Folder"],
            #"basePath": '/',
        },
    )
    # Höhe des Kalenders
    calendarHeight = schema.Int(
        title=_(u'Calendar height'),
        description=_(u'Calendar height in pixels'),
        required=False,
    )
    # Bearbeitung von Terminen erlauben
    caleditable = schema.Bool(
        title=_(u'Calendar editable'),
        description=_(u'Check this box if you want the events in the calendar to be editable.'),
        required=False,
    )


@implementer(IFullcalendar)
@adapter(IFullcalendarMarker)
class Fullcalendar(object):
    def __init__(self, context):
        self.context = context

    @property
    def slotMinutes(self):
        if safe_hasattr(self.context, 'slotMinutes'):
            return self.context.slotMinutes
        return None
    @slotMinutes.setter
    def slotMinutes(self, value):
        self.context.slotMinutes = value

    @property
    def allDay(self):
        if safe_hasattr(self.context, 'allDay'):
            return self.context.allDay
        return None
    @slotMinutes.setter
    def allDay(self, value):
        self.context.allDay = value

    @property
    def defaultCalendarView(self):
        if safe_hasattr(self.context, 'defaultCalendarView'):
            return self.context.defaultCalendarView
        return None
    @defaultCalendarView.setter
    def defaultCalendarView(self, value):
        self.context.defaultCalendarView = value

    @property
    def headerLeft(self):
        if safe_hasattr(self.context, 'headerLeft'):
            return self.context.headerLeft
        return None
    @headerLeft.setter
    def headerLeft(self, value):
        self.context.headerLeft = value

    @property
    def headerRight(self):
        if safe_hasattr(self.context, 'headerRight'):
            return self.context.headerRight
        return None
    @headerRight.setter
    def headerRight(self, value):
        self.context.headerRight = value

    @property
    def weekends(self):
        if safe_hasattr(self.context, 'weekends'):
            return self.context.weekends
        return None
    @weekends.setter
    def weekends(self, value):
        self.context.weekends = value

    @property
    def firstDay(self):
        if safe_hasattr(self.context, 'firstDay'):
            return self.context.firstDay
        return None
    @firstDay.setter
    def firstDay(self, value):
        self.context.firstDay = value

    @property
    def firstHour(self):
        if safe_hasattr(self.context, 'firstHour'):
            return self.context.firstHour
        return None
    @firstHour.setter
    def firstHour(self, value):
        self.context.firstHour = value

    @property
    def minTime(self):
        if safe_hasattr(self.context, 'minTime'):
            return self.context.minTime
        return None
    @minTime.setter
    def minTime(self, value):
        self.context.minTime = value

    @property
    def maxTime(self):
        if safe_hasattr(self.context, 'maxTime'):
            return self.context.maxTime
        return None
    @maxTime.setter
    def maxTime(self, value):
        self.context.maxTime = value

    @property
    def target_folder(self):
        if safe_hasattr(self.context, 'target_folder'):
            return self.context.target_folder
        return None
    @target_folder.setter
    def target_folder(self, value):
        self.context.target_folder = value

    @property
    def calendarHeight(self):
        if safe_hasattr(self.context, 'calendarHeight'):
            return self.context.calendarHeight
        return None
    @calendarHeight.setter
    def calendarHeight(self, value):
        self.context.calendarHeight = value

    @property
    def caleditable(self):
        if safe_hasattr(self.context, 'caleditable'):
            return self.context.caleditable
        return None
    @caleditable.setter
    def caleditable(self, value):
        self.context.caleditable = value

