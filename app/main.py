import sys
import json
import logging
import base64
import unicodedata
import traceback
import pandas as pd

from google.cloud import pubsub_v1

from models.google_ad_model import *
from models.google_analytics_model import *
from models.facebook_model import *
from models.bigquery_model import *
from models.yahoo_model import *
from models.datastore_model import *
from consts.common_consts import *

def google_ad( event, context ):

    # Get accounts
    accounts = DataStoreClient(get_datastore_info()).get_accounts(TypeConsts.TYPE_GOOGLE_AD)
    for account in accounts:

        try:
            # Get performance report
            items = GoogleAdReportClient().get_performance_report(account)
            print(account["name"] + ", " + account["account_id"] + " has %s campaigns." % ( str(len(items))) )
            if len(items) == 0:
                continue

            # Create Insert Data
            obj = {}
            for key in GOOGLEAD_ENTITY_KEYS:
                obj[key] = [d[key] for d in items]

            # Excec Create Data
            df = pandas.DataFrame(obj)
            BigQueryClient(get_googlead_bigquery_info()).write(df)

        except Exception as ex:
            print_error( account )

    # Result OK
    return "OK"
    
    
def facebook_ad( event, context ):
    
    # Get accounts
    datastore_client = DataStoreClient(get_datastore_info())
    accounts = datastore_client.get_accounts(TypeConsts.TYPE_FACEBOOK)
    access_info = datastore_client.get_access_info(TypeConsts.TYPE_FACEBOOK)
    for account in accounts:

        try:
            # Get performance report
            items = FaceBookReportClient(access_info).get_performance_report(account)
            print(account["name"] + ", " + account["account_id"] + " has %s campaigns." % ( str(len(items))) )
            if len(items) == 0:
                continue

            # Create Insert Data
            obj = {}
            for key in FACEBOOK_ENTITY_KEYS:
                obj[key] = [d[key] for d in items]

            # Excec Create Data
            df = pandas.DataFrame(obj)
            BigQueryClient(get_facebook_bigquery_info()).write(df)

        except Exception as ex:
            print_error( account )

    # Result OK
    return "OK"
    

def google_analytics( event, context ):
    
    # Get accounts
    datastore_client = DataStoreClient(get_datastore_info())
    accounts = datastore_client.get_accounts(TypeConsts.TYPE_GOOGLE_ANALYTICS)
    for account in accounts:

        try:
            # Get performance report
            items = GoogleAnalyticsReportClient().get_performance_report(account)
            print(account["name"] + ", " + account["account_id"] + " has %s campaigns." % ( str(len(items))) )
            if len(items) == 0:
                continue

            # Create Insert Data
            obj = {}
            for key in GOOGLE_ANALYTICS_ENTITY_KEYS:
                obj[key] = [d[key] for d in items]

            # Excec Create Data
            df = pandas.DataFrame(obj)
            BigQueryClient(get_googleanalytics_bigquery_info()).write(df)

        except Exception as ex:
            print_error( account )

    # Result OK
    return "OK"


def yahoo_ad( event, context ):
    '''
    https://github.com/yahoojp-marketing/ads-search-api-java-samples
    '''
    publisher = pubsub_v1.PublisherClient()
    datastore_client = DataStoreClient(get_datastore_info())

    # Launch Display Report
    accounts = datastore_client.get_accounts(TypeConsts.TYPE_YAHOO_DISPLAY)
    for account in accounts:

        body = dict_to_json({
            "account": account
        })

        __publish_pubsub( 
            publisher,
            PubSub.YAHOO_WORKER,
            body.encode("utf-8")
        )

    # Launch Search Report
    accounts = datastore_client.get_accounts(TypeConsts.TYPE_YAHOO_SEARCH)
    for account in accounts:

        body = dict_to_json({
            "account": account
        })

        __publish_pubsub( 
            publisher,
            PubSub.YAHOO_WORKER,
            body.encode("utf-8")
        )

def yahoo_ad_worker( event, context ):

    if is_dev():
        account = {
            "account_id": "*****",
            "name": "Sample Search",
            "type": TypeConsts.TYPE_YAHOO_SEARCH
        }        

        account = {
            "account_id": "*****",
            "name": "Sample Name",
            "type": TypeConsts.TYPE_YAHOO_DISPLAY
        }

    else:
        body = base64.b64decode(event['data']).decode('utf-8')
        body = json_to_dict( body )
        account = body.get("account")
    
    __internal_yahoo_ad_worker( account )


def __internal_yahoo_ad_worker( account ):
    '''
    '''
    ad_type = account["type"]
    account_id = int(account["account_id"])

    # Create client.
    client = YahooAdReportClient()

    # Get access token.
    token = client.get_refresh_token()
    access_token = token.get("access_token")
    job_id = client.add_performance_report( ad_type, account_id, access_token )
    if job_id is None:
        print( "YahooAd Failed: Failed in getting jobID" )
        return

    # Get performance report.
    try:

        # Wait until report is completed.
        is_ok_wait = client.wait_performance_report( ad_type, account_id, access_token, job_id )

        # Get report 
        if not is_ok_wait:
            raise Exception("Wait Timeout.")
        
        items = client.get_performance_report( ad_type, account_id, access_token, job_id )
        if 0 == len(items):
            print( "Report is not found." )
            return "OK"

        # Create Insert Data
        obj = {}
        index = 0
        for key in client.get_keys( ad_type ):
            #obj[key] = [ report[index] ]
            obj[key] = [d[index] for d in items]
            index += 1

        # Excec Create Data
        df = pandas.DataFrame(obj)
        BigQueryClient( get_yahoo_bigquery_info(ad_type) ).write(df)

    except Exception as ex:
        import traceback
        print(traceback.format_exc())
        print( "YahooAd Failed: %s" % (ex) )
        print_error( account )

    # Remove JobId
    is_ok_remove = client.delete_performance_report( ad_type, account_id, access_token, job_id )
    if not is_ok_remove:
        print( "YahooAd Failed: Remove JobId" )
        return "NG"

    return "OK"

def __publish_pubsub( publisher, topic_name, data ):
    '''
    【処理概要】
    メッセージ発行用のサブモジュール
    '''
    topic_path = publisher.topic_path(
        os.getenv('GCP_PROJECT'),
        topic_name
    )

    future = publisher.publish( topic_path, data )

    return future

def print_error( account ):
    print("-- Error Info Start -------------------------------")
    print(account["name"] + ", " + account["account_id"])
    print(sys.exc_info())
    print("-- Error Info End -------------------------------")

def __test_yahoo():

    #account = {
    #    "type": TypeConsts.TYPE_YAHOO_SEARCH,
    #    "account_id": "*****",
    #}
    #__internal_yahoo_ad_worker( account )

    # Yahoo
    datastore_client = DataStoreClient(get_datastore_info())
    accounts = datastore_client.get_accounts(TypeConsts.TYPE_YAHOO_DISPLAY)
    for account in accounts:
        __internal_yahoo_ad_worker( account )
    #accounts = datastore_client.get_accounts(TypeConsts.TYPE_YAHOO_SEARCH)
    #for account in accounts:
    #    __internal_yahoo_ad_worker( account )

if __name__ == '__main__':

    set_develop_flag()

    # For Debug
    __test_yahoo()
    # google_ad(None, None)
    # facebook_ad(None, None)
    # google_analytics(None, None)
    pass