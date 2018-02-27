import collections

import datetime
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
        # schedule_url = 'file:///home/techie/Downloads/stuy-weekly-schedule2.html'
        # schedule_url = 'file:///home/techie/Downloads/stuy-weekly-schedule1.txt'

        schedule_page_content = web.get_source(schedule_url, bs4_format=True)
        event_page_snippet = schedule_page_content.find_all(id='event-page')
        self._raise_exception_if_none(event_page_snippet, 'Cannot find snippet on schedule page!')
        self._print_debug_statement('Found event snippet on schedule page!')
        event_description_snippet = event_page_snippet[0].find_all(class_='eventDesc')
        self._raise_exception_if_none(event_description_snippet, 'Cannot find snippet on schedule page!')
        self._print_debug_statement('Found snippet on schedule page!')
        event_description_snippet[0] = re.sub('(\s){2,}', u'', unicode(event_description_snippet[0]))
        trash_pattern = re.compile('<[-\w\d /=:;"\.]+>')
        raw_schedule_data = trash_pattern.sub(u'', unicode(event_description_snippet[0]))
        self._print_debug_statement(raw_schedule_data.replace(u'\n', u''))
        self._print_debug_statement('Found schedule info on schedule page!')
        return raw_schedule_data

    def _get_days_of_breaks(self, raw_schedule_data_string):
        days_of_break = []
        search_start_index = 0
        weekday_raw_pattern = '(monday|tuesday|wednesday|thursday|friday)'
        date_range_pattern = re.compile('{0}[, \w\d]+- *{0},[\w\d ]+'.format(weekday_raw_pattern), re.IGNORECASE)
        for school_closed_match in re.finditer('close', raw_schedule_data_string, re.IGNORECASE):
            date_range_match = date_range_pattern.search(raw_schedule_data_string, search_start_index, school_closed_match.start())
            if date_range_match is None:
                # There are no long breaks, we can handle single day holidays separately
                break
            date_range = date_range_match.group(0)
            search_start_index = school_closed_match.end()
            self._print_debug_statement(date_range)

            raw_start_date, raw_end_date = date_range.split('-')
            current_year = datetime.datetime.today().year
            if re.search('december', raw_start_date, re.IGNORECASE) and re.search('january', raw_end_date, re.IGNORECASE):
                raw_start_date_with_year = '{} {}'.format(raw_start_date.strip(), current_year - 1)
                raw_end_date_with_year = '{} {}'.format(raw_end_date.strip(), current_year)
            else:
                raw_start_date_with_year = '{} {}'.format(raw_start_date.strip(), current_year)
                raw_end_date_with_year = '{} {}'.format(raw_end_date.strip(), current_year)
            parsed_start_date = re.sub(' (\d) ', r' 0\1 ', raw_start_date_with_year)
            parsed_end_date = re.sub(' (\d) ', r' 0\1 ', raw_end_date_with_year)

            start_date = datetime.datetime.strptime(parsed_start_date.title(), '%A, %B %d %Y')
            end_date = datetime.datetime.strptime(parsed_end_date.title(), '%A, %B %d %Y')
            num_of_days_in_range = (end_date - start_date + datetime.timedelta(days=1)).days
            dates_in_range = ['{date:%B} {date.day}'.format(date=start_date + datetime.timedelta(days=offset)) for offset in xrange(num_of_days_in_range)]
            days_of_break.extend(dates_in_range)
        return days_of_break

    def get_schedule_info(self):
        raw_schedule_data = self._get_raw_schedule_data()
        raw_schedule_data_string = raw_schedule_data.replace(u'\xa0', u'')

        days_of_break = self._get_days_of_breaks(raw_schedule_data_string)

        current_date = datetime.datetime.today().date()
        # 0 being Monday
        current_day_of_week = current_date.weekday() % 7
        first_date_of_week = current_date - datetime.timedelta(days=current_day_of_week) - datetime.timedelta(days=0)

        markers_pattern = re.compile('(close|schedule:|science/physical education:)', re.IGNORECASE)
        day_type_pattern = re.compile('(A|B)(\d)*', re.IGNORECASE)
        schedule_info = collections.OrderedDict()
        for offset in xrange(5):
            date_to_search_for = first_date_of_week + datetime.timedelta(days=offset)
            formatted_date = '{date:%B} {date.day}'.format(date=date_to_search_for)
            if formatted_date in days_of_break:
                schedule_type = 'No School'
                day_type = 'No School'
            else:
                date_pattern = re.compile('{date:%B}(\s)*{date.day}'.format(date=date_to_search_for), re.IGNORECASE)
                date_match = date_pattern.search(raw_schedule_data_string)
                if date_match:
                    schedule_type_marker_match = markers_pattern.search(raw_schedule_data_string, date_match.end() + 1)
                    if re.search('close', schedule_type_marker_match.group(0), re.IGNORECASE):
                        schedule_type = 'No School'
                        day_type = 'No School'
                    else:
                        day_type_marker_match = markers_pattern.search(raw_schedule_data_string, schedule_type_marker_match.end())
                        schedule_type = raw_schedule_data_string[schedule_type_marker_match.end():day_type_marker_match.start()].strip()
                        day_type_match = day_type_pattern.search(raw_schedule_data_string, day_type_marker_match.end() + 1)
                        day_type = day_type_match.group(0)
                else:
                    raise WeeklyScheduleScraperException('Cannot find data for date: {}'.format(formatted_date))

            schedule_info[formatted_date] = [schedule_type, day_type]
            self._print_debug_statement('{}: {}'.format(formatted_date, [schedule_type, day_type]))

        self._raise_exception_if_none(schedule_info, 'Cannot find schedule info on schedule page!')
        return schedule_info

if __name__ == '__main__':
    a = WeeklyScheduleScraper('http://stuy.edu', debug=True)
    print a.get_schedule_info()
