# -*- coding: utf-8 -*-
from collective.fullcalendar import _
from collective.fullcalendar.interfaces import IFullcalendarEnabled
from plone.app.contenttypes.interfaces import ICollection
from plone.app.event.base import AnnotationAdapter
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.folder.interfaces import IFolder
from plone.z3cform.layout import FormWrapper
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button, field, form
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.component import adapter, provideAdapter
from zope.interface import alsoProvides, implementer, Interface, noLongerProvides
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.annotation.interfaces import IAnnotations
from zope.annotation import factory


class IIFullcalendarSettings(Interface):

    slotMinutes = schema.Int(
        title=_(u"label_slot_length", default=u"Slot length"),
        description=_(u"help_slot_length", default=u"Slot length in minutes"),
        required=True,
        default=30,
    )
    allDay = schema.Bool(
        title=_(u"label_allDay", default=u"All day"),
        description=_(
            u"help_allDay", default=u'Display "All day" option for timeGridWeek-View'
        ),
        required=False,
        default=True,
    )
    defaultCalendarView = schema.Choice(
        title=_(u"label_defaultCalendarView", default=u"Standard View"),
        description=_(u"help_defaultCalendarView", default=u"Standard View"),
        required=True,
        vocabulary=SimpleVocabulary.fromValues(
            ["dayGridMonth", "timeGridWeek", "listWeek", "dayGridWeek"]
        ),
        default="dayGridMonth",
    )
    # Possible for headerLeft/headerRight: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek
    headerLeft = schema.TextLine(
        title=_(u"label_headerLeft", default=u"Kopfbereich links"),
        description=_(
            u"help_headerLeft",
            default=u"Mögliche Werte: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek",
        ),
        required=False,
        default="prev,next today",
    )
    headerRight = schema.TextLine(
        title=_(u"label_headerRight", default=u"Kopfbereich rechts"),
        description=_(
            u"help_headerRight",
            default=u"Mögliche Werte: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek",
        ),
        required=False,
        default="dayGridMonth timeGridWeek listWeek",
    )
    weekends = schema.Bool(
        title=_(u"label_weekends", default=u"Wochenenden anzeigen"),
        description=_(u"help_weekends", default=u"Wochenenden anzeigen"),
        required=False,
        default=True,
    )
    firstDay = schema.Choice(
        title=_(u"label_firstDay", default=u"Erster Wochentag"),
        description=_(u"help_firstDay", default=u"Erster Wochentag"),
        required=True,
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
                for pair in [
                    (0, u"sunday"),
                    (1, u"monday"),
                    (2, u"tuesday"),
                    (3, u"wednesday"),
                    (4, u"thursday"),
                    (5, u"friday"),
                    (6, u"saturday"),
                ]
            ]
        ),
        default=1,
    )
    firstHour = schema.TextLine(
        title=_(u"label_firstHour", default=u"Erste angezeigte Stunde"),
        description=_(
            u"help_firstHour",
            default=u'Legen Sie die anfängliche Scrollposition der Kalender-Tagesansicht fest (eine Zahl zwischen 0 und 23). Wenn vor dieser Zahl ein "+" oder "-" steht, wird die Zahl mit der aktuellen Zeit addiert bzw. substrahiert.',
        ),
        required=True,
        default="6",
    )
    minTime = schema.TextLine(
        title=_(u"label_minTime", default=u"Erste sichtbare Stunde"),
        description=_(
            u"help_minTime",
            default=u"Wählen Sie die erste sichtbare Stunde des Kalenders (z.B. '5' oder '5:30').",
        ),
        required=True,
        default="00:00:00",
    )
    maxTime = schema.TextLine(
        title=_(u"label_maxTime", default=u"Letzte sichtbare Stunde"),
        description=_(
            u"help_maxTime",
            default=u"Wählen Sie die letzte sichtbare Stunde des Kalenders (z.B. '5' oder '5:30').",
        ),
        required=True,
        default="24:00:00",
    )
    # Target for new events
    target_folder = RelationChoice(
        title=_(u"label_target_folder", default=u"Zielordner für neue Termine"),
        description=_(u"help_target_folder", default=u"Zielordner für neue Termine"),
        vocabulary="plone.app.vocabularies.Catalog",
        required=False,
    )
    directives.widget(
        "target_folder",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Folder"],
            # "basePath": '/',
        },
    )
    event_type = schema.Choice(
        title=_(u"event_type", default=u"Event content_type to add"),
        description=_(
            u"help_event_type",
            default=u"Or leave blank for default event type 'Event'.",
        ),
        vocabulary="plone.app.vocabularies.PortalTypes",
        required=False,
        default="Event",
    )
    # Höhe des Kalenders
    calendarHeight = schema.Int(
        title=_(u"label_calendarHeight", default=u"Calendar height"),
        description=_(u"help_calendarHeight", default=u"Calendar height in pixels"),
        required=False,
    )
    # Bearbeitung von Terminen erlauben
    caleditable = schema.Bool(
        title=_(u"label_caleditable", default=u"Calendar editable"),
        description=_(
            u"help_caleditable",
            default=u"Check this box if you want the events in the calendar to be editable.",
        ),
        required=False,
        default=False,
    )


@adapter(ICollection)
@adapter(IFolder)
@implementer(IIFullcalendarSettings)
class IFullcalendarSettings(AnnotationAdapter):
    """Annotation Adapter for IIFullcalendarSettings."""

    ANNOTATION_KEY = "fullcalendar_settings"


class FullcalendarSettingsForm(form.EditForm):
    fields = field.Fields(IIFullcalendarSettings)
    ignoreContext = False

    label = _(u"Edit fullcalendar settings")

    @button.buttonAndHandler(_(u"Save"), name="save")
    def handleSave(self, action):  # NOQA
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."), "info")
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u"Cancel"), name="cancel")
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Changes canceled."), "info")
        self.request.response.redirect(
            "%s/%s" % (self.context.absolute_url(), "@@fullcalendar_settings")
        )


class IFullcalendarTool(BrowserView):
    @property
    def available(self):
        return IFolder.providedBy(self.context) or ICollection.providedBy(self.context)

    @property
    def available_disabled(self):
        return self.available and not self.enabled

    @property
    def enabled(self):
        return IFullcalendarEnabled.providedBy(self.context)


class FullcalendarSettingsFormView(FormWrapper):
    form = FullcalendarSettingsForm

    def enable(self):
        """Enable fullcalendar on this context."""
        alsoProvides(self.context, IFullcalendarEnabled)
        self.context.reindexObject(idxs=("object_provides"))
        annotations = IAnnotations(self.context)
        if "fullcalendar_settings" not in annotations:
            # get the default-setting from the schema
            default_settings = {}
            for key, field in IIFullcalendarSettings.namesAndDescriptions():
                default_settings[key] = field.default
            annotations["fullcalendar_settings"] = default_settings
        self.context.setLayout("fullcalendar-view")
        self.request.response.redirect(self.context.absolute_url())

    def disable(self):
        """Disable fullcalendar on this context."""
        noLongerProvides(self.context, IFullcalendarEnabled)
        self.context.reindexObject(idxs=("object_provides"))
        annotations = IAnnotations(self.context)
        del annotations["fullcalendar_settings"]
        self.context.manage_delProperties(["layout"])
        self.request.response.redirect(self.context.absolute_url())
