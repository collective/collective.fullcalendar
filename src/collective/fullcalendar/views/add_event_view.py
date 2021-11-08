# -*- coding: utf-8 -*-
from plone.dexterity.browser import add


class AddForm(add.DefaultAddForm):
    portal_type = 'Event'

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        infos = self.request

        if 'date' in infos:
            self.widgets['IEventBasic.start'].value = infos['date']
            self.widgets['IEventBasic.end'].value = infos['date']

        if 'start' in infos and 'end' in infos:
            self.widgets['IEventBasic.start'].value = infos['start']
            self.widgets['IEventBasic.end'].value = infos['end']

        if 'allDay' in infos and infos['allDay'] == 'true':
            self.widgets['IEventBasic.whole_day'].value = ('selected',)


class AddView(add.DefaultAddView):
    form = AddForm