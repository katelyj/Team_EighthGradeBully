import re

from lib.utils import web

class WeeklyScheduleScraperException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class WeeklyScheduleScraper(object):

    def __init__(self, url, debug=False):
        self.url = url
        self.debug = debug

    def _print_debug_statement(self, message):
        if self.debug:
            print message

    def _raise_exception_if_none(self, item, message):
        if not item:
            raise WeeklyScheduleScraperException(message)

    def get_schedule_link(self):
        soup = web.get_source(self.url, bs4_format=True)
        table_snippets = soup.find_all('table')
        self._raise_exception_if_none(table_snippets, 'Cannot find snippet in homepage!')

        self._print_debug_statement('Found table snippet in homepage!')
        interested_table = table_snippets[0]
        table_links = interested_table.find_all('a')

        pattern = re.compile('[Ww]eekly [Ss]chedule')
        schedule_link = None
        for link in table_links:
            displayed_text = link.get_text()
            if pattern.search(displayed_text):
                schedule_link = link
        self._raise_exception_if_none(schedule_link, 'Cannot find schedule link!')
        self._print_debug_statement('Found schedule link!')
        return schedule_link.get('href')

    def _get_raw_schedule_data(self):
        schedule_url = self.get_schedule_link()
        schedule_page_content = web.get_source(schedule_url, bs4_format=True)
        event_page_snippet = schedule_page_content.find_all(id='event-page')
        self._raise_exception_if_none(event_page_snippet, 'Cannot find snippet on schedule page!')
        self._print_debug_statement('Found event snippet on schedule page!')
        event_description_snippet = event_page_snippet[0].find_all(class_='eventDesc')
        self._raise_exception_if_none(event_description_snippet, 'Cannot find snippet on schedule page!')
        self._print_debug_statement('Found snippet on schedule page!')
        trash_pattern = re.compile('<[-\w\d /=:;"\.]+>')
        raw_schedule_data = trash_pattern.sub(u'', unicode(event_description_snippet[0]))
        self._print_debug_statement(raw_schedule_data)
        self._print_debug_statement('Found schedule info on schedule page!')
        return raw_schedule_data

    def get_schedule_info(self):
        raw_schedule_data = self._get_raw_schedule_data()
        raw_schedule_data_string = raw_schedule_data.replace(u'\xa0', u'')

        MARKERS = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', '$']
        parsed_schedule_info = {}
        schedule_type_pattern = re.compile('(?<=Schedule:)(.*?)(?=Science)')
        day_type_pattern = re.compile('(([12\w]+)($|[Mm][Oo][Nn][Dd][Aa][Yy]))')
        for index in xrange(len(MARKERS) - 1):
            pattern = re.compile('({}.*?)(?={})'.format(MARKERS[index], MARKERS[index + 1]))
            matcher = pattern.search(raw_schedule_data_string)
            if matcher:
                snippet = matcher.group(1)
                print snippet

                raw_schedule_type = schedule_type_pattern.search(snippet)
                self._raise_exception_if_none(raw_schedule_type, 'Could not find schedule type')
                self._print_debug_statement('Found schedule type for {}: {}'.format(MARKERS[index].title(), raw_schedule_type.group(1)))
                parsed_schedule_type = raw_schedule_type.group(1)

                raw_day_type = day_type_pattern.search(snippet)
                self._raise_exception_if_none(raw_day_type, 'Could not find day type')
                self._print_debug_statement('Found day type for {}: {}'.format(MARKERS[index].title(), raw_day_type.group(2)))
                parsed_day_type = raw_day_type.group(2)

                parsed_schedule_info[MARKERS[index].title()] = [str(parsed_schedule_type.strip()), str(parsed_day_type)]
            else:
                raise WeeklyScheduleScraperException('Raw schedule data has invalid format!')

        self._raise_exception_if_none(parsed_schedule_info, 'Cannot find schedule info on schedule page!')
        return parsed_schedule_info

if __name__ == '__main__':
    a = WeeklyScheduleScraper('http://stuy.edu', debug=True)
    print a.get_schedule_info()
