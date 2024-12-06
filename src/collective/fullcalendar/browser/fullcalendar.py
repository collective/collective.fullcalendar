# -*- coding: utf-8 -*-
from collective.fullcalendar import _
from collective.fullcalendar.interfaces import IFullcalendarEnabled
from plone.app.contenttypes.behaviors.collection import ISyndicatableCollection
from plone.app.event.base import AnnotationAdapter
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.interfaces import IDexterityContainer
from plone.z3cform.layout import FormWrapper
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button, field, form
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import noLongerProvides
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


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
            [
                "dayGridMonth",
                "timeGridWeek",
                "listWeek",
                "dayGridWeek",
                "multiMonthYear",
            ]
        ),
        default="dayGridMonth",
    )
    # Possible for headerLeft/headerRight: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek
    headerLeft = schema.TextLine(
        title=_(u"label_headerLeft", default=u"Head area left"),
        description=_(
            u"help_headerLeft",
            default=u"Possible values: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek, multiMonthYear",
        ),
        required=False,
        default="prev,next today",
    )
    headerRight = schema.TextLine(
        title=_(u"label_headerRight", default=u"Head area right"),
        description=_(
            u"help_headerRight",
            default=u"Possible values: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek, multiMonthYear",
        ),
        required=False,
        default="dayGridMonth timeGridWeek listWeek multiMonthYear",
    )
    weekends = schema.Bool(
        title=_(u"label_weekends", default=u"Show weekends"),
        description=_(u"help_weekends", default=u"Show weekends"),
        required=False,
        default=True,
    )
    firstDay = schema.Choice(
        title=_(u"label_firstDay", default=u"First day of the week"),
        description=_(u"help_firstDay", default=u"Choose the first day of the week."),
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
        title=_(u"label_firstHour", default=u"First visible hour"),
        description=_(
            u"help_firstHour",
            default=u'Set the starting calendar day view scroll position (a number between 0 and 23). If there is a "+" or "-" in front of this number, the number is added or subtracted with the current time.',
        ),
        required=True,
        default="6",
    )
    minTime = schema.TextLine(
        title=_(u"label_minTime", default=u"First visible hour"),
        description=_(
            u"help_minTime",
            default=u"Select the first visible hour of the calendar (e.g. '5' or '5:30').",
        ),
        required=True,
        default="00:00:00",
    )
    maxTime = schema.TextLine(
        title=_(u"label_maxTime", default=u"Last visible hour"),
        description=_(
            u"help_maxTime",
            default=u"Select the last visible hour of the calendar (e.g. '5' oder '5:30').",
        ),
        required=True,
        default="24:00:00",
    )
    # Target for new events
    target_folder = RelationChoice(
        title=_(
            u"label_target_folder", default=u"Destination folder for new appointments"
        ),
        description=_(
            u"help_target_folder", default=u"Destination folder for new appointments"
        ),
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
    # Height of Calendar
    calendarHeight = schema.Int(
        title=_(u"label_calendarHeight", default=u"Calendar height"),
        description=_(u"help_calendarHeight", default=u"Calendar height in pixels"),
        required=False,
    )
    # Enable editing on events
    caleditable = schema.Bool(
        title=_(u"label_caleditable", default=u"Calendar editable"),
        description=_(
            u"help_caleditable",
            default=u"Check this box if you want the events in the calendar to be editable.",
        ),
        required=False,
        default=False,
    )


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
    def available(self):
        return IDexterityContainer.providedBy(
            self.context
        ) or ISyndicatableCollection.providedBy(self.context)

    def available_disabled(self):
        return self.available() and not self.enabled()

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
