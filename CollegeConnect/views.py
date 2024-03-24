from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from allauth.socialaccount.providers.linkedin_oauth2.provider import LinkedInOAuth2Provider
from allauth.socialaccount.helpers import complete_social_login
from django.views.generic import View
from django.shortcuts import redirect
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from allauth.socialaccount.providers.linkedin_oauth2.provider import LinkedInOAuth2Provider
from allauth.socialaccount.helpers import complete_social_login

from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from allauth.socialaccount.providers.linkedin_oauth2.provider import LinkedInOAuth2Provider
from allauth.socialaccount.helpers import complete_social_login
from django.views.generic import View
from django.shortcuts import redirect

class CustomLinkedInOAuth2Adapter(OAuth2Adapter):
    provider_id = LinkedInOAuth2Provider.id
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    authorize_url = 'https://www.linkedin.com/oauth/v2/authorization'
    profile_url = 'https://api.linkedin.com/v2/me'

    def complete_login(self, request, app, token, **kwargs):
        login = self.get_provider().sociallogin_from_response(request, token, **kwargs)
        return login

    def __init__(self, request=None):
        super().__init__(request)

class CustomOAuth2LoginView(OAuth2LoginView, View):  
    adapter_class = CustomLinkedInOAuth2Adapter

    def dispatch(self, request, *args, **kwargs):
        self.adapter = self.adapter_class(request)
        return super().dispatch(request, *args, **kwargs)

def linkedin_signup(request):
    return redirect('oauth2_login')