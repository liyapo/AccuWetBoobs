# -*- coding: utf-8 -*-

# Copyright(C) 2018      liyapo
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals


from weboob.browser import PagesBrowser, URL
from .pages import WeatherPage, CitySearch

__all__ = ['AccuweatherBrowser']

class AccuweatherBrowser(PagesBrowser):
    BASEURL = 'https://www.accuweather.com'
    city_search = URL('https://api.accuweather.com/locations/v1/cities/autocomplete\?q=(?P<pattern>.*)&apikey=d41dfd5e8a1748d0970cba6637647d96&language=en-us&get_param=value', CitySearch)


   # weather_page = URL('http://www.accuweather.com/en/pays/city/id/daily-weather-forecast/(?P<city_id>.*)', WeatherPage)

    weather_page = URL('en/pays/city/id/current-weather/(?P<city_id>.*)', WeatherPage)

    def iter_city_search(self, pattern):
        return self.city_search.go(pattern=pattern).iter_cities()

    def iter_forecast(self, city_id):
        return self.weather_page.go(city_id=city_id).iter_forecast()

    def get_current(self, city_id):
	return self.weather_page.go(city_id=city_id).get_current()


