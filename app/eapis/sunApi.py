# -*- coding: utf-8 -*-
import json
import urllib
from bs4 import BeautifulSoup
import logging
import endpoints
from protorpc import messages, message_types, remote
__author__ = 'haopd'
_logger = logging.getLogger(__name__)


class DataRequest(messages.Message):
    data = messages.StringField(1)


@endpoints.api(name='change_url', version='v1')
class SunApi(remote.Service):
    """ URL API
    """
    @endpoints.method(
        DataRequest,
        message_types.VoidMessage,
        name='sunapi',)

    def recive_data(self, request):
        logging.info(request.data)
        data = {}
        soup = BeautifulSoup(request.data, 'html.parser')
        trs = soup.find_all("tr")
        for i in range(2,len(trs)-1):
            tr = BeautifulSoup(str(trs[i]),'html.parser')
            tds = tr.find_all("td")
            campaign_title = tds[2].find_all("a")[0].text
            campaign_href = tds[2].find_all("a")[0].get('href')
            campaign_sold = int(tds[4].text)
            try:
                campaign_affiliate = float((tds[7].text).replace("$", ""))
            except:
                campaign_affiliate = 0
            try:
                campaign_artist = float((tds[8].text).replace("$", ""))
            except:
                campaign_artist = 0
            campaign_datas = [campaign_sold, campaign_affiliate, campaign_artist]
            if campaign_title in data:
                old_data = data[campaign_title]
                new_data = [old_data[0]+campaign_sold, old_data[1]+campaign_affiliate, old_data[2]+campaign_artist]
                data[campaign_title] = new_data
            else:
                data[campaign_title] = campaign_datas
        self.pushDataToGoogleSheet(data)
        return message_types.VoidMessage()

    def pushDataToGoogleSheet(self, data):
        import gae_sheet
        if data:
            url = "https://docs.google.com/spreadsheets/d/1X6XfgRzkMgig_E7C26U6MQa9uxiWiWDdaHIaFhqj5wY/edit#gid=0"
            for k, v in data.items():
                gae_sheet.run(k, v)
