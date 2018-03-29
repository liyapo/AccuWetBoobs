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

from datetime import date

from weboob.browser.pages import JsonPage, HTMLPage
from weboob.browser.elements import ItemElement, ListElement, DictElement, method
from weboob.capabilities.base import NotAvailable
from weboob.capabilities.weather import Forecast, Current, City, Temperature
from weboob.browser.filters.json import Dict
from weboob.browser.filters.standard import CleanText, CleanDecimal, Regexp, Format, Eval


class CitySearch(JsonPage):

    @method
    class iter_cities(DictElement):
        ignore_duplicate = True

        class item(ItemElement):
            klass = City

            #def condition(self):
             #   return Dict('type')(self) == "VILLE_FRANCE"

            obj_id = Dict('Key')
            obj_name = Format(u'%s %s %s', Dict('LocalizedName'), Dict['AdministrativeArea']['ID'], Dict['Country']['LocalizedName'])


class WeatherPage(HTMLPage):
    @method
    class iter_forecast(ListElement):
        item_xpath = '//*[@id="panel-main"]//div[@id="feed-tabs"]/ul/li'

        class item(ItemElement):
            klass = Forecast
		
	    obj_id = CleanText('./div/h4')
            obj_date = CleanText('./div/h4')
            '''def obj_date(self):
                actual_day_number = Eval(int,
                                         Regexp(CleanText('./dl/dt'),
                                                '\w{3} (\d+)'))(self)
                base_date = date.today()
                if base_date.day > actual_day_number:
                    base_date = base_date.replace(
                        month=(
                            (base_date.month + 1) % 12
                        )
                    )
                base_date = base_date.replace(day=actual_day_number)
                return base_date'''


	    def obj_low(self):
                temp = 4 #CleanDecimal('.//span[@class="small-temp"]')
                         
                #if temp != "-":  # Sometimes website does not return low
                #    temp = CleanDecimal(temp)(self)
                unit = u'C' #Regexp(CleanText('//*[@id="current-city-tab"]//span[@class="local-temp"]'), u'.*\xb0(\w)')(self)
                return Temperature(float(temp), unit)
               # return NotAvailable

            def obj_high(self):
                temp = 7 #CleanDecimal('.//span[@class="large-temp"]')(self)
               # if temp != "-":  # Sometimes website does not return high
               #     temp = CleanDecimal(temp)(self)
                unit = u'C' #Regexp(CleanText('//*[@id="current-city-tab"]//span[@class="local-temp"]'), u'.*\xb0(\w)')(self)
                return Temperature(float(temp), unit)
                #return NotAvailable

            obj_text = CleanText('.//span[@class="cond"]')

    @method
    class get_current(ItemElement):
        klass = Current
        obj_date = date.today()

        real_feel_temp = CleanDecimal('//*[@id="detail-now"]//span[@class="small-temp"]')
	temp_units = Regexp(CleanText('//*[@id="current-city-tab"]//span[@class="local-temp"]'), u'.*\xb0(\w)')

	description = CleanText('//*[@id="detail-now"]//span[@class="cond"]')
	wind_cond = CleanText('//*[@id="detail-now"]//li[@class="wind"]')
	humidity = CleanText('//*[@id="detail-now"]//ul[@class="stats"]/li[3]')
	
                             
	obj_text = Format(u'Real feel: %s \xb0%s - %s - %s - %s',  

           		real_feel_temp,
			temp_units,
			description, 
			wind_cond, 
			humidity)

        def obj_temp(self):
            temp = CleanDecimal('//*[@id="current-city-tab"]//span[@class="local-temp"]')(self)
            unit = Regexp(CleanText('//*[@id="current-city-tab"]//span[@class="local-temp"]'), u'.*\xb0(\w)')(self) 
            return Temperature(float(temp), unit)


