from flask import Flask, abort, request
from urllib.request import urlopen
from urllib.parse import urlencode,parse_qsl,urlparse
import webbrowser
import requests

CLIENT_ID='544125358258-jsnghl0v7lljccjpce93hpaj8hiuc5p6.apps.googleusercontent.com'

CLIENT_SECRET='gmNJI8gsjpY_AdbfEkwxajRd'

AUTHORIZE_URL='https://accounts.google.com/o/oauth2/auth?'

CALLBACK_URL='http://127.0.0.1:5000/oauth2callback'

ACCESS_TOKEN_URL='https://www.googleapis.com/oauth2/v3/token'

API_RESOURCE_URL='https://www.googleapis.com/oauth2/v1/userinfo'

SCOPE_URL='https://www.googleapis.com/auth/user.emails.read'


app = Flask(__name__)
@app.route('/')

def homepage():
	"""
	Displays the authorization link to users.

	"""
	text = '<a href="%s">Login with google</a>'
	return text % get_authorization_url()


def get_authorization_url():

	"""
	this function returns the authorization url

	it makes a get request to the authorization 
	url of google and  with the parameters
	that are appended to it.
	"""

	auth_parameters= {"client_id":CLIENT_ID,
					  "redirect_uri":CALLBACK_URL,
					  "scope":SCOPE_URL,	
  					  "response_type":"code",
					  "access_type":'offline',
   					  "include_granted_scopes":'true'				  
					 }
	auth_url=requests.get(AUTHORIZE_URL,params=auth_parameters) 
	#makes a get request to authorization url

	return auth_url.url   #the .url method returns the url with parameters appended to it.

@app.route('/oauth2callback') 
def google_call_back():
	"""
	The control is switched to this function when user is redirected after authorizing the client app.

	It returns the final user data which is defined in scope parameter.

	"""
	error = request.args.get('error', '')     
	if error:
	    return "Error: " + error        #returns the error if there is one.

	auth_code = request.args.get('code')  #it takes in authorization code
	access_token = get_access_token(auth_code) #takes in access token returned my the function
	return "your google info is:%s" % get_user_info(access_token)

def get_access_token(auth_code):
	"""
	this function makes a post request which exchanges authorization code for 
	access token and returns it.

	"""
	access_token_parameters={
								"client_id":CLIENT_ID,
								"client_secret":CLIENT_SECRET,
								"redirect_uri":CALLBACK_URL,
								"code":auth_code,
								"grant_type":"authorization_code"
							}

	
	token_result=requests.post(ACCESS_TOKEN_URL,params=access_token_parameters)
	access_token_result = token_result.json()    #stores the json form of the result 
	return access_token_result["access_token"]


def get_user_info(access_token):
	"""
	this function makes api calls to google resource server

	it exchanges access token to get user_info

	"""
	resource_parameters={

						"access_token":access_token,
						"Content-Type":"application/json"

					}
	user_info=requests.get(API_RESOURCE_URL, params=resource_parameters)
	my_user_info=user_info.json()
	return my_user_info


if __name__ == '__main__':
    app.run(debug=True)
