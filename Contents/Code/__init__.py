MUSIC_PREFIX = "/music/soundopinions"

NAME = "Sound Opinions"

USERID = "22158614"
CLIENT_ID = "560278700e21a4d6d7bf9a8eb359714c"
CLIENT_SECRET = "601d78e647ac804ca92b8b07f6dba8cd"

TRACKS_URL = "http://api.soundcloud.com/users/22158614/tracks?client_id=560278700e21a4d6d7bf9a8eb359714c&limit=5000"

ART  = 'art-default.jpg'
ICON = 'icon-default.jpg'

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(MUSIC_PREFIX, MusicMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "InfoList"
    MediaContainer.art = R(ART)

    HTTP.CacheTime = 0



def MusicMainMenu():

    dir = ProcessRequest(url = TRACKS_URL, title = 'Episodes', params = {'order': 'created_at'})

    return dir

def ProcessRequest(url, title, params, offset = 0, id = -1):
    request = JSON.ObjectFromURL(url, cacheTime = 0)

    oc = ObjectContainer(title2 = title)
    if 'errors' in request and len(request['errors'] > 0) and len(request) == 1:
        return ObjectContainer(header="Error", message="There are no available items...")

    for track in request:

        if track['streamable'] == False:
            continue

        if track['title'].startswith("#"):
            AddTrack(oc, track)


    return oc


def AddTrack(oc, track):
    if track['artwork_url']:
	thumb = track['artwork_url'].replace('large', 't500x500')

    oc.add(TrackObject(
        url = track['stream_url'],
        title = track['title'],
        summary = track['description'],
        art = 'https://i1.sndcdn.com/artworks-000115981060-vjott7-t500x500.jpg',
        thumb = thumb,
        duration = int(track['duration'])
    ))
