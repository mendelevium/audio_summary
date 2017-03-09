# Audio Summary: a podcast summarizer

This is a simple proof of concept hacked together in a day. The goal was to generate a short audio file containing the most important sentences from a larger audio segment.

## General idea:

* Split the audio in sentences base on silences
* Use CMUSphinx or another SpeechToText service to get the transcripts
* Apply a text summarizer to the transcripts
* Stitch together the audio files corresponding to the summary

The error rate of Sphinx is quite bad (45%) but since the original audio is used (and not the text) there is not need for a perfect transcription. To increase the quality of transcripts, use Google Cloud Speech API (model with the lowest error rate available). This might also produce a better summary for more technical conversations since Sphinx is only reliable for simple and frequent words.

## Prerequisite:

```python
	pip install pydub
	pip install sphinxpocket
	pip install sumy
```

	