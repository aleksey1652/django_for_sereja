from bs4 import BeautifulSoup
import requests
from random import choice
import re, json

from scrapy import get_html
from cat.views_to_admin import *
#from .models import Rentabilitys
from cat.models import USD, Computers

# Rentabilitys

class RivalsData:
    """ Скачиваем цены от конкурентов """

    def __init__(self, url):
        self.url = url

    def __get_data_rivals(self):
        #скачивает сыры данные(страница одного компа) от конкурента
        # и возвращает либо данные либо False
        return get_html(self.url)

    def versum_portal_data(self, name_comp):
        # берем цену из портала
        # выдает tuple: (флоат-цену, комент), комент: ок или назв ошибки

        try:
            comp = Computers.objects.get(name_computers=name_comp)
        except Exception as e:
            return (0, e)
        usd_ = USD.objects.last()
        currency = usd_.usd
        try:
            #rentability_ = Rentabilitys.objects.last().rentability
            #rentability_ = 1 + rentability_ / 100
            rentability_ = usd_.margin if usd_.margin else 1.29
            # новый алгоритм: исп наценку из cat.models
            rentability_comp = comp.class_computers # наценка компа
            rentability_ = rentability_ if not rentability_comp else rentability_comp
            # берем общую наценку из cat.models если нет индивидуальной наценки в компе
        except:
            rentability_ = 1.29
        _, price = get_comp_context(comp.pk)
        price_ua = round(price * currency * rentability_)
        return (price_ua, 'ok')

    def versum_data(self, label1='product-new-price', label2='span'):
        # выдает tuple: (флоат-цену, комент), комент: ок или назв ошибки
        data = self.__get_data_rivals()
        if data:
            soup = BeautifulSoup(data, "html.parser")
            try:
                soup_label1 = soup.find_all(class_=label1)[0]
            except IndexError:
                return (0, label1)
            try:
                soup_label2 = soup_label1.find(label2).get_text()
            except AttributeError:
                return (0, label2)
            try:
                price = float(re.sub(r'\D', '', soup_label2))
            except ValueError:
                return (0, 'float')
            return (price, 'ok')
        return (0, 'status_code')

    def hotline_data(self, label1='many__price-sum orange', label2='span',
                    label3='one__item'):
        # выдает tuple: (флоат-цену, комент), комент: ок или назв ошибки
        data = self.__get_data_rivals()
        if data:
            soup = BeautifulSoup(data, "html.parser")
            try:
                soup_label1 = soup.find_all(class_=label1)[0]
            except IndexError:
                try:
                    soup_label3 = soup.find_all(class_=label3)[0].get_text()
                except (IndexError, AttributeError):
                    return (0, label3)
                try:
                    price = float(re.sub(r'\D', '', soup_label3))
                except ValueError:
                    return (0, 'float')
                return (price, 'ok')
            try:
                soup_label2 = soup_label1.find(label2).get_text()
            except AttributeError:
                return (0, label2)
            try:
                price = float(re.sub(r'\D', '', soup_label2))
            except ValueError:
                return (0, 'float')
            return (price, 'ok')
        return (0, 'status_code')

    def itblok_data(self, label1='price-pp-wrap'):
        # выдает tuple: (флоат-цену, комент), комент: ок или назв ошибки
        data = self.__get_data_rivals()
        if data:
            soup = BeautifulSoup(data, "html.parser")
            try:
                soup_label1 = soup.find_all(class_=label1)[0]
            except IndexError:
                return (0, label1)
            try:
                # берем предпоследнюю цену (код товара последний, 1-может есть может нет)
                price = float(re.findall(r'\d+', soup_label1.get_text())[-2])
            except (ValueError, IndexError):
                return (0, 'float')
            return (price, 'ok')
        return (0, 'status_code')

    def art_data(self, label1='product__price', label2='span'):
        # выдает tuple: (флоат-цену, комент), комент: ок или назв ошибки
        data = self.__get_data_rivals()
        if data:
            soup = BeautifulSoup(data, "html.parser")
            try:
                soup_label1 = soup.find_all(class_=label1)[0]
            except IndexError:
                return (0, label1)
            try:
                soup_label2 = soup_label1.find(label2).get_text()
            except AttributeError:
                return (0, label2)
            try:
                price = float(re.sub(r'\D', '', soup_label2))
            except ValueError:
                return (0, 'float')
            return (price, 'ok')
        return (0, 'status_code')

    def compx_data(self, label1='product-price-wrapper', label2='product__price d-lg-none',
                    label3='product__special-price d-lg-none'):
        # выдает tuple: (флоат-цену, комент), комент: ок или назв ошибки
        data = self.__get_data_rivals()
        if data:
            soup = BeautifulSoup(data, "html.parser")
            try:
                soup_label1 = soup.find_all(class_=label1)[0]
            except IndexError:
                return (0, label1)
            try:
                soup_label2 = soup_label1.find(class_=label2).get_text()
            except AttributeError:
                # если акционная цена
                try:
                    soup_label2 = soup_label1.find(class_=label3).get_text()
                except AttributeError:
                    return (0, label3)
            try:
                price = float(re.sub(r'\D', '', soup_label2))
            except ValueError:
                return (0, 'float')
            return (price, 'ok')
        return (0, 'status_code')

    def telemart_data(self, label1='card-block__price-summ', label2=None):
        # выдает tuple: (флоат-цену, комент), комент: ок или назв ошибки
        data = self.__get_data_rivals()
        if data:
            soup = BeautifulSoup(data, "html.parser")
            try:
                soup_label1 = soup.find_all(class_=label1)[0]
            except IndexError:
                return (0, label1)
            try:
                soup_label2 = soup_label1.get_text()
            except AttributeError:
                return (0, 'get_text')
            try:
                price = float(re.sub(r'\D', '', soup_label2))
            except ValueError:
                return (0, 'float')
            return (price, 'ok')
        return (0, 'status_code')
