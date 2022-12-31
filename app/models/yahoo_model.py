import os
import json
import logging
import requests
import time

from utils.common_utils import *
from consts.common_consts import *

## Display Keys
## https://github.com/yahoojp-marketing/ydn-api-documents/blob/master/docs/en/api_reference/appendix/reports/AD.csv
YAHOO_REPORT_FIELDS_DISPLAY_KEYS = [
    "ACCOUNT_ID",
    "ACCOUNT_NAME",
    "CAMPAIGN_ID",
    "CAMPAIGN_NAME",
    #"ADGROUP_ID",
    #"ADGROUP_NAME",
    #"AD_ID",
    #"AD_NAME",
    #"AD_TYPE",
    "DELIVER",
    "AD_TITLE",
    "DESCRIPTION1",
    "DESCRIPTION2",
    "DISPLAY_URL",
    "AD_LAYOUT",
    #"CONVERSION_NAME",
    "CAMPAIGN_TYPE",
    "APP_ID",
    "APP_NAME",
    "APP_OS",
    "CAMPAIGN_BUYING_TYPE",
    "DESTINATION_URL_CAMPAIGN_BANNER",

    ## Metrics
    "IMPS",
    "CLICK_RATE",
    "COST",
    "CLICK",
    "AVG_CPC",
    "AVG_DELIVER_RANK",
    "TOTAL_VIEWABLE_IMPS",
    "VIEWABLE_IMPS",
    "INVIEW_RATE",
    "INVIEW_CLICK",
    "INVIEW_CLICK_RATE",
    "AVG_CPV",
    "VIDEO_VIEWS_TO_25",
    "VIDEO_VIEWS_TO_50",
    "VIDEO_VIEWS_TO_75",
    "VIDEO_VIEWS_TO_95",
    "VIDEO_VIEWS_TO_100",
    "AVG_PERCENT_VIDEO_VIEWED",
    "AVG_DURATION_VIDEO_VIEWED",
    "VIDEO_VIEWS",
    "PAID_VIDEO_VIEWS",
    "PAID_VIDEO_VIEW_RATE",
    "VIDEO_VIEWS_TO_3_SEC",
    "CONVERSIONS",
    "CONV_RATE",
    "COST_PER_CONV",
    "CONV_VALUE",
    "VALUE_PER_CONV",
    "ALL_CONV",
    "ALL_CONV_RATE",
    "COST_PER_ALL_CONV",
    "ALL_CONV_VALUE",
    "VALUE_PER_ALL_CONV",
    "CONVERSIONS_VIA_AD_CLICK",
    "CONVERSION_RATE_VIA_AD_CLICK",
    "COST_PER_CONV_VIA_AD_CLICK",
    "CONV_VALUE_VIA_AD_CLICK",
    "VALUE_PER_CONV_VIA_AD_CLICK",
    "CROSS_DEVICE_CONVERSIONS",
    "CONV_VALUE_PER_COST",
    "ALL_CONV_VALUE_PER_COST",
    "CONV_VALUE_VIA_AD_CLICK_PER_COST",
    "IMPS_PREV",
    "CLICK_RATE_PREV",
    "AVG_CPM",
    "AVG_VCPM",
    "MEASURED_IMPS",
    "VIEWABLE_CLICK",
    "MEASURED_IMPS_RATE",
    "VIEWABLE_IMPS_RATE",
    "VIEWABLE_CLICK_RATE",
    "VIDEO_VIEWS_TO_10_SEC",

    ## Segument
    #"URL_ID",
    #"URL_NAME",
    #"PREF_ID",
    #"PREF_NAME",
    #"CITY_ID",
    #"CITY_NAME",
    #"WARD_ID",
    #"WARD_NAME",
    #"GENDER",
    #"AGE",
    #"MONTH",
    #"DAY",
    #"HOUR",
    #"DEVICE",
    #"AD_STYLE",
    #"MEDIA_ID",
    #"MEDIA_NAME",
    #"MEDIA_FILE_NAME",
    #"MEDIA_AD_FORMAT",
    #"SEARCHKEYWORD_ID",
    #"SEARCHKEYWORD",
    #"CONVERSION_CATEGORY",
    #"CARRIER",
    #"IMAGE_OPTION",
    #"OS",
    #"APPLI",
    #"CAMPAIGN_GOALS",
]

YAHOO_REPORT_DISPLAY_KEYS = YAHOO_REPORT_FIELDS_DISPLAY_KEYS[:]
YAHOO_REPORT_DISPLAY_KEYS.append("ad_type")
YAHOO_REPORT_DISPLAY_KEYS.append("report_date")
YAHOO_REPORT_DISPLAY_KEYS.append("create_on")
YAHOO_REPORT_DISPLAY_KEYS.append("create_user")

## Search Keys
## https://trocco.zendesk.com/hc/ja/articles/360037171834-%E8%BB%A2%E9%80%81%E5%85%83-Yahoo-%E6%A4%9C%E7%B4%A2%E5%BA%83%E5%91%8A-YSS-
YAHOO_REPORT_FIELDS_SEARCH_KEYS = [
    "ACCOUNT_ID", 
    "ACCOUNT_NAME",
    "CAMPAIGN_ID",
    "CAMPAIGN_NAME",
    "CAMPAIGN_DISTRIBUTION_SETTINGS",
    "CAMPAIGN_DISTRIBUTION_STATUS",
    "DAILY_SPENDING_LIMIT",
    "CAMPAIGN_START_DATE",
    "CAMPAIGN_END_DATE",
    "TRACKING_URL",
    "CUSTOM_PARAMETERS",
    "CAMPAIGN_TRACKING_ID",
    "CAMPAIGN_MOBILE_BID_MODIFIER",
    "CAMPAIGN_DESKTOP_BID_MODIFIER",
    "CAMPAIGN_TABLET_BID_MODIFIER",
    "CAMPAIGN_TYPE",
    "LABELS",
    "LABELS_JSON",
    "BID_STRATEGY_ID",
    "BID_STRATEGY_NAME",
    "BID_STRATEGY_TYPE",
    "ENHANCED_CPC_ENABLED",

    ### Metrix
    "COST",
    "IMPS",
    "CLICKS",
    "CLICK_RATE",
    "AVG_CPC",
    "INVALID_CLICKS",
    "INVALID_CLICK_RATE",
    "IMPRESSION_SHARE",
    "EXACT_MATCH_IMPRESSION_SHARE",
    "BUDGET_LOST_IMPRESSION_SHARE",
    "QUALITY_LOST_IMPRESSION_SHARE",
    "CONVERSIONS",
    "CONV_RATE",
    "CONV_VALUE",
    "COST_PER_CONV",
    "VALUE_PER_CONV",
    "ALL_CONV",
    "ALL_CONV_RATE",
    "ALL_CONV_VALUE",
    "COST_PER_ALL_CONV",
    "VALUE_PER_ALL_CONV",
    "CROSS_DEVICE_CONVERSIONS",
    "ABSOLUTE_TOP_IMPRESSION_PERCENTAGE",
    "TOP_IMPRESSION_PERCENTAGE",
    "SEARCH_ABSOLUTE_TOP_IMPRESSION_SHARE",
    "SEARCH_TOP_IMPRESSION_SHARE",
    "SEARCH_BUDGET_LOST_ABSOLUTE_TOP_IMPRESSION_SHARE",
    "SEARCH_RANK_LOST_ABSOLUTE_TOP_IMPRESSION_SHARE",
    "SEARCH_BUDGET_LOST_TOP_IMPRESSION_SHARE",
    "SEARCH_RANK_LOST_TOP_IMPRESSION_SHARE",
    "CONV_VALUE_PER_COST",
    "ALL_CONV_VALUE_PER_COST",

    ### Seguments
    #"NETWORK",
    #"CLICK_TYPE",
    #"DEVICE",
    #"DAY",
    #"DAY_OF_WEEK",
    #"QUARTER",
    #"YEAR",
    #"MONTH",
    #"MONTH_OF_YEAR",
    #"WEEK",
    #"HOUR_OF_DAY",
    #"OBJECT_OF_CONVERSION_TRACKING",
    #"CONVERSION_NAME",
]

YAHOO_REPORT_SEARCH_KEYS = YAHOO_REPORT_FIELDS_SEARCH_KEYS[:]
YAHOO_REPORT_SEARCH_KEYS.append("ad_type")
YAHOO_REPORT_SEARCH_KEYS.append("report_date")
YAHOO_REPORT_SEARCH_KEYS.append("create_on")
YAHOO_REPORT_SEARCH_KEYS.append("create_user")


class YahooAdReportClient():

    def __init__(self):
        pass

    def create_header(self, access_token):
        headers = {
            "Accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Bearer %s" % (access_token)
        }
        return headers

    def get_endpoint(self, ad_type):
        if ad_type == TypeConsts.TYPE_YAHOO_DISPLAY:
            return YAHOO_API.DISPLAY
        elif ad_type == TypeConsts.TYPE_YAHOO_SEARCH:
            return YAHOO_API.SEARCH
        else:
            return None

    def get_keys(self, ad_type):
        if ad_type == TypeConsts.TYPE_YAHOO_DISPLAY:
            return YAHOO_REPORT_DISPLAY_KEYS
        elif ad_type == TypeConsts.TYPE_YAHOO_SEARCH:
            return YAHOO_REPORT_SEARCH_KEYS
        else:
            return None


    #----------------------------------------------------------------
    # Refresh Token
    #----------------------------------------------------------------
    def get_refresh_token(self):
        '''
        Get Refresh Token
        '''
        auth_url = YAHOO_API.TOKEN % (
            os.environ.get('YAHOO_CLIEND_ID'),
            os.environ.get('YAHOO_CLIENT_SECRET'),
            os.environ.get('YAHOO_REFRESH_TOKEN')
        )

        response = requests.post( auth_url )
        if response.status_code == YAHOO_API.STATUS_OK:
            return json.loads( response.text )
        else:
            print( response.text )
            return None

    #----------------------------------------------------------------
    # Add Param
    #----------------------------------------------------------------
    def get_add_param(self, ad_type, account_id):

        if ad_type == TypeConsts.TYPE_YAHOO_DISPLAY:
            # ReportDefinitionService
            # https://yahoojp-marketing.github.io/ads-display-api-documents/
            return [{
                "accountId": account_id,
                "fields": YAHOO_REPORT_FIELDS_DISPLAY_KEYS,
                "reportName": "CampaignReport",
                "dateRangeType": "YESTERDAY",
                "downloadEncode": "UTF-8",
                "downloadFormat": "CSV",
#                "frequencyRange": "DAILY",
                "lang": "JA",
            }]
        elif ad_type == TypeConsts.TYPE_YAHOO_SEARCH:
            # ReportDefinitionService
            # https://yahoojp-marketing.github.io/ads-search-api-documents/?lang=ja&v=1
            return [{
                "accountId": account_id,
                "fields": YAHOO_REPORT_FIELDS_SEARCH_KEYS,
                "reportName": "CampaignReport",
                "reportType": "CAMPAIGN",
                "reportCompressType": "NONE",
                "reportDateRangeType": "YESTERDAY",
                "reportDownloadEncode": "UTF-8",
                "reportDownloadFormat": "CSV",
                "reportIncludeDeleted": "FALSE",
                "reportIncludeZeroImpressions": "FALSE",
                "reportLanguage": "JA",
            }]
        else:
            return None


    def add_performance_report(self, ad_type, account_id, access_token) -> str:
        '''
        '''
        headers = self.create_header(access_token)
        payload = {
            "accountId": account_id,
            "operand": self.get_add_param( ad_type, account_id )
        }

        response = requests.post(
            self.get_endpoint(ad_type) + "add", 
            data = json.dumps(payload), 
            headers = headers
        )

        if response.status_code == YAHOO_API.STATUS_OK:
            json_obj = json.loads( response.text )
            values = json_obj.get("rval", {}).get("values", [])[0]
            if values.get("errors") is not None:
                print( values.get("errors") )
                return None

            return values.get("reportDefinition", {}).get("reportJobId")
        else:
            print( response.text )
            return None

    #----------------------------------------------------------------
    # Wait Process
    #----------------------------------------------------------------
    def get_processing_status(self, ad_type):
        if ad_type == TypeConsts.TYPE_YAHOO_DISPLAY:
            return ["IN_PROGRESS", "ACCEPTED"]
        elif ad_type == TypeConsts.TYPE_YAHOO_SEARCH:
            return ["IN_PROGRESS", "WAIT"]
        else:
            return None

    def get_response_status(self, ad_type, json_obj):
        if ad_type == TypeConsts.TYPE_YAHOO_DISPLAY:
            return json_obj.get("rval", {}).get("values", [])[0].get("reportDefinition", {}).get("jobStatus")
        elif ad_type == TypeConsts.TYPE_YAHOO_SEARCH:
            return json_obj.get("rval", {}).get("values", [])[0].get("reportDefinition", {}).get("reportJobStatus")
        else:
            return None

    def wait_performance_report(self, ad_type, account_id, access_token, job_id) -> bool:
        '''
        Wait until report is enabled.
        '''
        is_ok = False

        headers = self.create_header(access_token)
        payload = {
            "accountId": account_id,
            "reportJobIds": [
                job_id
            ],
        }

        index = 0
        while True:

            time.sleep(10)

            response = requests.post(
                self.get_endpoint(ad_type) + "get", 
                data = json.dumps(payload), 
                headers = headers
            )

            if response.status_code != YAHOO_API.STATUS_OK:
                print( "Error in wait_performance_report: HTTP Status Error %s" % (response.status_code) )
                break

            json_obj = json.loads( response.text )
            error_no = json_obj.get("errors").get("code") if json_obj.get("errors") else None
            if error_no:
                print( "Error in wait_performance_report: Error No %s" % (error_no) )
                break

            status = self.get_response_status( ad_type, json_obj )
            if status == "COMPLETED":
                is_ok = True
                break
            elif status in self.get_processing_status(ad_type):
                continue
            else:
                print( "Error in wait_performance_report: Status Not Found %s" % (status) )
                break

            index += 1
            if 30 <= index:
                print( "Error in wait_performance_report: Timeout" )
                break

        return is_ok

    #----------------------------------------------------------------
    # Get report.
    #----------------------------------------------------------------
    def append_option_param( self, ad_type, report ):
        '''
        '''

        report.append( ad_type )
        report.append( create_yesterday_date() )
        report.append( create_today() )
        report.append( CREATE_USER )

        return report

    def get_report_from_csv(self, ad_type, csv):

        items = []
        length = len( csv )
        if ad_type == TypeConsts.TYPE_YAHOO_DISPLAY:

            for ii, report in enumerate( csv ):
                if ii != 0 and ii != length - 1:
                    self.append_option_param( ad_type, report )
                    items.append( report )

            return items

        elif ad_type == TypeConsts.TYPE_YAHOO_SEARCH:

            for ii, report in enumerate( csv ):
                if ii != 0 and ii != length - 1:
                    self.append_option_param( ad_type, report )
                    items.append( report )

            return items
        else:
            return None

    def get_performance_report(self, ad_type, account_id, access_token, job_id) -> dict:
        '''
        Get performance report
        '''
        headers = self.create_header(access_token)
        payload = {
            "accountId": account_id,
            "reportJobId": job_id
        }

        response = requests.post(
            self.get_endpoint(ad_type) + "download", 
            data = json.dumps(payload), 
            headers = headers
        )

        if response.status_code == YAHOO_API.STATUS_OK:

            print( response.text )
            parsed_csv = parse_csv( response.text )
            report = self.get_report_from_csv( ad_type, parsed_csv )

            return report
        else:
            print( response.text )
            return None

    #----------------------------------------------------------------
    # Delete report
    #----------------------------------------------------------------
    def delete_performance_report(self, ad_type, account_id, access_token, job_id) -> bool:
        '''
        Delete created report.
        '''
        headers = self.create_header(access_token)
        payload = {
            "accountId": account_id,
            "operand": [{
                "reportJobId": job_id
            }]
        }

        response = requests.post(
            self.get_endpoint(ad_type) + "remove", 
            data = json.dumps(payload), 
            headers = headers
        )

        if response.status_code == YAHOO_API.STATUS_OK:

            json_obj = json.loads( response.text )
            error_no = json_obj.get("errors").get("code") if json_obj.get("errors") else None
            if error_no:
                print( "Error in delete_performance_report: Error No  %s" % (error_no) )
                return False

            return True
        else:
            print( response.text )
            return False