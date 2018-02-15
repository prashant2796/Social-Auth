from urllib.request import urlopen
from urllib.parse import urlencode,parse_qsl,urlparse
import webbrowser
import requests

import requests.auth

# https://www.googleapis.com/auth/userinfo.email

CLIENT_ID='544125358258-jsnghl0v7lljccjpce93hpaj8hiuc5p6.apps.googleusercontent.com'

CLIENT_SECRET='gmNJI8gsjpY_AdbfEkwxajRd'

AUTHORIZE_URL='https://accounts.google.com/o/oauth2/auth'

CALLBACK_URL='http://127.0.0.1:8000/admin/oauth2callback'

ACCESS_TOKEN_URL='https://www.googleapis.com/oauth2/v3/token'

API_RESOURCE_URL='https://www.googleapis.com/oauth2/v1/userinfo'

def get_authorization_url():

	auth_parameters= {"client_id":CLIENT_ID,
					  "response_type":"code",
					  "redirect_uri":CALLBACK_URL,
					  "scope":"email"
					 }

	auth_url="?".join([AUTHORIZE_URL,urlencode(auth_parameters)])
	webbrowser.open_new_tab(auth_url)

get_authorization_url()


redirect_url = input("Paste here url you were redirected:\n")


def get_authorization_code():

	redirect_parameters=dict(parse_qsl(urlparse(redirect_url).query))
	auth_code=redirect_parameters['code']
	return auth_code

get_authorization_code()

def get_access_token():
	access_token_parameters={
								"client_id":CLIENT_ID,
								"CLIENT_SECRET":CLIENT_SECRET,
								"redirect_uri":CALLBACK_URL,
								"code":get_authorization_code(),
								"grant_type":'authorization_code'
							}
	result=urlopen(ACCESS_TOKEN_URL,data=urlencode(access_token_parameters).encode("utf-8"))
	result_content=json.loads(result.read())
	print(result_content)
	# access_token=result_content['access_token']
	# print(access_token)

	# client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	# post_data = {"grant_type": "authorization_code",
	#              "code": get_authorization_code(),
	#              "redirect_uri": CALLBACK_URL}
	# response = requests.post(AUTHORIZE_URL,
	#                          auth=client_auth,
	#                          data=post_data)
	# token_json = response.json()
	# my_access_token=token_json["access_token"]
	# print(my_access_token)

	

get_access_token()



