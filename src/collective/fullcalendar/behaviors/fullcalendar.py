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
from zope.schema.vocabulary import SimpleVocabulary


class IFullcalendarMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IFullcalendar(model.Schema):
    """
    """
    slotMinutes = schema.Int(
        title=_(u'Slot length'),
        description=_(u'Slot length in minutes'),
        required=False,
    )
    allDay = schema.Bool(
        title=_(u'Full day'),
        description=_(u'Display \"All day\" option'),
        required=False,
    )
    #views_items = [
    #    ('day', u'Day'),
    #    ('week', u'Week'),
    #    ('month', u'Month'),
    #]
    #views_terms = [SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in views_items]
    #views_vocabulary = SimpleVocabulary(views_terms)
    #views_vocabulary = SimpleVocabulary.fromValues(['day','week','month'])
    defaultCalendarView = schema.Choice(
        title=_(u'Standard-Ansicht'),
        description=_(u'Standard-Ansicht'),
        required=False,
        vocabulary=SimpleVocabulary.fromValues(['day','week','month'])
    )
    headerLeft = schema.List(
        title=_(u'Kopfbereich links'),
        description=_(u'Kopfbereich links'),
        required=False,
        value_type=schema.Choice(vocabulary=SimpleVocabulary.fromValues(['prev','next']))
    )
    headerRight = schema.List(
        title=_(u'Kopfbereich rechts'),
        description=_(u'Kopfbereich rechts'),
        required=False,
        value_type=schema.Choice(vocabulary=SimpleVocabulary.fromValues(['prev','next']))
    )
    weekends = schema.Bool(
        title=_(u'Wochenenden anzeigen'),
        description=_(u'Wochenenden anzeigen'),
        required=False,
    )
    firstDay = schema.Choice(
        title=_(u'Erster Wochentag'),
        description=_(u'Erster Wochentag'),
        required=False,
        vocabulary=SimpleVocabulary.fromValues(['monday','tuesday','wednesday','thursday','friday','saturday','sunday'])
    )
    firstDay = schema.TextLine(
        title=_(u'Erste angezeigte Stunde'),
        description=_(u'Erste angezeigte Stunde'),
        required=False,
    )
    minTime = schema.TextLine(
        title=_(u'Erste sichtbare Stunde'),
        description=_(u'Erste sichtbare Stunde'),
        required=False,
    )
    maxTime = schema.TextLine(
        title=_(u'Letzte sichtbare Stunde'),
        description=_(u'Letzte sichtbare Stunde'),
        required=False,
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
    def project(self):
        if safe_hasattr(self.context, 'project'):
            return self.context.project
        return None

    @project.setter
    def project(self, value):
        self.context.project = value
