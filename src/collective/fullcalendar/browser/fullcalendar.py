# -*- coding: utf-8 -*-
from collective.fullcalendar import _
from plone.app.event import base
from plone.app.event.base import AnnotationAdapter
from collective.fullcalendar.interfaces import IFullcalenderEnabled
from plone.folder.interfaces import IFolder
from plone.app.contenttypes.interfaces import ICollection
from plone.z3cform.layout import FormWrapper
from Products.Five.browser import BrowserView
from z3c.form import field
from z3c.form import form
from z3c.form import button
from zope import schema
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import noLongerProvides

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from z3c.relationfield.schema import RelationChoice
from plone.autoform import directives
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from Products.statusmessages.interfaces import IStatusMessage


class IIFullcalenderSettings(Interface):

    slotMinutes = schema.Int(
        title=_(
            u'label_slot_length',
            default=u'Slot length'),
        description=_(
            u'help_slot_length',
            default=u'Slot length in minutes'
        ),
        required=True,
        default=30
    )
    allDay = schema.Bool(
        title=_(
            u'label_allDay',
            default=u'All day'
        ),
        description=_(
            u'help_allDay',
            default=u'Display \"All day\" option for timeGridWeek-View'
        ),
        required=False,
        default=True
    )
    defaultCalendarView = schema.Choice(
        title=_(
            u'label_defaultCalendarView',
            default=u'Standard View'
        ),
        description=_(
            u'help_defaultCalendarView',
            default=u'Standard View'
        ),
        required=True,
        vocabulary=SimpleVocabulary.fromValues(['dayGridMonth', 'timeGridWeek', 'listWeek', 'dayGridWeek']),
        default='dayGridMonth'
    )
    # Possible for headerLeft/headerRight: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek
    headerLeft = schema.TextLine(
        title=_(
            u'label_headerLeft',
            default=u'Kopfbereich links'
        ),
        description=_(
            u'help_headerLeft',
            default=u'Mögliche Werte: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek'
        ),
        required=False,
        default='prev,next today'
    )
    headerRight = schema.TextLine(
        title=_(
            u'label_headerRight',
            default=u'Kopfbereich rechts'
        ),
        description=_(
            u'help_headerRight',
            default=u'Mögliche Werte: title, prev, next, prevYear, nextYear, today, dayGridMonth, timeGridWeek, listWeek, dayGridWeek'
        ),
        required=False,
        default='dayGridMonth timeGridWeek listWeek'
    )
    weekends = schema.Bool(
        title=_(
            u'label_weekends',
            default=u'Wochenenden anzeigen'
        ),
        description=_(
            u'help_weekends',
            default=u'Wochenenden anzeigen'
        ),
        required=False,
        default=True
    )
    firstDay = schema.Choice(
        title=_(
            u'label_firstDay',
            default=u'Erster Wochentag'
        ),
        description=_(
            u'help_firstDay',
            default=u'Erster Wochentag'
        ),
        required=True,
        vocabulary=SimpleVocabulary([SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in [(0, u'sunday'), (1, u'monday'), (2, u'tuesday'), (3, u'wednesday'), (4, u'thursday'), (5, u'friday'), (6, u'saturday')]]),
        default=1
    )
    firstHour = schema.TextLine(
        title=_(
            u'label_firstHour',
            default=u'Erste angezeigte Stunde'
        ),
        description=_(
            u'help_firstHour',
            default=u'Legen Sie die anfängliche Scrollposition der Kalender-Tagesansicht fest (eine Zahl zwischen 0 und 23). Wenn vor dieser Zahl ein "+" oder "-" steht, wird die Zahl mit der aktuellen Zeit addiert bzw. substrahiert.'
        ),
        required=True,
        default='6'
    )
    minTime = schema.TextLine(
        title=_(
            u'label_minTime',
            default=u'Erste sichtbare Stunde'
        ),
        description=_(
            u'help_minTime',
            default=u'Wählen Sie die erste sichtbare Stunde des Kalenders (z.B. \'5\' oder \'5:30\').'
        ),
        required=True,
        default='00:00:00'
    )
    maxTime = schema.TextLine(
        title=_(
            u'label_maxTime',
            default=u'Letzte sichtbare Stunde'
        ),
        description=_(
            u'help_maxTime',
            default=u'Wählen Sie die letzte sichtbare Stunde des Kalenders (z.B. \'5\' oder \'5:30\').'
        ),
        required=True,
        default='24:00:00'
    )
    # Zielordner für neue Termine
    target_folder = RelationChoice(
        title=_(
            u'label_target_folder',
            default=u'Zielordner für neue Termine'
        ),
        description=_(
            u'help_target_folder',
            default=u'Zielordner für neue Termine'
        ),
        vocabulary='plone.app.vocabularies.Catalog',
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
    # Höhe des Kalenders
    calendarHeight = schema.Int(
        title=_(
            u'label_calendarHeight',
            default=u'Calendar height'
        ),
        description=_(
            u'help_calendarHeight',
            default=u'Calendar height in pixels'
        ),
        required=False,
    )
    # Bearbeitung von Terminen erlauben
    caleditable = schema.Bool(
        title=_(
            u'label_caleditable',
            default=u'Calendar editable'
        ),
        description=_(
            u'help_caleditable',
            default=u'Check this box if you want the events in the calendar to be editable.'
        ),
        required=False,
    )


@adapter(ICollection)
@adapter(IFolder)
@implementer(IIFullcalenderSettings)
class IFullcalenderSettings(AnnotationAdapter):
    """Annotation Adapter for IIFullcalenderSettings.
    """
    ANNOTATION_KEY = "fullcalender_settings"


class FullcalenderSettingsForm(form.EditForm):
    fields = field.Fields(IIFullcalenderSettings)
    ignoreContext = False

    label = _(u"Edit fullcalender settings")

    @button.buttonAndHandler(_(u"Save"), name='save')
    def handleSave(self, action):  # NOQA
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes saved."),
            "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes canceled."),
            "info")
        self.request.response.redirect("%s/%s" % (
            self.context.absolute_url(),
            '@@fullcalender_settings'))


class IFullcalenderTool(BrowserView):

    @property
    def available(self):
        return (IFolder.providedBy(self.context) or ICollection.providedBy(self.context))

    @property
    def available_disabled(self):
        return self.available and not self.enabled

    @property
    def enabled(self):
        return IFullcalenderEnabled.providedBy(self.context)


class FullcalenderSettingsFormView(FormWrapper):
    form = FullcalenderSettingsForm

    def enable(self):
        """Enable fullcalendar import on this context.
        """
        alsoProvides(self.context, IFullcalenderEnabled)
        self.context.reindexObject(idxs=('object_provides'))
        # TODO: save default calendar settings in annotation
        # TODO: enable fullcalendar view
        self.request.response.redirect(self.context.absolute_url())

    def disable(self):
        """Disable fullcalendar import on this context.
        """
        noLongerProvides(self.context, IFullcalenderEnabled)
        self.context.reindexObject(idxs=('object_provides'))
        # TODO: delete calendar settings annotation
        # TODO: unset fullcalendar view
        self.request.response.redirect(self.context.absolute_url())
