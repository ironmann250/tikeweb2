import requests
try:
    from xml.etree import cElementTree as ET
except ImportError as e:
    from xml.etree import ET
from string import Template

#error raising and such...
class RequestError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

req_url='https://secure.3gdirectpay.com/API/v6/'
red_url='https://secure.3gdirectpay.com/pay.asp?ID='
dt={'company_token': '224F472D-2E3A-4355-9D99-48A0533D9E72',
    'price': '0', 'details': 'test product',
    'redirect_url': 'www.bing.com',
    'date': '2018/06/14 16:30', 'type': '20173',
    'email':'test@t.com','fname':'test','lname':'johnny',
    'address':'kigali rwanda kk45','city':'kigali',
    'country':'rw','phone':'78016203','zip':'56001'} #test data for create token

ddt={'company_token':'224F472D-2E3A-4355-9D99-48A0533D9E72',
     'transaction_token':'910285C5-15ED-4755-875E-59B820AC0454'} #test dataa for cancel token and verify token
#company token: 9F416C11-127B-4DE2-AC7F-D5710E4C5E0A
#3854,5525
def create_token(mapping=dt,headers = {'Content-Type': 'application/xml'}):
	data=Template('''<?xml version="1.0" encoding="utf-8"?>
	<API3G>
	<CompanyToken>$company_token</CompanyToken>
	<Request>createToken</Request>
	<Transaction>
	<customerEmail>$email</customerEmail>
	<customerFirstName>$fname</customerFirstName>
	<customerLastName>$lname</customerLastName>
	<customerAddress>$address</customerAddress>
	<customerCity>$city</customerCity>
	<customerCountry>$country</customerCountry>
	<customerDialCode>RW</customerDialCode>
	<customerPhone>$phone</customerPhone>
	<customerZip>$zip</customerZip>
	<PaymentAmount>$price</PaymentAmount>
	<PaymentCurrency>RWF</PaymentCurrency>
	<RedirectURL>$redirect_url</RedirectURL>
	<DefaultPayment>MO</DefaultPayment>
	<DefaultPaymentCountry>rwanda</DefaultPaymentCountry>
	</Transaction>
	<Services>
	  <Service>
	    <ServiceType>$type</ServiceType>
	    <ServiceDescription>$details</ServiceDescription>
	    <ServiceDate>$date</ServiceDate>
	  </Service>
	</Services>
	</API3G>''').substitute(mapping)
	response=requests.post(req_url, data=data, headers=headers)
	xml_rec=ET.fromstring(response.text)
	if xml_rec.find('Result').text != '000':
	    raise RequestError(xml_rec.find('ResultExplanation').text+' [error code: '+xml_rec.find('Result').text+' ]')
	else:
	    return {'code':xml_rec.find('Result').text,'token':xml_rec.find('TransToken').text,
					'ref':xml_rec.find('TransRef').text,
					'url':red_url+xml_rec.find('TransToken').text}
			
def verify_token(mapping=ddt,headers = {'Content-Type': 'application/xml'}):
    data=Template('''<?xml version="1.0" encoding="utf-8"?>
    <API3G>
        <CompanyToken>$company_token</CompanyToken>
        <Request>verifyToken</Request>
      <TransactionToken>$transaction_token</TransactionToken>
    </API3G>''').substitute(mapping)
    response=requests.post(req_url, data=data, headers=headers)
    xml_rec=ET.fromstring(response.text)
    if xml_rec.find('Result').text[0]=='9':
        return {'code':xml_rec.find('Result').text,'paid':False,
                'message':xml_rec.find('ResultExplanation').text}
    elif xml_rec.find('Result').text[0]=='000':
        return {'code':xml_rec.find('Result').text,'paid':True,
                'message':xml_rec.find('ResultExplanation').text}
    else:
        raise RequestError(xml_rec.find('ResultExplanation').text+' [error code: '+xml_rec.find('Result').text+' ]')


def cancel_token(mapping=ddt,headers = {'Content-Type': 'application/xml'}):
    data=Template('''<?xml version="1.0" encoding="utf-8"?>
    <API3G>
        <CompanyToken>$company_token</CompanyToken>
        <Request>cancelToken</Request>
        <TransactionToken>$transaction_token</TransactionToken>v
    </API3G>''').substitute(mapping)
    response=requests.post(req_url, data=data, headers=headers)
    xml_rec=ET.fromstring(response.text)
    if xml_rec.find('Result').text != '000':
        raise RequestError(xml_rec.find('ResultExplanation').text+' [error code: '+xml_rec.find('Result').text+' ]')
    else:
        return {'message':xml_rec.find('ResultExplanation').text}



