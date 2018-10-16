import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_times(days):
    event_times = []

    for day in days:
        date = parse_date(day.find('span', class_='rec_sched_date').get_text())

        blocks_even = day.find_all('tr', class_="rec_sched_hidden rec_sched_content rec_sched_roweven PublicSwim")
        blocks_odd = day.find_all('tr', class_="rec_sched_hidden rec_sched_content rec_sched_rowodd PublicSwim")

        events = blocks_even + blocks_odd

        for event in events:
            start_time, end_time = parse_time(event.find('th').get_text())
            
            start = convert_to_datetime(start_time, date)
            end = convert_to_datetime(end_time, date)

            swim_type = parse_type(event.find('td').get_text())
            new_event = {
                "state_time": start,
                "end_time": end,
                "swim_type": swim_type
            }

            event_times.append(new_event)

    return event_times

def convert_to_datetime(time, date):
    date_time_string = ' '.join([time, date])

    date_time_object = datetime.strptime(date_time_string, "%I:%M %p %B %d, %Y")

    return date_time_object

def parse_date(date_string):
    date = re.sub('.*DAY ', '', date_string)
    return date

def parse_type(type_string):
    swim_type = type_string.split('\r')
    swim_type = swim_type[0]

    return swim_type


def parse_time(time_string):
    start, end = time_string.split('-')

    start = start.strip()
    end = end.strip()

    return start, end

def get_days(soup):
    public = soup.find_all('div', class_="each_schedule publicswim")

    public = public[0]
    days = public.find_all('tbody')

    return days

def get_page():
    page = requests.get("http://www.calgary.ca/CSPS/Recreation/Pages/Pools/Foothills-schedules.aspx")

    print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup



if __name__ == '__main__':
    soup = get_page()
    days = get_days(soup)
    events = get_times(days)

    for e in events:
        print(e)