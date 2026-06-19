# High-quality Microsoft Edge English neural narrators
edge_tts_narrators = {
    "en-US-GuyNeural",
    "en-US-AriaNeural",
    "en-US-JennyNeural",
    "en-US-ChristopherNeural",
    "en-GB-RyanNeural",
    "en-GB-SoniaNeural",
    "en-AU-NatashaNeural",
    "en-AU-WilliamNeural",
    "en-CA-ClaraNeural",
    "en-CA-LiamNeural",
    "en-IN-NeerjaNeural",
    "en-IN-PrabhatNeural"
}

# Standard, WaveNet, and Neural2 English voice codes for programmatic narration
google_tts_narrators = {
    "en-US-Neural2-A", "en-US-Neural2-C", "en-US-Neural2-D", "en-US-Neural2-F",
    "en-US-WaveNet-A", "en-US-WaveNet-B", "en-US-WaveNet-C", "en-US-WaveNet-D",
    "en-GB-Neural2-B", "en-GB-Neural2-C", "en-GB-Wavenet-A", "en-GB-Wavenet-B",
    "en-AU-Neural2-A", "en-AU-WaveNet-A", "en-IN-Neural2-A", "en-IN-WaveNet-A"
}

# Note: You can fetch the live list dynamically using the google-cloud-texttospeech library:
# client = texttospeech.TextToSpeechClient()
# voices = client.list_voices(language_code="en")