import requests

# Constants
URL = "http://10.5.241.37:8767"
HEADERS = {'content-type': 'text/xml'}
SUCCESS_KEYWORD = "Success"
DEVICE_DN = 'DeviceDn'

# Functions
def update_xml_with_new_number(xml_string, device_dn, new_number):
    """Replace occurrences of the device DN with a new number in the given XML string."""
    return xml_string.replace(device_dn, new_number)

def send_soap_request(xml_string):
    """Send a SOAP request to the URL with the provided XML string."""
    response = requests.post(URL, data=xml_string, headers=HEADERS)
    return response

def check_response_success(response):
    """Check if the response contains a success message."""
    if SUCCESS_KEYWORD not in response.text:
        print("Configuration failure!")
        quit()

# Example XML strings
create_subscriber_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <soapenv:Header>
        <ns1:hiqHEADER soapenv:actor="http://schemas.xmlsoap.org/soap/actor/next" soapenv:mustUnderstand="0" xmlns:ns1="urn:siemens-hiq8000">
            <InterfaceWSDL>V10.00.10.01</InterfaceWSDL>
            <OperatorId>uCtxId:1897</OperatorId>
            <ClientId>10.14.255.100</ClientId>
        </ns1:hiqHEADER>
    </soapenv:Header>
    <soapenv:Body>
        <CreateSubscriber xmlns="urn:siemens-hiq8000">
            <ServiceId xmlns="">DeviceDn</ServiceId>
            <OperatorId xmlns="">OSVAssistant@system</OperatorId>
            <CreateSubRequest xmlns="">
                <AccountMgtInfo>
                    <AccountId></AccountId>
                    <BillingId></BillingId>
                    <RetailerId></RetailerId>
                    <RateArea></RateArea>
                    <ExternalDNFlag>true</ExternalDNFlag>
                    <CallingLoc></CallingLoc>
                    <NumberPlanName>PNP_IPSL</NumberPlanName>
                    <DistinctiveRinging>false</DistinctiveRinging>
                </AccountMgtInfo>
                <SubscriberBGInfo>
                    <BGName>BG_IPSL</BGName>
                    <BGLineName>+DeviceDn</BGLineName>
                    <BGAttendantNumber>false</BGAttendantNumber>
                    <Extension>0001</Extension>
                    <BGDeptName></BGDeptName>
                    <BGEmergencyDeptName></BGEmergencyDeptName>
                    <AlphanumericSIPUri></AlphanumericSIPUri>
                </SubscriberBGInfo>
                <AccountUserInfo>
                    <DisplayName>+DeviceDn</DisplayName>
                    <TimeZone></TimeZone>
                    <Pin></Pin>
                    <Pin2></Pin2>
                    <Pin3></Pin3>
                    <Pin4></Pin4>
                    <Pin5></Pin5>
                    <PublicPin></PublicPin>
                    <BusinessAuthCode></BusinessAuthCode>
                    <PrivateAuthCode></PrivateAuthCode>
                </AccountUserInfo>
                <Status>
                    <SubscriberStatus>Active</SubscriberStatus>
                </Status>
                <ConnectionInfo>
                    <IPPhone>
                        <Name>DeviceDn</Name>
                        <RegType>Dynamic</RegType>
                        <Register>false</Register>
                        <SIPSecurity>
                            <Scheme>no-security</Scheme>
                            <SrtpSupport>SrtpAutomatic</SrtpSupport>
                            <SdesSrtpSupport>SrtpAutomatic</SdesSrtpSupport>
                        </SIPSecurity>
                        <IPConnectionType>TCP</IPConnectionType>
                        <Attributes>
                            <AcceptBillingNumber>false</AcceptBillingNumber>
                            <Reserved1>false</Reserved1>
                            <Reserved2>false</Reserved2>
                            <Reserved3>false</Reserved3>
                            <TrustedSub>false</TrustedSub>
                            <MediaReDirectionAllowed>false</MediaReDirectionAllowed>
                            <AoRPerContact>false</AoRPerContact>
                            <OverrideIRMCodecRestrictions>false</OverrideIRMCodecRestrictions>
                            <TransferHandoff>false</TransferHandoff>
                            <SendInsecureRefferedByHeader>false</SendInsecureRefferedByHeader>
                            <VideoCallAllowed>true</VideoCallAllowed>
                            <SendPubNrInFQNInFromHeader>false</SendPubNrInFQNInFromHeader>
                            <SendInternationalNumberInGNF>false</SendInternationalNumberInGNF>
                            <DoNotPublishRegistrationToE911DM>false</DoNotPublishRegistrationToE911DM>
                            <DisableLongCallAudit>false</DisableLongCallAudit>
                            <RegistViaCentralSBC>false</RegistViaCentralSBC>
                            <DoNotSendAlphanumericSIPURI>false</DoNotSendAlphanumericSIPURI>
                            <SendAlphanumericSIPURIWhenAvailable>false</SendAlphanumericSIPURIWhenAvailable>
                            <Reserved5>false</Reserved5>
                            <Reserved6>false</Reserved6>
                            <AllowSubProvidedCallingID>false</AllowSubProvidedCallingID>
                            <Reserved7>false</Reserved7>
                            <DoNotAllowURNsForNG911>false</DoNotAllowURNsForNG911>
                            <DisableSRTP>false</DisableSRTP>
                            <Reserved8>false</Reserved8>
                            <Reserved10>false</Reserved10>
                            <Reserved11>false</Reserved11>
                            <DoNotAllowNG911Headers>false</DoNotAllowNG911Headers>
                            <ACDCallDistributionDevice>false</ACDCallDistributionDevice>
                            <SipRecordAllCalls>false</SipRecordAllCalls>
                            <DoNotAllowGeolocationHeaders>false</DoNotAllowGeolocationHeaders>
                            <HideIsFocus>false</HideIsFocus>
                            <SimultaneousCallsNotAllowedFromMultipleContacts>false</SimultaneousCallsNotAllowedFromMultipleContacts>
                        </Attributes>
                        <AssociatedSipEndpointName></AssociatedSipEndpointName>
                        <VIPType>VIPNo</VIPType>
                        <AnatSupport>AnatAuto</AnatSupport>
                        <OutgoingCallSupervisionTimer>0</OutgoingCallSupervisionTimer>
                        <ICESupport>ICEAutomatic</ICESupport>
                        <AEISupport>AEIAuto</AEISupport>
                        <SipUAForkingSupport>SipUAForkingAuto</SipUAForkingSupport>
                        <SrtpMode>SrtpModeAuto</SrtpMode>
                    </IPPhone>
                </ConnectionInfo>
                <InterExchange/>
                <KeysetInfo>
                    <KeysetUse>KeysetNone</KeysetUse>
                    <KeysetPrivacy>false</KeysetPrivacy>
                </KeysetInfo>
                <ListOfFeatures>
                    <CfMCT>
                        <Subscribed>SwitchWide</Subscribed>
                    </CfMCT>
                </ListOfFeatures>
            </CreateSubRequest>
        </CreateSubscriber>
    </soapenv:Body>
</soapenv:Envelope>'''
add_moh_xml_string = '''<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"xmlns:xsd="http://www.w3.org/2001/XMLSchema"xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <soapenv:Header>
        <ns1:hiqHEADER soapenv:actor="http://schemas.xmlsoap.org/soap/actor/next"
            soapenv:mustUnderstand="0" xmlns:ns1="urn:siemens-hiq8000">
            <InterfaceWSDL>V10.00.10.01</InterfaceWSDL>
            <OperatorId>uCtxId:1997</OperatorId>
            <ClientId>10.14.255.100</ClientId>
        </ns1:hiqHEADER>
    </soapenv:Header>
    <soapenv:Body>
        <UpdateSubscriberFeatures2 xmlns="urn:siemens-hiq8000">
            <UpdateSubscriberFeaturesRequest xmlns="">
                <ServiceId>DeviceDn</ServiceId>
                <OperatorId>OSVAssistant@system</OperatorId>
                <ListOfFeatures>
                    <CfMOH>
                        <Subscribed>AddReplace</Subscribed>
                        <Enabled>true</Enabled>
                    </CfMOH>
                </ListOfFeatures>
            </UpdateSubscriberFeaturesRequest>
        </UpdateSubscriberFeatures2>
    </soapenv:Body>
</soapenv:Envelope>'''

# Main program
def main():
    new_number = '6867110001'

    # Update and send the Create Subscriber SOAP request
    updated_create_subscriber_xml = update_xml_with_new_number(create_subscriber_xml, DEVICE_DN, new_number)
    create_subscriber_response = send_soap_request(updated_create_subscriber_xml)
    check_response_success(create_subscriber_response)

    # Update and send the Add Music on Hold SOAP request
    updated_add_moh_xml = update_xml_with_new_number(add_moh_xml_string, DEVICE_DN, new_number)
    add_moh_response = send_soap_request(updated_add_moh_xml)
    check_response_success(add_moh_response)

if __name__ == "__main__":
    main()