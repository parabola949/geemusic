from flask_ask import statement, audio
from os import environ
from geemusic import ask, queue, app
from geemusic.utils.music import GMusicWrapper

##
# Callbacks
#
@ask.on_playback_stopped()
def stopped(offset):
    queue.paused_offset = offset
    app.logger.debug("Stopped at %s" % offset)

@ask.on_playback_started()
def started(offset):
    app.logger.debug("Started at %s" % offset)

@ask.on_playback_nearly_finished()
def nearly_finished():
    next_id = queue.up_next()

    if next_id != None:
        api = GMusicWrapper(environ['GOOGLE_EMAIL'], environ['GOOGLE_PASSWORD'])
        stream_url = api.get_stream_url(next_id)

        return audio().enqueue(stream_url)

@ask.on_playback_finished()
def nearly_finished():
    next_id = queue.next()

    if next_id != None:
        api = GMusicWrapper(environ['GOOGLE_EMAIL'], environ['GOOGLE_PASSWORD'])
        stream_url = api.get_stream_url(next_id)

        return audio().play(stream_url)

##
# Intents
#
@ask.intent('AMAZON.StartOverIntent')
def resume():
    next_id = queue.current()

    app.logger.debug('Queue status: %s', queue)
    if next_id == None:
        return audio("There are no songs on the queue")
    else:
        api = GMusicWrapper(environ['GOOGLE_EMAIL'], environ['GOOGLE_PASSWORD'])
        stream_url = api.get_stream_url(next_id)

        return audio().enqueue(stream_url)

@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming').resume()

@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Pausing').stop()

@ask.intent('AMAZON.StopIntent')
def stop():
    queue.reset()
    return audio('Stopping').stop()

@ask.intent('AMAZON.NextIntent')
def next_song():
    next_id = queue.next()

    if next_id == None:
        return audio("There are no more songs on the queue")
    else:
        api = GMusicWrapper(environ['GOOGLE_EMAIL'], environ['GOOGLE_PASSWORD'])
        stream_url = api.get_stream_url(next_id)

        return audio().play(stream_url)

@ask.intent('AMAZON.PreviousIntent')
def prev_song():
    prev_id = queue.prev()

    if prev_id == None:
        return audio("You can't go back any farther in the queue")
    else:
        api = GMusicWrapper(environ['GOOGLE_EMAIL'], environ['GOOGLE_PASSWORD'])
        stream_url = api.get_stream_url(prev_id)

        return audio().play(stream_url)