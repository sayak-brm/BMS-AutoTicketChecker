#!/usr/bin/env python3
import urllib.request, urllib.error, urllib.parse
import re
import time
import datetime
import os
import sys

from notify_run import Notify
import pytz
from bs4 import BeautifulSoup

class Event:
    def __init__(self, city, pref_venues, movie, date):
        clean_city = []
        for word in city.lower().split():
            clean_city.append(''.join([letter for letter in word if letter.isalnum()]))
        clean_movie = []
        for word in movie.lower().split():
            clean_movie.append(''.join([letter for letter in word if letter.isalnum()]))
        self.city = '-'.join(clean_city)
        self.movie = '-'.join(clean_movie)
        self.date = date
        self.title = None
        self.notify = None
        self.url = ''
        self.shows = None
        self.endpoint = ''
        self.pref_venues = pref_venues

    @staticmethod
    def get_regex_url(url, regex):
        soup = BeautifulSoup(urllib.request.urlopen(url), 'html.parser')
        return soup.find('a', href=re.compile(regex)).attrs['href']

    @staticmethod
    def get_movie_stub(city, movie):
        base_url = 'https://in.bookmyshow.com'
        city_url = base_url + '/' + city
        stub = Event.get_regex_url(city_url, '{}\/movies\/.*{}.*'.format(city.lower(), movie.lower()))
        return stub if stub[0] == '/' else '/' + stub

    @staticmethod
    def get_ticket_url(movie_stub):
        base_url = 'https://in.bookmyshow.com'
        _, city, _, movie_name, movie_id = movie_stub.split('/')
        region_code = Event.get_regex_url(base_url + movie_stub, 'https:\/\/support[.]bookmyshow[.]com\/support\/home[?]regionCode=(\w\w\w\w)')[-4:]
        ticket_url = "https://in.bookmyshow.com/buytickets/{}-{}/movie-{}-{}-MT/".format(movie_name, city, region_code.lower(), movie_id)
        return ticket_url

    @staticmethod
    def get_cities():
        cities = []
        with open('./res/cities.dat', 'r') as dat:
            for city in dat: cities.append(city[:-1])
        return cities

    def config(self):
        import os
        if not os.path.exists('./dat'):
            os.makedirs('./dat')
        date_obj = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
        today = date_obj.strftime('%Y%m%d')
        config_dat = './dat/{}.dat'.format('-'.join([self.city.lower(), self.movie.lower(), *self.pref_venues]))

        if os.path.isfile(config_dat):
            with open(config_dat, 'r') as cfg:
                cfgs = cfg.readline().split(',')
                self.endpoint = cfgs[0]
                self.url = cfgs[1]
                self.notify = Notify(endpoint = self.endpoint)
                self.date = self.date if self.date and int(self.date) >= int(today) else cfgs[2]
                self.date = self.date if int(self.date) >= int(today) else today
        else:
            self.notify = Notify()
            self.endpoint = self.notify.register().endpoint
            stub = self.get_movie_stub(self.city, self.movie)
            self.url = self.get_ticket_url(stub)
            self.date = self.date if self.date and int(self.date) >= int(today) else today

        with open(config_dat, 'w') as cfg:
            cfg.write(','.join([self.endpoint, self.url, self.date]))

    def get_channel(self):
        return self.notify.info().channel_page

    def tickets_available(self):
        return self.title is not None

    def get_shows(self):
        req = urllib.request.Request(self.url)
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')
        shows = str(soup.find_all('div', {'data-online': 'Y'}))
        shows_soup = BeautifulSoup(shows, 'html.parser')
        
        title_element = soup.find(attrs={'class' : 'cinema-name-wrapper'})
        try: self.title = title_element.find('a').text.strip()
        except Exception as ex: self.title = None

        self.shows ={}
        venue_list = str(soup.find('ul', {'id': 'venuelist'}))
        venue_soup = BeautifulSoup(venue_list, 'html.parser')
        for venue in venue_soup.find_all('li'):
            times = str(shows_soup.find_all('a', {'data-venue-code': venue['data-id']}))
            times_soup = BeautifulSoup(times, 'html.parser')
            self.shows[venue['data-id']] = (venue['data-name'], [show_time.text.strip() for show_time in times_soup.findAll(attrs={'data-venue-code' : venue['data-id']})])

    def send_push(self):
        msg = 'Shows for {} is available on {} at a preferred venue! BOOK NOW!'.format(self.title, datetime.datetime.strptime(self.date, '%Y%m%d').strftime('%d/%m/%Y'))
        self.notify.send(msg, self.url)
        return msg

def display_shows(title, shows, pref_venues):
    pref = False if len(pref_venues) > 0 else True
    i = 1
    for venue_id, venue_info in shows.items():
        print('{} {:>2}. {:4}: {}'.format('*' if venue_id in pref_venues else ' ', i, venue_id, venue_info[0]))
        pref = pref or venue_id in pref_venues
        j = 'a'
        for show_time in venue_info[1]:
            print('\t{:>2}) {}'.format(j, show_time))
            j = str(chr(ord(j)+1))
        i += 1
    return pref

def run(city, pref_venues, movie, date):
    movie = Event(city, pref_venues, movie, date)
    try: movie.config()
    except Exception as ex:
        print('Unable to configure event!')
        print("Error: ", str(ex))
        input('Press Enter to exit...')
        sys.exit()

    print("Subscribe to notifications at",movie.get_channel())

    while True:
        try:
            movie.get_shows()
        except Exception as ex:
            print("Error: ", str(ex)) 

        if not movie.tickets_available():
            print("Not available yet")
            time.sleep(300)
        else: break

    print("\n\n##### TICKETS AVAILABLE for {} #####\n".format(movie.title))
    if display_shows(movie.title, movie.shows, pref_venues):
        print('\n{}'.format(movie.send_push()))
    input('\nPress Enter to exit...')
    sys.exit()

if __name__ == '__main__':
    city = input("City: ")
    pref_venues = [venue.strip() for venue in input("Pref. Venues (comma-separated): ").upper().split(',')]
    movie = input("Movie: ")
    date = input("Date (yyyymmdd): ")

    pref_venues = list(filter(None, pref_venues))
    run(city, pref_venues, movie, date)
    
