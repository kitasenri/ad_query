# Consts
is_develop = False

CREATE_USER = "CloudFunction"

PROJECT_ID = "*****"
PROJECT_ID_DEV = "*****"
DATASET_NAME = "ad_query"
DATASET_NAME_DEV = "ad_query_dev"
IF_EXISTS = "append"

class YAHOO_API:
    STATUS_OK = 200
    TOKEN = "https://biz-oauth.yahoo.co.jp/oauth/v1/token?grant_type=refresh_token&client_id=%s&client_secret=%s&refresh_token=%s"
    SEARCH = "https://ads-search.yahooapis.jp/api/v1/ReportDefinitionService/"
    DISPLAY = "https://ads-display.yahooapis.jp/api/v1/ReportDefinitionService/"

class TypeConsts:
    TYPE_GOOGLE_AD = "GoogleAd"
    TYPE_FACEBOOK = "Facebook"
    TYPE_YAHOO_DISPLAY = "YahooDisplay"
    TYPE_YAHOO_SEARCH = "YahooSearch"
    TYPE_GOOGLE_ANALYTICS = "GoogleAnalytics"
    TYPE_FILEMAKER = "FileMaker"

class PubSub:
    YAHOO_WORKER = "topic_yahoo_ad_worker"

def set_develop_flag():
    global is_develop
    is_develop = True

def is_dev():
    global is_develop
    return is_develop

def get_datastore_info():
    info = {
        "project": PROJECT_ID
    }
    if is_develop:
        info["project"] = PROJECT_ID_DEV

    return info

def get_googlead_bigquery_info():

    info = {
        "project": PROJECT_ID,
        "dataset": DATASET_NAME,
        "table": "google_ad_performance_report",
        "if_exists": IF_EXISTS
    }

    if is_develop:
        info["project"] = PROJECT_ID_DEV
        info["dataset"] = DATASET_NAME_DEV

    return info

def get_googleanalytics_bigquery_info():

    info = {
        "project": PROJECT_ID,
        "dataset": DATASET_NAME,
        "table": "google_analytics_performance_report",
        "if_exists": IF_EXISTS
    }

    if is_develop:
        info["project"] = PROJECT_ID_DEV
        info["dataset"] = DATASET_NAME_DEV

    return info

def get_facebook_bigquery_info():

    info = {
        "project": PROJECT_ID,
        "dataset": DATASET_NAME,
        "table": "facebook_performance_report",
        "if_exists": IF_EXISTS
    }

    if is_develop:
        info["project"] = PROJECT_ID_DEV
        info["dataset"] = DATASET_NAME_DEV

    return info

def get_yahoo_bigquery_info(ad_type):

    info = {
        "project": PROJECT_ID,
        "dataset": DATASET_NAME,
        "if_exists": IF_EXISTS
    }

    if ad_type == TypeConsts.TYPE_YAHOO_DISPLAY:
        info["table"] = "yahoo_performance_report_display"
    elif ad_type == TypeConsts.TYPE_YAHOO_SEARCH:
        info["table"] = "yahoo_performance_report_search"

    if is_develop:
        info["project"] = PROJECT_ID_DEV
        info["dataset"] = DATASET_NAME_DEV

    return info