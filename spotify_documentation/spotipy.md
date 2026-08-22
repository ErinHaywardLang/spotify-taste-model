# Welcome to Spotipy! — spotipy 2.0 documentation


# Welcome to Spotipy!

_Spotipy_ is a lightweight Python library for the [Spotify Web API](https://developer.spotify.com/documentation/web-api/). With _Spotipy_ you get full access to all of the music data provided by the Spotify platform.


# Features

_Spotipy_ supports all of the features of the Spotify Web API including access to all end points, and support for user authorization. For details on the capabilities you are encouraged to review the [Spotify Web API](https://developer.spotify.com/documentation/web-api/) documentation.


# Installation

Install or upgrade _Spotipy_ with:

```bash
pip install spotipy --upgrade
```

You can also obtain the source code from the [Spotipy GitHub repository](https://github.com/plamere/spotipy).


# Getting Started

All methods require user authorization. You will need to register your app at [My Dashboard](https://developer.spotify.com/dashboard/applications) to get the credentials necessary to make authorized calls (a _client id_ and _client secret_).

_Spotipy_ supports two authorization flows:

> -   **Authorization Code flow** This method is suitable for long-running applications which the user logs into once. It provides an access token that can be refreshed.
>     
>     Note
>     
>     Requires you to add a redirect URI to your application at [My Dashboard](https://developer.spotify.com/dashboard/applications). See [Redirect URI](#redirect-uri) for more details.
>     
> -   **Client Credentials flow** This method makes it possible to authenticate your requests to the Spotify Web API and to obtain a higher rate limit than you would with the Authorization Code flow.
>     

For guidance on setting your app credentials watch this [video tutorial](https://youtu.be/kaBVN8uP358) or follow the [Spotipy Tutorial for Beginners](https://github.com/spotipy-dev/spotipy/blob/2.22.1/TUTORIAL.md).

For a longer tutorial with examples included, refer to this [video playlist](https://www.youtube.com/watch?v=tmt5SdvTqUI&list=PLqgOPibB_QnzzcaOFYmY2cQjs35y0is9N&index=1).


# Authorization Code Flow

This flow is suitable for long-running applications in which the user grants permission only once. It provides an access token that can be refreshed. Since the token exchange involves sending your secret key, perform this on a secure location, like a backend service, and not from a client such as a browser or from a mobile app.


## Quick start

To support the **Client Authorization Code Flow** _Spotipy_ provides a class SpotifyOAuth that can be used to authenticate requests like so:

```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " -- ", track['name'])
```

or if you are reluctant to immortalize your app credentials in your source code, you can set environment variables like so (use `$env:"credentials"` instead of `export` on Windows):

```bash
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```


## Scopes

See [Using Scopes](https://developer.spotify.com/documentation/web-api/concepts/scopes/) for information about scopes.


## Redirect URI

The **Authorization Code Flow** needs you to add a **redirect URI** to your application at [My Dashboard](https://developer.spotify.com/dashboard/applications) (navigate to your application and then _[Edit Settings]_).

The `redirect_uri` argument or `SPOTIPY_REDIRECT_URI` environment variable must match the redirect URI added to your application in your Dashboard. The redirect URI can be any valid URI (it does not need to be accessible) such as `http://example.com` or `http://127.0.0.1:9090`.

> Note
> 
> If you choose an http-scheme URL, and it’s for 127.0.0.1, **AND** it specifies a port, then spotipy will instantiate
> 
> > a server on the indicated response to receive the access token from the response at the end of the oauth flow ([see the code](https://github.com/plamere/spotipy/blob/master/spotipy/oauth2.py#L483-L490)).


# Client Credentials Flow

The Client Credentials flow is used in server-to-server authentication. Only endpoints that do not access user information can be accessed. The advantage here in comparison with requests to the Web API made without an access token, is that a higher rate limit is applied.

As opposed to the Authorization Code Flow, you will not need to set `SPOTIPY_REDIRECT_URI`, which means you will never be redirected to the sign in page in your browser:

```bash
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
```

To support the **Client Credentials Flow** _Spotipy_ provides a class SpotifyClientCredentials that can be used to authenticate requests like so:

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print(f"{i + 1 + playlists['offset']:4d} {playlist['uri']} {playlist['name']}")
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
```


# IDs URIs and URLs

_Spotipy_ supports a number of different ID types:

> -   **Spotify URI** - The resource identifier that you can enter, for example, in the Spotify Desktop client’s search box to locate an artist, album, or track. Example: `spotify:track:6rqhFgbbKwnb9MLmUQDhG6`
>     
> -   **Spotify URL** - An HTML link that opens a track, album, app, playlist or other Spotify resource in a Spotify client. Example: `http://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6`
>     
> -   **Spotify ID** - A base-62 number that you can find at the end of the Spotify URI (see above) for an artist, track, album, etc. Example: `6rqhFgbbKwnb9MLmUQDhG6`
>     

In general, any _Spotipy_ method that needs an artist, album, track or playlist ID will accept ids in any of the above form


# Customized token caching

Tokens are refreshed automatically and stored by default in the project main folder. As this might not suit everyone’s needs, spotipy provides a way to create customized cache handlers.

[https://github.com/plamere/spotipy/blob/master/spotipy/cache_handler.py](https://github.com/plamere/spotipy/blob/master/spotipy/cache_handler.py)

The custom cache handler would need to be a class that inherits from the base cache handler `CacheHandler`. The default cache handler `CacheFileHandler` is a good example. An instance of that new class can then be passed as a parameter when creating `SpotifyOAuth`, `SpotifyPKCE` or `SpotifyImplicitGrant`. The following handlers are available and defined in the URL above.

> -   `CacheFileHandler`
>     
> -   `MemoryCacheHandler`
>     
> -   `DjangoSessionCacheHandler`
>     
> -   `FlaskSessionCacheHandler`
>     
> -   `RedisCacheHandler`
>     
> -   `MemcacheCacheHandler`: install with dependency using `pip install "spotipy[pymemcache]"`
>     

Feel free to contribute new cache handlers to the repo.


# Examples

Here is an example of using _Spotipy_ to list the names of all the albums released by the artist ‘Birdy’:

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
```

Here’s another example showing how to get 30 second samples and cover art for the top 10 tracks for Led Zeppelin:

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
results = spotify.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
```

Finally, here’s an example that will get the URL for an artist image given the artist’s name:

```python
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    name = 'Radiohead'

results = spotify.search(q='artist:' + name, type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'], artist['images'][0]['url'])
```

There are many more examples of how to use _Spotipy_ in the [spotipy-examples repository](https://github.com/spotipy-dev/spotipy-examples) on GitHub.


# API Reference


# `client` Module

A simple and thin Python library for the Spotify Web API

_class_ spotipy.client.Spotify(_auth=None_, _requests_session=True_, _client_credentials_manager=None_, _oauth_manager=None_, _auth_manager=None_, _proxies=None_, _requests_timeout=5_, _status_forcelist=None_, _retries=3_, _status_retries=3_, _backoff_factor=0.3_, _language=None_)

Bases: `object`

Example usage:

```python
import spotipy

urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
sp = spotipy.Spotify()

artist = sp.artist(urn)
print(artist)

user = sp.user('plamere')
print(user)
```

__init__(_auth=None_, _requests_session=True_, _client_credentials_manager=None_, _oauth_manager=None_, _auth_manager=None_, _proxies=None_, _requests_timeout=5_, _status_forcelist=None_, _retries=3_, _status_retries=3_, _backoff_factor=0.3_, _language=None_)

Creates a Spotify API client.

Parameters:

-   **auth** -- An access token (optional)
    
-   **requests_session** -- A Requests session object or a truthy value to create one. A falsy value disables sessions. It should generally be a good idea to keep sessions enabled for performance reasons (connection pooling).
    
-   **client_credentials_manager** -- SpotifyClientCredentials object
    
-   **oauth_manager** -- SpotifyOAuth object
    
-   **auth_manager** -- SpotifyOauth, SpotifyClientCredentials, or SpotifyImplicitGrant object
    
-   **proxies** -- Definition of proxies (optional). See Requests doc [https://2.python-requests.org/en/master/user/advanced/#proxies](https://2.python-requests.org/en/master/user/advanced/#proxies)
    
-   **requests_timeout** -- Tell Requests to stop waiting for a response after a given number of seconds
    
-   **status_forcelist** -- Tell requests what type of status codes retries should occur on
    
-   **retries** -- Total number of retries to allow
    
-   **status_retries** -- Number of times to retry on bad status codes
    
-   **backoff_factor** -- A backoff factor to apply between attempts after the second try See urllib3 [https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html](https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html)
    
-   **language** -- The language parameter advertises what language the user prefers to see. See ISO-639-1 language code: [https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
    

add_to_queue(_uri_, _device_id=None_)

Adds a song to the end of a user’s queue

If device A is currently playing music, and you try to add to the queue and pass in the id for device B, you will get a ‘Player command failed: Restriction violated’ error I therefore recommend leaving device_id as None so that the active device is targeted

Parameters:

-   **uri** -- song uri, id, or url
    
-   **device_id** -- the id of a Spotify device. If None, then the active device is used.
    

album(_album_id_, _market=None_)

returns a single album given the album’s ID, URIs or URL

Parameters:

-   album_id - the album ID, URI or URL
    
-   market - an ISO 3166-1 alpha-2 country code
    

album_tracks(_album_id_, _limit=50_, _offset=0_, _market=None_)

Get Spotify catalog information about an album’s tracks

Parameters:

-   album_id - the album ID, URI or URL
    
-   limit - the number of items to return
    
-   offset - the index of the first item to return
    
-   market - an ISO 3166-1 alpha-2 country code.
    

albums(_albums_, _market=None_)

returns a list of albums given the album IDs, URIs, or URLs

Parameters:

-   albums - a list of album IDs, URIs or URLs
    
-   market - an ISO 3166-1 alpha-2 country code
    

artist(_artist_id_)

returns a single artist given the artist’s ID, URI or URL

Parameters:

-   artist_id - an artist ID, URI or URL
    

artist_albums(_artist_id_, _album_type=None_, _include_groups=None_, _country=None_, _limit=20_, _offset=0_)

Get Spotify catalog information about an artist’s albums

This method is deprecated and may be removed in a future version. Use artist_albums(…, include_groups=’…’) instead.

Parameters:

-   artist_id - the artist ID, URI or URL
    
-   include_groups - the types of items to return. One or more of ‘album’, ‘single’,
    
    ‘appears_on’, ‘compilation’. If multiple types are desired, pass in a comma separated string; e.g., ‘album,single’.
    
-   country - limit the response to one particular country.
    
-   limit - the number of albums to return
    
-   offset - the index of the first album to return
    

artist_related_artists(_artist_id_)

Get Spotify catalog information about artists similar to an identified artist. Similarity is based on analysis of the Spotify community’s listening history.

This endpoint has been removed by Spotify and is no longer available.

Parameters:

-   artist_id - the artist ID, URI or URL
    

artist_top_tracks(_artist_id_, _country='US'_)

Get Spotify catalog information about an artist’s top 10 tracks by country.

Parameters:

-   artist_id - the artist ID, URI or URL
    
-   country - limit the response to one particular country.
    

artists(_artists_)

returns a list of artists given the artist IDs, URIs, or URLs

Parameters:

-   artists - a list of artist IDs, URIs or URLs
    

audio_analysis(_track_id_)

Get audio analysis for a track based upon its Spotify ID

This endpoint has been removed by Spotify and is no longer available.

Parameters:

-   track_id - a track URI, URL or ID
    

audio_features(_tracks=[]_)

Get audio features for one or multiple tracks based upon their Spotify IDs

This endpoint has been removed by Spotify and is no longer available.

Parameters:

-   tracks - a list of track URIs, URLs or IDs, maximum: 100 ids
    

_property_ auth_manager

available_markets()

Get the list of markets where Spotify is available. Returns a list of the countries in which Spotify is available, identified by their ISO 3166-1 alpha-2 country code with additional country codes for special territories.

categories(_country=None_, _locale=None_, _limit=20_, _offset=0_)

Get a list of categories

Parameters:

-   country - An ISO 3166-1 alpha-2 country code.
    
-   locale - The desired language, consisting of an ISO 639-1 alpha-2 language code and an ISO 3166-1 alpha-2 country code, joined by an underscore.
    
-   limit - The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50
    
-   offset - The index of the first item to return. Default: 0 (the first object). Use with limit to get the next set of items.
    

category(_category_id_, _country=None_, _locale=None_)

Get info about a category

Parameters:

-   category_id - The Spotify category ID for the category.
    
-   country - An ISO 3166-1 alpha-2 country code.
    
-   locale - The desired language, consisting of an ISO 639-1 alpha-2 language code and an ISO 3166-1 alpha-2 country code, joined by an underscore.
    

category_playlists(_category_id=None_, _country=None_, _limit=20_, _offset=0_)

Get a list of playlists for a specific Spotify category

This endpoint has been removed by Spotify and is no longer available.

Parameters:

-   category_id - The Spotify category ID for the category.
    
-   country - An ISO 3166-1 alpha-2 country code.
    
-   limit - The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50
    
-   offset - The index of the first item to return. Default: 0 (the first object). Use with limit to get the next set of items.
    

country_codes _= ['AD', 'AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'EC', 'SV', 'EE', 'FI', 'FR', 'DE', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'ID', 'IE', 'IT', 'JP', 'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX', 'MC', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'ES', 'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 'UY']_

current_playback(_market=None_, _additional_types=None_)

Get information about user’s current playback.

Parameters:

-   market - an ISO 3166-1 alpha-2 country code.
    
-   additional_types - episode to get podcast track information
    

current_user()

Get detailed profile information about the current user. An alias for the ‘me’ method.

current_user_follow_playlist(_playlist_id_, _public=True_)

Add the current authenticated user as a follower of a playlist.

Parameters:

-   playlist_id - the id of the playlist
    

current_user_followed_artists(_limit=20_, _after=None_)

Gets a list of the artists followed by the current authorized user

Parameters:

-   limit - the number of artists to return
    
-   after - the last artist ID retrieved from the previous
    
    request
    

current_user_following_artists(_ids=None_)

Check if the current user is following certain artists

Returns list of booleans respective to ids

Parameters:

-   ids - a list of artist URIs, URLs or IDs
    

current_user_following_users(_ids=None_)

Check if the current user is following certain users

Returns list of booleans respective to ids

Parameters:

-   ids - a list of user URIs, URLs or IDs
    

current_user_playing_track(_market=None_, _additional_types=('track',)_)

Get information about the current users currently playing track.

Parameters:

-   market - An ISO 3166-1 alpha-2 country code or the
    
    string from_token.
    
-   additional_types - list of item types to return.
    
    valid types are: track and episode
    

current_user_playlists(_limit=50_, _offset=0_)

Get current user playlists without required getting his profile Parameters:

> -   limit - the number of items to return
>     
> -   offset - the index of the first item to return
>     

current_user_recently_played(_limit=50_, _after=None_, _before=None_)

Get the current user’s recently played tracks

Parameters:

-   limit - the number of entities to return
    
-   after - unix timestamp in milliseconds. Returns all items
    
    after (but not including) this cursor position. Cannot be used if before is specified.
    
-   before - unix timestamp in milliseconds. Returns all items
    
    before (but not including) this cursor position. Cannot be used if after is specified
    

current_user_saved_albums(_limit=20_, _offset=0_, _market=None_)

Gets a list of the albums saved in the current authorized user’s “Your Music” library

Parameters:

-   limit - the number of albums to return (MAX_LIMIT=50)
    
-   offset - the index of the first album to return
    
-   market - an ISO 3166-1 alpha-2 country code.
    

current_user_saved_albums_add(_albums=[]_)

Add one or more albums to the current user’s “Your Music” library. Parameters:

> -   albums - a list of album URIs, URLs or IDs
>     

current_user_saved_albums_contains(_albums=[]_)

Check if one or more albums is already saved in the current Spotify user’s “Your Music” library.

Parameters:

-   albums - a list of album URIs, URLs or IDs
    

current_user_saved_albums_delete(_albums=[]_)

Remove one or more albums from the current user’s “Your Music” library.

Parameters:

-   albums - a list of album URIs, URLs or IDs
    

current_user_saved_episodes(_limit=20_, _offset=0_, _market=None_)

Gets a list of the episodes saved in the current authorized user’s “Your Music” library

Parameters:

-   limit - the number of episodes to return
    
-   offset - the index of the first episode to return
    
-   market - an ISO 3166-1 alpha-2 country code
    

current_user_saved_episodes_add(_episodes=None_)

Add one or more episodes to the current user’s “Your Music” library.

Parameters:

-   episodes - a list of episode URIs, URLs or IDs
    

current_user_saved_episodes_contains(_episodes=None_)

Check if one or more episodes is already saved in the current Spotify user’s “Your Music” library.

Parameters:

-   episodes - a list of episode URIs, URLs or IDs
    

current_user_saved_episodes_delete(_episodes=None_)

Remove one or more episodes from the current user’s “Your Music” library.

Parameters:

-   episodes - a list of episode URIs, URLs or IDs
    

current_user_saved_shows(_limit=20_, _offset=0_, _market=None_)

Gets a list of the shows saved in the current authorized user’s “Your Music” library

Parameters:

-   limit - the number of shows to return
    
-   offset - the index of the first show to return
    
-   market - an ISO 3166-1 alpha-2 country code
    

current_user_saved_shows_add(_shows=[]_)

Add one or more albums to the current user’s “Your Music” library. Parameters:

> -   shows - a list of show URIs, URLs or IDs
>     

current_user_saved_shows_contains(_shows=[]_)

Check if one or more shows is already saved in the current Spotify user’s “Your Music” library.

Parameters:

-   shows - a list of show URIs, URLs or IDs
    

current_user_saved_shows_delete(_shows=[]_)

Remove one or more shows from the current user’s “Your Music” library.

Parameters:

-   shows - a list of show URIs, URLs or IDs
    

current_user_saved_tracks(_limit=20_, _offset=0_, _market=None_)

Gets a list of the tracks saved in the current authorized user’s “Your Music” library

Parameters:

-   limit - the number of tracks to return
    
-   offset - the index of the first track to return
    
-   market - an ISO 3166-1 alpha-2 country code
    

current_user_saved_tracks_add(_tracks=None_)

Add one or more tracks to the current user’s “Your Music” library.

Parameters:

-   tracks - a list of track URIs, URLs or IDs
    

current_user_saved_tracks_contains(_tracks=None_)

Check if one or more tracks is already saved in the current Spotify user’s “Your Music” library.

Parameters:

-   tracks - a list of track URIs, URLs or IDs
    

current_user_saved_tracks_delete(_tracks=None_)

Remove one or more tracks from the current user’s “Your Music” library.

Parameters:

-   tracks - a list of track URIs, URLs or IDs
    

current_user_top_artists(_limit=20_, _offset=0_, _time_range='medium_term'_)

Get the current user’s top artists

Parameters:

-   limit - the number of entities to return (max 50)
    
-   offset - the index of the first entity to return
    
-   time_range - Over what time frame are the affinities computed Valid-values: short_term, medium_term, long_term
    

current_user_top_tracks(_limit=20_, _offset=0_, _time_range='medium_term'_)

Get the current user’s top tracks

Parameters:

-   limit - the number of entities to return
    
-   offset - the index of the first entity to return
    
-   time_range - Over what time frame are the affinities computed Valid-values: short_term, medium_term, long_term
    

current_user_unfollow_playlist(_playlist_id_)

Unfollows (deletes) a playlist for the current authenticated user

Parameters:

-   playlist_id - the id of the playlist
    

currently_playing(_market=None_, _additional_types=None_)

Get user’s currently playing track.

Parameters:

-   market - an ISO 3166-1 alpha-2 country code.
    
-   additional_types - episode to get podcast track information
    

default_retry_codes _= (429, 500, 502, 503, 504)_

devices()

Get a list of user’s available devices.

episode(_episode_id_, _market=None_)

returns a single episode given the episode’s ID, URIs or URL

Parameters:

-   episode_id - the episode ID, URI or URL
    
-   market - an ISO 3166-1 alpha-2 country code.
    
    The episode must be available in the given market. If user-based authorization is in use, the user’s country takes precedence. If neither market nor user country are provided, the content is considered unavailable for the client.
    

episodes(_episodes_, _market=None_)

returns a list of episodes given the episode IDs, URIs, or URLs

Parameters:

-   episodes - a list of episode IDs, URIs or URLs
    
-   market - an ISO 3166-1 alpha-2 country code.
    
    Only episodes available in the given market will be returned. If user-based authorization is in use, the user’s country takes precedence. If neither market nor user country are provided, the content is considered unavailable for the client.
    

featured_playlists(_locale=None_, _country=None_, _timestamp=None_, _limit=20_, _offset=0_)

Get a list of Spotify featured playlists

This endpoint has been removed by Spotify and is no longer available.

Parameters:

-   locale - The desired language, consisting of a lowercase ISO 639-1 alpha-2 language code and an uppercase ISO 3166-1 alpha-2 country code, joined by an underscore.
    
-   country - An ISO 3166-1 alpha-2 country code.
    
-   timestamp - A timestamp in ISO 8601 format: yyyy-MM-ddTHH:mm:ss. Use this parameter to specify the user’s local time to get results tailored for that specific date and time in the day
    
-   limit - The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50
    
-   offset - The index of the first item to return. Default: 0 (the first object). Use with limit to get the next set of items.
    

get_audiobook(_id_, _market=None_)

Get Spotify catalog information for a single audiobook identified by its unique Spotify ID.

Parameters: - id - the Spotify ID for the audiobook - market - an ISO 3166-1 alpha-2 country code.

get_audiobook_chapters(_id_, _market=None_, _limit=20_, _offset=0_)

Get Spotify catalog information about an audiobook’s chapters.

Parameters: - id - the Spotify ID for the audiobook - market - an ISO 3166-1 alpha-2 country code. - limit - the maximum number of items to return - offset - the index of the first item to return

get_audiobooks(_ids_, _market=None_)

Get Spotify catalog information for multiple audiobooks based on their Spotify IDs.

Parameters: - ids - a list of Spotify IDs for the audiobooks - market - an ISO 3166-1 alpha-2 country code.

max_retries _= 3_

me()

Get detailed profile information about the current user. An alias for the ‘current_user’ method.

new_releases(_country=None_, _limit=20_, _offset=0_)

Get a list of new album releases featured in Spotify

Parameters:

-   country - An ISO 3166-1 alpha-2 country code.
    
-   limit - The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50
    
-   offset - The index of the first item to return. Default: 0 (the first object). Use with limit to get the next set of items.
    

next(_result_)

returns the next result given a paged result

Parameters:

-   result - a previously returned paged result
    

next_track(_device_id=None_)

Skip user’s playback to next track.

Parameters:

-   device_id - device target for playback
    

pause_playback(_device_id=None_)

Pause user’s playback.

Parameters:

-   device_id - device target for playback
    

playlist(_playlist_id_, _fields=None_, _market=None_, _additional_types=('track',)_)

Gets playlist by id.

Parameters:

-   playlist - the id of the playlist
    
-   fields - which fields to return
    
-   market - An ISO 3166-1 alpha-2 country code or the
    
    string from_token.
    
-   additional_types - list of item types to return.
    
    valid types are: track and episode
    

playlist_add_items(_playlist_id_, _items_, _position=None_)

Adds tracks/episodes to a playlist

Parameters:

-   playlist_id - the id of the playlist
    
-   items - a list of track/episode URIs or URLs
    
-   position - the position to add the tracks
    

playlist_change_details(_playlist_id_, _name=None_, _public=None_, _collaborative=None_, _description=None_)

Changes a playlist’s name and/or public/private state, collaborative state, and/or description

Parameters:

-   playlist_id - the id of the playlist
    
-   name - optional name of the playlist
    
-   public - optional is the playlist public
    
-   collaborative - optional is the playlist collaborative
    
-   description - optional description of the playlist
    

playlist_cover_image(_playlist_id_)

Get cover image of a playlist.

Parameters:

-   playlist_id - the playlist ID, URI or URL
    

playlist_is_following(_playlist_id_, _user_ids_)

Check to see if the given users are following the given playlist

Parameters:

-   playlist_id - the id of the playlist
    
-   user_ids - the ids of the users that you want to check to see
    
    if they follow the playlist. Maximum: 5 ids.
    

playlist_items(_playlist_id_, _fields=None_, _limit=100_, _offset=0_, _market=None_, _additional_types=('track', 'episode')_)

Get full details of the tracks and episodes of a playlist.

Parameters:

-   playlist_id - the playlist ID, URI or URL
    
-   fields - which fields to return
    
-   limit - the maximum number of tracks to return
    
-   offset - the index of the first track to return
    
-   market - an ISO 3166-1 alpha-2 country code.
    
-   additional_types - list of item types to return.
    
    valid types are: track and episode
    

playlist_remove_all_occurrences_of_items(_playlist_id_, _items_, _snapshot_id=None_)

Removes all occurrences of the given tracks/episodes from the given playlist

Parameters:

-   playlist_id - the id of the playlist
    
-   items - list of track/episode ids to remove from the playlist
    
-   snapshot_id - optional id of the playlist snapshot
    

playlist_remove_specific_occurrences_of_items(_playlist_id_, _items_, _snapshot_id=None_)

Removes all occurrences of the given tracks from the given playlist

Parameters:

-   playlist_id - the id of the playlist
    
-   items - an array of objects containing Spotify URIs of the
    
    tracks/episodes to remove with their current positions in the playlist. For example:
    
    > [ { “uri”:”4iV5W9uYEdYUVa79Axb7Rh”, “positions”:[2] }, { “uri”:”1301WleyT98MSxVHPZCA6M”, “positions”:[7] } ]
    
-   snapshot_id - optional id of the playlist snapshot
    

playlist_reorder_items(_playlist_id_, _range_start_, _insert_before_, _range_length=1_, _snapshot_id=None_)

Reorder tracks in a playlist

Parameters:

-   playlist_id - the id of the playlist
    
-   range_start - the position of the first track to be reordered
    
-   range_length - optional the number of tracks to be reordered
    
    (default: 1)
    
-   insert_before - the position where the tracks should be
    
    inserted
    
-   snapshot_id - optional playlist’s snapshot ID
    

playlist_replace_items(_playlist_id_, _items_)

Replace all tracks/episodes in a playlist

Parameters:

-   playlist_id - the id of the playlist
    
-   items - list of track/episode ids to comprise playlist
    

playlist_tracks(_playlist_id_, _fields=None_, _limit=100_, _offset=0_, _market=None_, _additional_types=('track',)_)

Get full details of the tracks of a playlist.

This method is deprecated and may be removed in a future version. Use playlist_items(playlist_id, …, additional_types=(‘track’,)) instead.

Parameters:

-   playlist_id - the playlist ID, URI or URL
    
-   fields - which fields to return
    
-   limit - the maximum number of tracks to return
    
-   offset - the index of the first track to return
    
-   market - an ISO 3166-1 alpha-2 country code.
    
-   additional_types - list of item types to return.
    
    valid types are: track and episode
    

playlist_upload_cover_image(_playlist_id_, _image_b64_)

Replace the image used to represent a specific playlist

Parameters:

-   playlist_id - the id of the playlist
    
-   image_b64 - image data as a Base64 encoded JPEG image string
    
    (maximum payload size is 256 KB)
    

previous(_result_)

returns the previous result given a paged result

Parameters:

-   result - a previously returned paged result
    

previous_track(_device_id=None_)

Skip user’s playback to previous track.

Parameters:

-   device_id - device target for playback
    

queue()

Gets the current user’s queue

recommendation_genre_seeds()

Get a list of genres available for the recommendations function.

This endpoint has been removed by Spotify and is no longer available.

recommendations(_seed_artists=None_, _seed_genres=None_, _seed_tracks=None_, _limit=20_, _country=None_, _**kwargs_)

Get a list of recommended tracks for one to five seeds. (at least one of seed_artists, seed_tracks and seed_genres are needed)

This endpoint has been removed by Spotify and is no longer available.

Parameters:

-   seed_artists - a list of artist IDs, URIs or URLs
    
-   seed_tracks - a list of track IDs, URIs or URLs
    
-   seed_genres - a list of genre names. Available genres for
    
    recommendations can be found by calling recommendation_genre_seeds
    
-   country - An ISO 3166-1 alpha-2 country code. If provided,
    
    all results will be playable in this country.
    
-   limit - The maximum number of items to return. Default: 20.
    
    Minimum: 1. Maximum: 100
    
-   min/max/target_<attribute> - For the tuneable track
    
    attributes listed in the documentation, these values provide filters and targeting on results.
    

repeat(_state_, _device_id=None_)

Set repeat mode for playback.

Parameters:

-   state - track, context, or off
    
-   device_id - device target for playback
    

search(_q_, _limit=10_, _offset=0_, _type='track'_, _market=None_)

searches for an item

Parameters:

-   q - the search query (see how to write a query in the
    
    official documentation [https://developer.spotify.com/documentation/web-api/reference/search/](https://developer.spotify.com/documentation/web-api/reference/search/)) # noqa

    
-   limit - the number of items to return (min = 1, default = 10, max = 50). The limit is applied
    
    within each type, not on the total response.
    
-   offset - the index of the first item to return
    
-   type - the types of items to return. One or more of ‘artist’, ‘album’,
    
    ‘track’, ‘playlist’, ‘show’, and ‘episode’. If multiple types are desired, pass in a comma separated string; e.g., ‘track,album,episode’.
    
-   market - An ISO 3166-1 alpha-2 country code or the string
    
    from_token.
    

search_markets(_q_, _limit=10_, _offset=0_, _type='track'_, _markets=None_, _total=None_)

(experimental) Searches multiple markets for an item

Parameters:

-   q - the search query (see how to write a query in the
    
    official documentation [https://developer.spotify.com/documentation/web-api/reference/search/](https://developer.spotify.com/documentation/web-api/reference/search/)) # noqa

    
-   limit - the number of items to return (min = 1, default = 10, max = 50). If a search is to be done on multiple
    
    markets, then this limit is applied to each market. (e.g. search US, CA, MX each with a limit of 10). If multiple types are specified, this applies to each type.
    
-   offset - the index of the first item to return
    
-   type - the types of items to return. One or more of ‘artist’, ‘album’,
    
    ‘track’, ‘playlist’, ‘show’, or ‘episode’. If multiple types are desired, pass in a comma separated string.
    
-   markets - A list of ISO 3166-1 alpha-2 country codes. Search all country markets by default.
    
-   total - the total number of results to return across multiple markets and types.
    

seek_track(_position_ms_, _device_id=None_)

Seek to position in current track.

Parameters:

-   position_ms - position in milliseconds to seek to
    
-   device_id - device target for playback
    

set_auth(_auth_)

show(_show_id_, _market=None_)

returns a single show given the show’s ID, URIs or URL

Parameters:

-   show_id - the show ID, URI or URL
    
-   market - an ISO 3166-1 alpha-2 country code.
    
    The show must be available in the given market. If user-based authorization is in use, the user’s country takes precedence. If neither market nor user country are provided, the content is considered unavailable for the client.
    

show_episodes(_show_id_, _limit=50_, _offset=0_, _market=None_)

Get Spotify catalog information about a show’s episodes

Parameters:

-   show_id - the show ID, URI or URL
    
-   limit - the number of items to return
    
-   offset - the index of the first item to return
    
-   market - an ISO 3166-1 alpha-2 country code.
    
    Only episodes available in the given market will be returned. If user-based authorization is in use, the user’s country takes precedence. If neither market nor user country are provided, the content is considered unavailable for the client.
    

shows(_shows_, _market=None_)

returns a list of shows given the show IDs, URIs, or URLs

Parameters:

-   shows - a list of show IDs, URIs or URLs
    
-   market - an ISO 3166-1 alpha-2 country code.
    
    Only shows available in the given market will be returned. If user-based authorization is in use, the user’s country takes precedence. If neither market nor user country are provided, the content is considered unavailable for the client.
    

shuffle(_state_, _device_id=None_)

Toggle playback shuffling.

Parameters:

-   state - true or false
    
-   device_id - device target for playback
    

start_playback(_device_id=None_, _context_uri=None_, _uris=None_, _offset=None_, _position_ms=None_)

Start or resume user’s playback.

Provide a context_uri to start playback of an album, artist, or playlist.

Provide a uris list to start playback of one or more tracks.

Provide offset as {“position”: <int>} or {“uri”: “<track uri>”} to start playback at a particular offset.

Parameters:

-   device_id - device target for playback
    
-   context_uri - spotify context uri to play
    
-   uris - spotify track uris
    
-   offset - offset into context by index or track
    
-   position_ms - (optional) indicates from what position to start playback.
    
    Must be a positive number. Passing in a position that is greater than the length of the track will cause the player to start playing the next song.
    

track(_track_id_, _market=None_)

returns a single track given the track’s ID, URI or URL

Parameters:

-   track_id - a spotify URI, URL or ID
    
-   market - an ISO 3166-1 alpha-2 country code.
    

tracks(_tracks_, _market=None_)

returns a list of tracks given a list of track IDs, URIs, or URLs

Parameters:

-   tracks - a list of spotify URIs, URLs or IDs. Maximum: 50 IDs.
    
-   market - an ISO 3166-1 alpha-2 country code.
    

transfer_playback(_device_id_, _force_play=True_)

Transfer playback to another device. Note that the API accepts a list of device ids, but only actually supports one.

Parameters:

-   device_id - transfer playback to this device
    
-   force_play - true: after transfer, play. false:
    
    keep current state.
    

user(_user_)

Gets basic profile information about a Spotify User

Parameters:

-   user - the id of the usr
    

user_follow_artists(_ids=[]_)

Follow one or more artists Parameters:

> -   ids - a list of artist IDs
>     

user_follow_users(_ids=[]_)

Follow one or more users Parameters:

> -   ids - a list of user IDs
>     

user_playlist(_user_, _playlist_id=None_, _fields=None_, _market=None_)

Gets a single playlist of a user

This method is deprecated and may be removed in a future version. Use playlist(playlist_id) instead.

Parameters:

-   user - the id of the user
    
-   playlist_id - the id of the playlist
    
-   fields - which fields to return
    

user_playlist_add_episodes(_user_, _playlist_id_, _episodes_, _position=None_)

This function is no longer in use, please use the recommended function in the warning!

Adds episodes to a playlist

This method is deprecated and may be removed in a future version. Use playlist_add_items(playlist_id, episodes) instead.

Parameters:

-   user - the id of the user
    
-   playlist_id - the id of the playlist
    
-   episodes - a list of track URIs, URLs or IDs
    
-   position - the position to add the episodes
    

user_playlist_add_tracks(_user_, _playlist_id_, _tracks_, _position=None_)

This function is no longer in use, please use the recommended function in the warning!

Adds tracks to a playlist

This method is deprecated and may be removed in a future version. Use playlist_add_items(playlist_id, tracks) instead.

Parameters:

-   user - the id of the user
    
-   playlist_id - the id of the playlist
    
-   tracks - a list of track URIs, URLs or IDs
    
-   position - the position to add the tracks
    

user_playlist_change_details(_user_, _playlist_id_, _name=None_, _public=None_, _collaborative=None_, _description=None_)

This function is no longer in use, please use the recommended function in the warning!

Changes a playlist’s name and/or public/private state

This method is deprecated and may be removed in a future version. Use playlist_change_details(playlist_id, …) instead.

Parameters:

-   user - the id of the user
    
-   playlist_id - the id of the playlist
    
-   name - optional name of the playlist
    
-   public - optional is the playlist public
    
-   collaborative - optional is the playlist collaborative
    
-   description - optional description of the playlist
    

user_playlist_create(_user_, _name_, _public=True_, _collaborative=False_, _description=''_)

Creates a playlist for a user

Parameters:

-   user - the id of the user
    
-   name - the name of the playlist
    
-   public - is the created playlist public
    
-   collaborative - is the created playlist collaborative
    
-   description - the description of the playlist
    

user_playlist_follow_playlist(_playlist_owner_id_, _playlist_id_)

This function is no longer in use, please use the recommended function in the warning!

Add the current authenticated user as a follower of a playlist.

This method is deprecated and may be removed in a future version. Use current_user_follow_playlist(playlist_id) instead.

Parameters:

-   playlist_owner_id - the user id of the playlist owner
    
-   playlist_id - the id of the playlist
    

user_playlist_is_following(_playlist_owner_id_, _playlist_id_, _user_ids_)

This function is no longer in use, please use the recommended function in the warning!

Check to see if the given users are following the given playlist

This method is deprecated and may be removed in a future version. Use playlist_is_following(playlist_id, user_ids) instead.

Parameters:

-   playlist_owner_id - the user id of the playlist owner
    
-   playlist_id - the id of the playlist
    
-   user_ids - the ids of the users that you want to check to see
    
    if they follow the playlist. Maximum: 5 ids.
    

user_playlist_remove_all_occurrences_of_tracks(_user_, _playlist_id_, _tracks_, _snapshot_id=None_)

This function is no longer in use, please use the recommended function in the warning!

Removes all occurrences of the given tracks from the given playlist

This method is deprecated and may be removed in a future version. Use playlist_remove_all_occurrences_of_items(playlist_id, tracks) instead.

Parameters:

-   user - the id of the user
    
-   playlist_id - the id of the playlist
    
-   tracks - the list of track ids to remove from the playlist
    
-   snapshot_id - optional id of the playlist snapshot
    

user_playlist_remove_specific_occurrences_of_tracks(_user_, _playlist_id_, _tracks_, _snapshot_id=None_)

This function is no longer in use, please use the recommended function in the warning!

Removes specific occurrences of the given tracks from the given playlist

This endpoint has been removed by Spotify and is no longer available.

Parameters:

-   user - the id of the user
    
-   playlist_id - the id of the playlist
    
-   tracks - an array of objects containing Spotify URIs of the
    
    tracks to remove with their current positions in the playlist. For example:
    
    > [ { “uri”:”4iV5W9uYEdYUVa79Axb7Rh”, “positions”:[2] }, { “uri”:”1301WleyT98MSxVHPZCA6M”, “positions”:[7] } ]
    
-   snapshot_id - optional id of the playlist snapshot
    

user_playlist_reorder_tracks(_user_, _playlist_id_, _range_start_, _insert_before_, _range_length=1_, _snapshot_id=None_)

This function is no longer in use, please use the recommended function in the warning!

Reorder tracks in a playlist from a user

This method is deprecated and may be removed in a future version. Use playlist_reorder_items(playlist_id, …) instead.

Parameters:

-   user - the id of the user
    
-   playlist_id - the id of the playlist
    
-   range_start - the position of the first track to be reordered
    
-   range_length - optional the number of tracks to be reordered
    
    (default: 1)
    
-   insert_before - the position where the tracks should be
    
    inserted
    
-   snapshot_id - optional playlist’s snapshot ID
    

user_playlist_replace_tracks(_user_, _playlist_id_, _tracks_)

This function is no longer in use, please use the recommended function in the warning!

Replace all tracks in a playlist for a user

This method is deprecated and may be removed in a future version. Use playlist_replace_items(playlist_id, tracks) instead.

Parameters:

-   user - the id of the user
    
-   playlist_id - the id of the playlist
    
-   tracks - the list of track ids to add to the playlist
    

user_playlist_tracks(_user=None_, _playlist_id=None_, _fields=None_, _limit=100_, _offset=0_, _market=None_)

Get full details of the tracks of a playlist owned by a user.

This method is deprecated and may be removed in a future version. Use playlist_tracks(playlist_id) instead.

Parameters:

-   user - the id of the user
    
-   playlist_id - the id of the playlist
    
-   fields - which fields to return
    
-   limit - the maximum number of tracks to return
    
-   offset - the index of the first track to return
    
-   market - an ISO 3166-1 alpha-2 country code.
    

user_playlist_unfollow(_user_, _playlist_id_)

This function is no longer in use, please use the recommended function in the warning!

Unfollows (deletes) a playlist for a user

This method is deprecated and may be removed in a future version. Use current_user_unfollow_playlist(playlist_id) instead.

Parameters:

-   user - the id of the user
    
-   name - the name of the playlist
    

user_playlists(_user_, _limit=50_, _offset=0_)

Gets playlists of a user

Parameters:

-   user - the id of the usr
    
-   limit - the number of items to return
    
-   offset - the index of the first item to return
    

user_unfollow_artists(_ids=[]_)

Unfollow one or more artists Parameters:

> -   ids - a list of artist IDs
>     

user_unfollow_users(_ids=[]_)

Unfollow one or more users Parameters:

> -   ids - a list of user IDs
>     

volume(_volume_percent_, _device_id=None_)

Set playback volume.

Parameters:

-   volume_percent - volume between 0 and 100
    
-   device_id - device target for playback
    

_exception_ spotipy.client.SpotifyException(_http_status_, _code_, _msg_, _reason=None_, _headers=None_)

Bases: `SpotifyBaseException`

__init__(_http_status_, _code_, _msg_, _reason=None_, _headers=None_)


# `oauth2` Module

_class_ spotipy.oauth2.SpotifyClientCredentials(_client_id=None_, _client_secret=None_, _proxies=None_, _requests_session=True_, _requests_timeout=None_, _cache_handler=None_)

Bases: `SpotifyAuthBase`

OAUTH_TOKEN_URL _= 'https://accounts.spotify.com/api/token'_

__init__(_client_id=None_, _client_secret=None_, _proxies=None_, _requests_session=True_, _requests_timeout=None_, _cache_handler=None_)

Creates a Client Credentials Flow Manager.

The Client Credentials flow is used in server-to-server authentication. Only endpoints that do not access user information can be accessed. This means that endpoints that require authorization scopes cannot be accessed. The advantage, however, of this authorization flow is that it does not require any user interaction

You can either provide a client_id and client_secret to the constructor or set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables

Parameters:

-   client_id: Must be supplied or set as environment variable
    
-   client_secret: Must be supplied or set as environment variable
    
-   proxies: Optional, proxy for the requests library to route through
    
-   requests_session: A Requests session
    
-   requests_timeout: Optional, tell Requests to stop waiting for a response after
    
    a given number of seconds
    
-   cache_handler: An instance of the CacheHandler class to handle
    
    getting and saving cached authorization tokens. Optional, will otherwise use CacheFileHandler. (takes precedence over cache_path and username)
    

get_access_token(_as_dict=True_, _check_cache=True_)

If a valid access token is in memory, returns it Else fetches a new token and returns it

> Parameters: - as_dict: (deprecated) a boolean indicating if returning the access token
> 
> > as a token_info dictionary, otherwise it will be returned as a string.

_class_ spotipy.oauth2.SpotifyImplicitGrant(_client_id=None_, _redirect_uri=None_, _state=None_, _scope=None_, _cache_path=None_, _username=None_, _show_dialog=False_, _cache_handler=None_)

Bases: `SpotifyAuthBase`

Implements Implicit Grant Flow for client apps

This auth manager enables _user and non-user_ endpoints with only a client secret, redirect uri, and username. The user will need to copy and paste a URI from the browser every hour.


## Security Warning

The OAuth standard no longer recommends the Implicit Grant Flow for client-side code. Spotify has implemented the OAuth-suggested PKCE extension that removes the need for a client secret in the Authentication Code flow. Use the SpotifyPKCE auth manager instead of SpotifyImplicitGrant.

SpotifyPKCE contains all the functionality of SpotifyImplicitGrant, plus automatic response retrieval and refreshable tokens. Only a few replacements need to be made:

-   get_auth_response()[‘access_token’] -> get_access_token(get_authorization_code())
    
-   get_auth_response() -> get_access_token(get_authorization_code()); get_cached_token()
    
-   parse_response_token(url)[‘access_token’] -> get_access_token(parse_response_code(url))
    
-   parse_response_token(url) -> get_access_token(parse_response_code(url)); get_cached_token()
    

The security concern in the Implicit Grant flow is that the token is returned in the URL and can be intercepted through the browser. A request with an authorization code and proof of origin could not be easily intercepted without a compromised network.

OAUTH_AUTHORIZE_URL _= 'https://accounts.spotify.com/authorize'_

__init__(_client_id=None_, _redirect_uri=None_, _state=None_, _scope=None_, _cache_path=None_, _username=None_, _show_dialog=False_, _cache_handler=None_)

Creates Auth Manager using the Implicit Grant flow

**See help(SpotifyImplicitGrant) for full Security Warning**


### Parameters

-   client_id: Must be supplied or set as environment variable
    
-   redirect_uri: Must be supplied or set as environment variable
    
-   state: May be supplied, no verification is performed
    
-   scope: Optional, either a list of scopes or comma separated string of scopes.
    
    e.g, “playlist-read-private,playlist-read-collaborative”
    
-   cache_handler: An instance of the CacheHandler class to handle
    
    getting and saving cached authorization tokens. May be supplied, will otherwise use CacheFileHandler. (takes precedence over cache_path and username)
    
-   cache_path: (deprecated) May be supplied, will otherwise be generated
    
    (takes precedence over username)
    
-   username: (deprecated) May be supplied or set as environment variable
    
    (will set cache_path to .cache-{username})
    
-   show_dialog: Interpreted as boolean
    

get_access_token(_state=None_, _response=None_, _check_cache=True_)

Gets Auth Token from cache (preferred) or user interaction


### Parameters

-   state: May be given, overrides (without changing) self.state
    
-   response: URI with token, can break expiration checks
    
-   check_cache: Interpreted as boolean
    

get_auth_response(_state=None_)

Gets a new auth **token** with user interaction

get_authorize_url(_state=None_)

Gets the URL to use to authorize this app

get_cached_token()

Gets the cached token for the app

This method is deprecated and may be removed in a future version.

_static_ parse_auth_response_url(_url_)

parse_response_token(_url_, _state=None_)

Parse the response code in the given response url

validate_token(_token_info_)

_class_ spotipy.oauth2.SpotifyOAuth(_client_id=None_, _client_secret=None_, _redirect_uri=None_, _state=None_, _scope=None_, _cache_path=None_, _username=None_, _proxies=None_, _show_dialog=False_, _requests_session=True_, _requests_timeout=None_, _open_browser=True_, _cache_handler=None_)

Bases: `SpotifyAuthBase`

Implements Authorization Code Flow for Spotify’s OAuth implementation.

OAUTH_AUTHORIZE_URL _= 'https://accounts.spotify.com/authorize'_

OAUTH_TOKEN_URL _= 'https://accounts.spotify.com/api/token'_

__init__(_client_id=None_, _client_secret=None_, _redirect_uri=None_, _state=None_, _scope=None_, _cache_path=None_, _username=None_, _proxies=None_, _show_dialog=False_, _requests_session=True_, _requests_timeout=None_, _open_browser=True_, _cache_handler=None_)

Creates a SpotifyOAuth object

Parameters:

-   client_id: Must be supplied or set as environment variable
    
-   client_secret: Must be supplied or set as environment variable
    
-   redirect_uri: Must be supplied or set as environment variable
    
-   state: Optional, no verification is performed
    
-   scope: Optional, either a list of scopes or comma separated string of scopes.
    
    e.g, “playlist-read-private,playlist-read-collaborative”
    
-   cache_path: (deprecated) Optional, will otherwise be generated
    
    (takes precedence over username)
    
-   username: (deprecated) Optional or set as environment variable
    
    (will set cache_path to .cache-{username})
    
-   proxies: Optional, proxy for the requests library to route through
    
-   show_dialog: Optional, interpreted as boolean
    
-   requests_session: A Requests session
    
-   requests_timeout: Optional, tell Requests to stop waiting for a response after
    
    a given number of seconds
    
-   open_browser: Optional, whether the web browser should be opened to
    
    authorize a user
    
-   cache_handler: An instance of the CacheHandler class to handle
    
    getting and saving cached authorization tokens. Optional, will otherwise use CacheFileHandler. (takes precedence over cache_path and username)
    

get_access_token(_code=None_, _as_dict=True_, _check_cache=True_)

Gets the access token for the app given the code

Parameters:

-   code: the response code
    
-   as_dict: (deprecated) a boolean indicating if returning the access token
    
    as a token_info dictionary, otherwise it will be returned as a string.
    

get_auth_response(_open_browser=None_)

get_authorization_code(_response=None_)

get_authorize_url(_state=None_)

Gets the URL to use to authorize this app

get_cached_token()

Gets the cached token for the app

This method is deprecated and may be removed in a future version.

_static_ parse_auth_response_url(_url_)

parse_response_code(_url_)

Parse the response code in the given response url

Parameters:

-   url - the response url
    

refresh_access_token(_refresh_token_)

validate_token(_token_info_)

_exception_ spotipy.oauth2.SpotifyOauthError(_message_, _error=None_, _error_description=None_, _*args_, _**kwargs_)

Bases: `SpotifyBaseException`

Error during Auth Code or Implicit Grant flow

__init__(_message_, _error=None_, _error_description=None_, _*args_, _**kwargs_)

_class_ spotipy.oauth2.SpotifyPKCE(_client_id=None_, _redirect_uri=None_, _state=None_, _scope=None_, _cache_path=None_, _username=None_, _proxies=None_, _requests_timeout=None_, _requests_session=True_, _open_browser=True_, _cache_handler=None_)

Bases: `SpotifyAuthBase`

Implements PKCE Authorization Flow for client apps

This auth manager enables _user and non-user_ endpoints with only a client ID, redirect URI, and username. When the app requests an access token for the first time, the user is prompted to authorize the new client app. After authorizing the app, the client app is then given both access and refresh tokens. This is the preferred way of authorizing a mobile/desktop client.

OAUTH_AUTHORIZE_URL _= 'https://accounts.spotify.com/authorize'_

OAUTH_TOKEN_URL _= 'https://accounts.spotify.com/api/token'_

__init__(_client_id=None_, _redirect_uri=None_, _state=None_, _scope=None_, _cache_path=None_, _username=None_, _proxies=None_, _requests_timeout=None_, _requests_session=True_, _open_browser=True_, _cache_handler=None_)

Creates Auth Manager with the PKCE Auth flow.

Parameters:

-   client_id: Must be supplied or set as environment variable
    
-   redirect_uri: Must be supplied or set as environment variable
    
-   state: Optional, no verification is performed
    
-   scope: Optional, either a list of scopes or comma separated string of scopes.
    
    e.g, “playlist-read-private,playlist-read-collaborative”
    
-   cache_path: (deprecated) Optional, will otherwise be generated
    
    (takes precedence over username)
    
-   username: (deprecated) Optional or set as environment variable
    
    (will set cache_path to .cache-{username})
    
-   proxies: Optional, proxy for the requests library to route through
    
-   requests_timeout: Optional, tell Requests to stop waiting for a response after
    
    a given number of seconds
    
-   requests_session: A Requests session
    
-   open_browser: Optional, whether the web browser should be opened to
    
    authorize a user
    
-   cache_handler: An instance of the CacheHandler class to handle
    
    getting and saving cached authorization tokens. Optional, will otherwise use CacheFileHandler. (takes precedence over cache_path and username)
    

get_access_token(_code=None_, _check_cache=True_)

Gets the access token for the app

If the code is not given and no cached token is used, an authentication window will be shown to the user to get a new code.

Parameters:

-   code - the response code from authentication
    
-   check_cache - if true, checks for a locally stored token
    
    before requesting a new token
    

get_authorization_code(_response=None_)

get_authorize_url(_state=None_)

Gets the URL to use to authorize this app

get_cached_token()

get_pkce_handshake_parameters()

_static_ parse_auth_response_url(_url_)

parse_response_code(_url_)

Parse the response code in the given response url

Parameters:

-   url - the response url
    

refresh_access_token(_refresh_token_)

validate_token(_token_info_)

_exception_ spotipy.oauth2.SpotifyStateError(_local_state=None_, _remote_state=None_, _message=None_, _error=None_, _error_description=None_, _*args_, _**kwargs_)

Bases: [`SpotifyOauthError`](#spotipy.oauth2.SpotifyOauthError "spotipy.exceptions.SpotifyOauthError")

The state sent and state received were different

__init__(_local_state=None_, _remote_state=None_, _message=None_, _error=None_, _error_description=None_, _*args_, _**kwargs_)


## `util` Module

spotipy.util.prompt_for_user_token(_username=None_, _scope=None_, _client_id=None_, _client_secret=None_, _redirect_uri=None_, _cache_path=None_, _oauth_manager=None_, _show_dialog=False_)

Prompt the user to login if necessary and returns a user token suitable for use with the spotipy.Spotify constructor.

Deprecated since version This: method is deprecated and may be removed in a future version.

Parameters:

-   username - the Spotify username. (optional)
    
-   scope - the desired scope of the request. (optional)
    
-   client_id - the client ID of your app. (required)
    
-   client_secret - the client secret of your app. (required)
    
-   redirect_uri - the redirect URI of your app. (required)
    
-   cache_path - path to location to save tokens. (required)
    
-   oauth_manager - OAuth manager object. (optional)
    
-   show_dialog - If True, a login prompt always shows or defaults to False. (optional)
    


# Support

You can ask questions about Spotipy on Stack Overflow. Don’t forget to add the _Spotipy_ tag, and any other relevant tags as well, before posting.

> [http://stackoverflow.com/questions/ask](http://stackoverflow.com/questions/ask)

If you think you’ve found a bug, let us know at [Spotipy Issues](https://github.com/plamere/spotipy/issues)


# Contribute

If you are a developer with Python experience, and you would like to contribute to Spotipy, please be sure to follow the guidelines listed below:

Export the needed Environment variables:

```bash
export SPOTIPY_CLIENT_ID=client_id_here 
export SPOTIPY_CLIENT_SECRET=client_secret_here 
export SPOTIPY_CLIENT_USERNAME=client_username_here  # This is actually an id not spotify display name 

export SPOTIPY_REDIRECT_URI=http://127.0.0.1:8080  # Make url is set in app you created to get your ID and SECRET

```

Create virtual environment, install dependencies, run tests:

```bash
$ virtualenv --python=python3.12 env 
(env) $ pip install --user -e . 
(env) $ python -m unittest discover -v tests
```

**Lint**

To automatically fix the code style:

```bash
pip install autopep8 
autopep8 --in-place --aggressive --recursive .
```

To verify the code style:

```bash
pip install flake8 
flake8 .
```

To make sure if the import lists are stored correctly:

```bash
pip install isort 
isort . -c -v
```

**Publishing (by maintainer)**

-   Bump version in setup.py
    
-   Bump and date changelog
    
-   Add to changelog:

```

## Unreleased

// Add your changes here and then delete this line
```

-   Commit changes
    
-   Package to pypi:

```bash
python setup.py sdist bdist_wheel 
python3 setup.py sdist bdist_wheel 
twine check dist/* 
twine upload --repository-url https://upload.pypi.org/legacy/ --skip-existing dist/_.(whl|gz|zip)~dist/*linux_.whl
```

-   Create github release [https://github.com/plamere/spotipy/releases](https://github.com/plamere/spotipy/releases) with the changelog content for the version and a short name that describes the main addition
    
-   Build the documentation again to ensure it’s on the latest version
    

**Changelog**

Don’t forget to add a short description of your change in the [CHANGELOG](https://github.com/plamere/spotipy/blob/master/CHANGELOG.md)!


# License

(Taken from [https://github.com/plamere/spotipy/blob/master/LICENSE.md](https://github.com/plamere/spotipy/blob/master/LICENSE.md)):

MIT License
Copyright (c) 2021 Paul Lamere
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Indices and tables

-   [Index](#)
    
-   [Module Index](#)
    
-   [Search Page](#)