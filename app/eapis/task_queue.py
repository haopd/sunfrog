# -*- coding: utf-8 -*-
import logging
from protorpc import messages, message_types, remote
from bs4 import BeautifulSoup
import app
from app.eapis.sunApi import DataSheets

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class UploadDataToSheet(app.BaseRequestHandler):
    def post(self):
        data = self.request.POST
        obj = DataSheets.get_by_id(int(data.get('id')))
        if obj:
            soup = BeautifulSoup(obj.data, 'html.parser')
            trs = soup.find_all("tr")
            for i in range(2, len(trs) - 1):
                tr = BeautifulSoup(str(trs[i]), 'html.parser')
                tds = tr.find_all("td")
                campaign_title = tds[2].find_all("a")[0].text
                campaign_href = tds[2].find_all("a")[0].get('href')
                campaign_sold = int(tds[4].text)
                try:
                    if '$' not in (tds[7].text):
                        campaign_affiliate = 0
                    else:
                        campaign_affiliate = float((tds[7].text).replace("$", ""))
                except:
                    campaign_affiliate = 0
                try:
                    campaign_artist = float((tds[8].text).replace("$", ""))
                except:
                    campaign_artist = 0
                campaign_totals = campaign_affiliate + campaign_artist
                campaign_datas = [campaign_sold, campaign_affiliate,
                                  campaign_artist,
                                  campaign_totals]

                if campaign_title in data:
                    old_data = data[campaign_title]
                    new_data = [old_data[0] + campaign_sold,
                                old_data[1] + campaign_affiliate,
                                old_data[2] + campaign_artist,
                                old_data[3] + campaign_totals]
                    data[campaign_title] = new_data
                else:
                    data[campaign_title] = campaign_datas
            self.pushDataToGoogleSheet(data)

    def pushDataToGoogleSheet(self, data):
        import gae_sheet
        if data:
            for k, v in data.items():
                gae_sheet.run(k, v)
