# -*- coding: utf-8 -*-

cont_set = set(['news', 'music'])
days_set = set(['never', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])


class Settings(object):
    # class for storing configuration

    def __init__(self):
        self._alarm_time = '0'
        self._last_modified = '0'
        self._content = 'news'
        self._days = 'never'
        self._alarm_active = '0'
        self._individual_message = '0'
        self._text = '0'
        self._volume = '0'

    def fill_with_default_values(self):
        self._alarm_time = '13:00'
        self._content = 'news'
        self._days = 'monday'
        self._alarm_active = '0'
        self._individual_message = '.'
        self._text = '.'
        self._volume = '50'

    def get_alarm_time(self): return self._alarm_time

    def set_alarm_time(self, value): self._alarm_time = value

    def get_last_modified(self): return self._last_modified

    def set_last_modified(self, value): self._last_modified = value

    def get_content(self): return self._content

    def set_content(self, value):
        assert value in cont_set
        self._content = value

    def get_days(self): return self._days

    def set_days(self, value):
        assert value in days_set
        self._days = value

    def get_alarm_active(self): return self._alarm_active

    def set_alarm_active(self, value): self._alarm_active = value

    def get_individual_message(self): return self._individual_message

    def set_individual_message(self, value): self._individual_message = value

    def get_text(self): return self._text

    def set_text(self, value): self._text = value

    def get_volume(self): return self._volume

    def set_volume(self, value): self._volume = value

    alarm_time = property(get_alarm_time, set_alarm_time)
    last_modified = property(get_last_modified, set_last_modified)
    content = property(get_content, set_content)
    days = property(get_days, set_days)
    alarm_active = property(get_alarm_active, set_alarm_active)
    individual_message = property(get_individual_message, set_individual_message)
    text = property(get_text, set_text)
    volume = property(get_volume, set_volume)
