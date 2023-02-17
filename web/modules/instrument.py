import guitarpro
from time import sleep, time_ns
import paho.mqtt.client as mqtt


def get_song(fn, start=time_ns()):
    song = guitarpro.parse(fn, encoding='cp1250')

    data = {}
    data['artist'] = song.artist
    data['title'] = song.title
    data['tempo'] = song.tempo
    data['start'] = start + 5 * 1000 * 1000 * 1000
    data['b'] = []

    beat_counter = 0
    for track in song.tracks:
        for measure in track.measures:
            for voice in measure.voices:
                for beat in voice.beats:
                    b = {}
                    b['d'] = beat.duration.value
                    if beat.duration.isDotted:
                        b['d'] = beat.duration.value * 2.0 / 3.0
                    b['n'] = []

                    if beat.status == guitarpro.BeatStatus.empty:
                        b['s'] = "e"
                    elif beat.status == guitarpro.BeatStatus.normal:
                        b['s'] = "n"
                    elif beat.status == guitarpro.BeatStatus.rest:
                        b['s'] = "r"

                    for note in beat.notes:
                        b['n'].append({'s': note.string, 'f': note.value})
                        if note.type == guitarpro.NoteType.tie:
                            b['s'] = 'r'

                    data['b'].append(b)

                    # if beat.status == guitarpro.BeatStatus.normal:
                    #     beat_counter += 1
                    #     # limit to max_beats
                    #     if beat_counter > max_beats:
                    #         return data

    # with open('/tmp/data.json', 'w') as outfile:
    #     json.dump(data, outfile)

    return data


