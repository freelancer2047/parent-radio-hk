#!/usr/bin/env python3

from flask import Flask, request
import azure.cognitiveservices.speech as speechsdk
import os
import threading
import time
import queue

class AzureSpeechSynthesizer:

    def __init__(self, key, region):
        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        self.speech_config.speech_synthesis_language = "zh-HK"

    def synthesize(self, text):
        filename = "/opt/parent-radio-hk/queue/%d.mp3" % int(time.time())
        audio_output = speechsdk.audio.AudioOutputConfig(filename=filename + ".part")
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_output)
        result = speech_synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            os.rename(filename + ".part", filename)
            print("Speech synthesized to file %s" % filename)
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
            print("Did you update the subscription info?")

speech_synthesizer = AzureSpeechSynthesizer(key=os.environ['AZURE_KEY'], region=os.environ['AZURE_REGION'])
message_queue = queue.Queue()
app = Flask(__name__)

def synthesizer_loop():
    while True:
        message = message_queue.get()
        if message is None:
            break
        print('Synthesizing: %s' % message)
        speech_synthesizer.synthesize(message)
        message_queue.task_done()

@app.route('/messages', methods=['POST'])
def postMessage():
    message = request.get_json(force=True)['text']
    message_queue.put(message)
    return "Message added"

if __name__ == '__main__':
    thread = threading.Thread(target=synthesizer_loop)
    thread.start()
    app.run()
