Changelog
=========

1.4 (unreleased)
----------------

- Upgrade FullCalendar to v6.1.15. Integrate year (multi month) view.
  [kreafox]
- Refactor getting JS variable from Plone Python class method.
  [ksuess]


1.3 (2024-11-29)
----------------

- fix unhashable type: dict in Plone 6.1
  [MrTango]


1.2 (2023-07-04)
----------------

- Remove invalid python_requires.
  [pbauer]
- Add norwegian translation.
  [espenmn]
- Add CSS class for publication class. CSS class will be 'state-published', etc..
  [espenmn]
- Fix: have get_events return recurring events.
  [witch]


1.0b2 (2021-12-11)
------------------

- Fix support for folders.
  [pbauer]

- Support custom collection-types.
  [pbauer]

- Ignore limit and batching in collections.
  [pbauer]

- Do not calculate events twice.
  [pbauer]


1.0b1 (2021-11-22)
------------------

- Make own form for adding new events
  [wkbkhard]

- Fix add-link location
  [pbauer]

- Add setting: custom event type
  [ksuess]

- Fix whole day events
  [ksuess]

- Use default-settings from schema.
  [pbauer]

- Switch view on enable and disable
  [pbauer]

- Remove german phrases
  [wkbkhard]

1.0a3
------------------

- Enhance installation profiles and resources
  [wkbkhard, ksuess]

- Add fullcalendar to collections
  [wkbkhard]

- Adding events over calendar with normal AddForm possible
  [wkbkhard]

1.0a2
------------------

- Changing programming of configuration
  [wkbkhard]

- Disable fullcalendar behavior (still there, but not directly installed)
  [wkbkhard]

- Add fullcalendar interface with AnnotationAdapter with possibility to enable/disable calendar by action
  [wkbkhard]

1.0a1
------------------

- Initial release.
  [wkbkhard]
