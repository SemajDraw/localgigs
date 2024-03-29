from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import render

from rest_framework import permissions, authentication, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from . import serializers, ticketmaster, spotify
import json


# Django-rest-auth classes
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


@receiver(user_logged_in)
@login_required
@permission_classes((permissions.IsAuthenticated, ))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def get_users_spotify_details(request, **kwargs):
    """
    Make a GET request to the spotify API for the users playlist IDs
    :param request: Incoming request
    :return: Result in Json
    """
    if request.user.social_auth.exists():
        user = request.user
        if user.is_authenticated:
            try:
                res = spotify.get_user_details(user)
                return res
            except Exception as e:
                print(e)
        else:
            print('Not a valid user')
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        pass


@receiver(user_logged_in)
@login_required
@permission_classes((permissions.IsAuthenticated, ))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def get_spotify_playlist_artist_count(request, **kwargs):
    """
    Make a GET request to the spotify API for the users playlist IDs
    :param request: Incoming request search and city string
    :return: Result in Json
    """
    if request.user.social_auth.exists():
        user = request.user
        if user.is_authenticated:
            try:
                res = spotify.update_user_spotify_details(request, user)
                update_recommended_events(request)
                return res
            except Exception as e:
                print(e)
        else:
            print('Not a valid user')
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        pass


def update_recommended_events(request):
    try:
        user_id = request.user.id
        user_ip = request.META.get('REMOTE_ADDR', None)
        ticketmaster.update_recommended_events(user_id, user_ip)
    except Exception as e:
        print('Event update failed...')


# Allows an authenticated user to make a call to the Ticketmaster API with search parameter
@login_required
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def search_ticketmaster_events(request):
    """
    Make a GET request to the ticketmaster API with the strings entered by the user
    :param request: Incoming request search and city string
    :return: Result in Json
    """
    if request.method == 'GET':
        try:
            event_list = ticketmaster.search_ticketmaster(request)
            return render(request, 'app/events.html', {'event_list': event_list})

        except Exception as e:
            return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Returns a list of recommended gig objects for a user
@login_required
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def render_recommended_events(request):
    """
    Make a GET request to the ticketmaster API with a list of the users recommended artists
    :param request: Incoming request search and city string
    :return: Result in Json
    """
    if request.method == 'GET':
        try:
            event_list = request.user.profile.recommended_events
            return render(request, 'app/events.html', {'event_list': event_list})

        except Exception as e:
            return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@login_required
@permission_classes((permissions.IsAuthenticated, ))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def update_saved_events(request):

    if request.method == 'POST':
        try:
            user = request.user
            serializer = serializers.ProfileSerializer
            if user.is_authenticated:
                if user.profile.saved_events == "[]":
                    saved_events = json.loads(user.profile.saved_events)
                else:
                    saved_events = user.profile.saved_events

                new_event = json.loads(request.POST['save_event'])

                if not any(event['name'] == new_event['name']
                       and event['date'] == new_event['date'] for event in saved_events):

                    saved_events.append(new_event)
                    serializer.update(serializer, user.profile, {'saved_events': saved_events})
                    return Response(status=status.HTTP_200_OK)
                else:
                    pass

        except Exception as e:
            print(e)
            return Response({"detail": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@login_required
@permission_classes((permissions.IsAuthenticated, ))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def delete_saved_event(request):

    if request.method == 'POST':
        try:
            user = request.user
            serializer = serializers.ProfileSerializer
            if user.is_authenticated:
                saved_events = user.profile.saved_events
                delete_event = json.loads(request.POST['save_event'])
                saved_events[:] = [event for event in saved_events if not
                (event['name'] == delete_event['name'] and event['date'] == delete_event['date'])]

                serializer.update(serializer, user.profile, {'saved_events': saved_events})
                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@login_required
@permission_classes((permissions.IsAuthenticated, ))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def get_saved_events(request):

    if request.method == 'GET':
        try:
            user = request.user
            saved_events = user.profile.saved_events
            return Response({'event_list': saved_events}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


# Returns a list of recommended gig objects for a user
@login_required
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def get_recommended_events(request):
    """
    Make a GET request to the ticketmaster API with a list of the users recommended artists
    :param request: Incoming request search and city string
    :return: Result in Json
    """
    if request.method == 'GET':
        try:
            event_list = request.user.profile.recommended_events
            return Response({'event_list': event_list}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# # Returns a list of recommended gig objects for a user
# @api_view(['GET', ])
# @login_required
# @permission_classes((permissions.IsAuthenticated,))
# @authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
# def get_recommender_model_events(request):
#     """
#     Make a GET request to the ticketmaster API with a list of the users recommended artists
#     :param request: Incoming request search and city string
#     :return: Result in Json
#     """
#     if request.method == 'GET':
#         user = request.user
#         try:
#             user_artist_count = user.spotify.artist_count
#             user_email = user.email
#             res = requests.post('http://127.0.0.1:8001/api/get_recommendations/',
#                                 data={user_email: json.dumps(user_artist_count)})
#             recommended_artists = json.loads(res.content)['recommended_artists']
#
#         except Exception as e:
#             print(e)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# Allows an authenticated user to make a call to the Ticketmaster API with search parameter
@login_required
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def get_ticketmaster_events(request):
    """
    Make a GET request to the ticketmaster API with the strings entered by the user
    :param request: Incoming request search and city string
    :return: Result in Json
    """
    if request.method == 'GET':
        try:
            event_list = ticketmaster.search_ticketmaster(request)
            return Response({'event_list': event_list}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# API login for mobile application that returns the users profile information
# and an authentication token
@api_view(["GET", ])
@permission_classes((permissions.AllowAny,))
def token_login(request):
    if (not request.GET["email"]) or (not request.GET["password"]):
        return Response({"detail": "Missing email and/or password"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=request.GET["email"], password=request.GET["password"])
    if user:
        if user.is_active:
            login(request, user)
            try:
                my_token = Token.objects.get(user=user)
                first_name = user.first_name
                last_name = user.last_name
                return Response({"token": "{}".format(my_token.key),
                                 "first_name": "{}".format(first_name),
                                 "last_name": "{}".format(last_name),
                                 },
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": "Could not get token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Inactive account"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Invalid User Id of Password"}, status=status.HTTP_400_BAD_REQUEST)
