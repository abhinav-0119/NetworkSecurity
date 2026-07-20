import os
import sys

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import pandas as pd

class CustomData:
    def __init__(self,having_IP_Address,URL_Length,Shortining_Service,having_At_Symbol,
  double_slash_redirecting,Prefix_Suffix,having_Sub_Domain,SSLfinal_State,Domain_registeration_length,
  Favicon,port,HTTPS_token,Request_URL,URL_of_Anchor,Links_in_tags,SFH,Submitting_to_email,
  Abnormal_URL,Redirect,on_mouseover,RightClick,popUpWidnow,Iframe,age_of_domain,
  DNSRecord,web_traffic,Page_Rank,Google_Index,Links_pointing_to_page,Statistical_report):
        try:
            self.having_IP_Address=having_IP_Address
            self.URL_Length=URL_Length
            self.Shortining_Service=Shortining_Service
            self.having_At_Symbol=having_At_Symbol
            self.double_slash_redirecting=double_slash_redirecting
            self.Prefix_Suffix=Prefix_Suffix
            self.having_Sub_Domain=having_Sub_Domain
            self.SSLfinal_State=SSLfinal_State
            self.Domain_registeration_length=Domain_registeration_length
            self.Favicon=Favicon
            self.port=port
            self.HTTPS_token=HTTPS_token
            self.Request_URL=Request_URL
            self.URL_of_Anchor=URL_of_Anchor
            self.Links_in_tags=Links_in_tags
            self.SFH=SFH
            self.Submitting_to_email=Submitting_to_email
            self.Abnormal_URL=Abnormal_URL
            self.Redirect=Redirect
            self.on_mouseover=on_mouseover
            self.RightClick=RightClick
            self.popUpWidnow=popUpWidnow
            self.Iframe=Iframe
            self.age_of_domain=age_of_domain
            self.DNSRecord=DNSRecord
            self.web_traffic=web_traffic
            self.Page_Rank=Page_Rank
            self.Google_Index=Google_Index
            self.Links_pointing_to_page=Links_pointing_to_page
            self.Statistical_report=Statistical_report
        except Exception as e:
            raise CustomException(e,sys)
    def data_asdf(self):
        try:
            data = {
    "having_IP_Address": [self.having_IP_Address],
    "URL_Length": [self.URL_Length],
    "Shortining_Service": [self.Shortining_Service],
    "having_At_Symbol": [self.having_At_Symbol],
    "double_slash_redirecting": [self.double_slash_redirecting],
    "Prefix_Suffix": [self.Prefix_Suffix],
    "having_Sub_Domain": [self.having_Sub_Domain],
    "SSLfinal_State": [self.SSLfinal_State],
    "Domain_registeration_length": [self.Domain_registeration_length],
    "Favicon": [self.Favicon],
    "port": [self.port],
    "HTTPS_token": [self.HTTPS_token],
    "Request_URL": [self.Request_URL],
    "URL_of_Anchor": [self.URL_of_Anchor],
    "Links_in_tags": [self.Links_in_tags],
    "SFH": [self.SFH],
    "Submitting_to_email": [self.Submitting_to_email],
    "Abnormal_URL": [self.Abnormal_URL],
    "Redirect": [self.Redirect],
    "on_mouseover": [self.on_mouseover],
    "RightClick": [self.RightClick],
    "popUpWidnow": [self.popUpWidnow],
    "Iframe": [self.Iframe],
    "age_of_domain": [self.age_of_domain],
    "DNSRecord": [self.DNSRecord],
    "web_traffic": [self.web_traffic],
    "Page_Rank": [self.Page_Rank],
    "Google_Index": [self.Google_Index],
    "Links_pointing_to_page": [self.Links_pointing_to_page],
    "Statistical_report": [self.Statistical_report]
}
            df=pd.DataFrame(data)
            return df
        except Exception as e:
            raise CustomException(e,sys)
    
        
                
                