# -*- coding: utf-8 -*-
from collective.fullcalendar import _
from plone.app.event import base
from plone.app.event.base import AnnotationAdapter
from collective.fullcalendar.interfaces import IFullcalenderEnabled
from plone.folder.interfaces import IFolder
from plone.z3cform.layout import FormWrapper
from Products.Five.browser import BrowserView
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import noLongerProvides


class IFullcalenderSettings(Interface):

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


@adapter(IFolder)
@implementer(IFullcalenderSettings)
class IFullcalenderSettings(AnnotationAdapter):
    """Annotation Adapter for IFullcalenderSettings.
    """
    ANNOTATION_KEY = "fullcalender_settings"


class IFullcalenderSettingsForm(form.Form):
    fields = field.Fields(IFullcalenderSettings)
    ignoreContext = False


class IFullcalenderTool(BrowserView):

    @property
    def available(self):
        return IFolder.providedBy(self.context)

    @property
    def available_disabled(self):
        return self.available and not self.enabled

    @property
    def enabled(self):
        return IFullcalenderEnabled.providedBy(self.context)


class IFullcalenderSettingsFormView(FormWrapper):
    form = IFullcalenderSettingsForm

    def enable(self):
        """Enable icalendar import on this context.
        """
        alsoProvides(self.context, IFullcalenderEnabled)
        self.context.reindexObject(idxs=('object_provides'))
        self.request.response.redirect(self.context.absolute_url())

    def disable(self):
        """Disable icalendar import on this context.
        """
        noLongerProvides(self.context, IFullcalenderEnabled)
        self.context.reindexObject(idxs=('object_provides'))
        self.request.response.redirect(self.context.absolute_url())
