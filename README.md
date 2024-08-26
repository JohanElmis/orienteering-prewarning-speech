# orienteering-prewarning-speech

This is a small tool to generate pre-warning speech-files using TTS.

When hosting orienteering events - especially relays, it's very useful to get an announcement<BR>
that your team is about to come in for the switch - so the next runner can get ready.

## Purpose
The pre-warning feature is built in to several tools already - where support for playing files exists in some tools as well.<BR>
Recording files manually - works - but it snot really flexible and time consuming.<BR>
TTS Text-To-Speech has come a long way today - so why not generate the voice-announcements automatically?

This is what this program focuses on.

### MeOS
We are currently using MeOS, so this is what I use to pull out info here.<BR>
In MeOS pre-warning automation you can put files in a folder that will be played. These should be WAV files.<BR>

### Incoming Orienteerer
I'm using another project that can run on almost any computer that talks to MeOS Information server.<BR>
Display through a web-browser, and plays the sound-files. Using NodeJS.<BR>

[GitHub Incoming-Orienteerer](https://github.com/qtoden/incoming-orienteerer)



There are several others as well - but many of them are outdated or was not using MeOS.<BR>
So I decided to just focus on the voice-part.


### Orienteering Event Software
* [MeOS](https://www.melin.nu/meos/sv/index.php)

* [SOFT:s tidtagningsprogram OLA](https://www.orientering.se/forening/arrangor/tavlingsadministration/ola/)


### Online Radio controls
* [Radio Online Control](https://roc.olresultat.se/ver7.3/roc.php?mainmenu=about&language=engelska)

* [WiRoc](https://wiroc.se/#wiroc)

## Installation
Check out into your local directory<BR>
It requires Python 3 (3.12)<BR>

### Google TTS
The current version is using Google TTS as that is one of few that offers a API to the service<BR>
without having to get Enterprise agreements that costs a lot of money.

You can set up the Google one for free.<br>
[Google Text-to-speech](https://cloud.google.com/text-to-speech)<BR>
Voice is OK - and gets even better with the Premium voices - (that costs a little bit more).<BR>

https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python<BR>


Setup environment according to Pipfile<br>
```$ pipenv install```

If you have `pyenv` installed and configured, Pipenv will automatically ask you if you want to<BR>
install a required version of Python if you don’t already have it available.

#### Run the Python env

commands:

```shell
# Enter the environment
$ pipenv shell

# Run the actual command - after editing the settings.yml file.
python meos_relay_tts_generator.py

# Exit the environment
$ exit

```



## Text-to-Speech engines
[Google Text-to-speech](https://cloud.google.com/text-to-speech)<BR>
This has a decent to good Swedish voice - and API's which made it very easy to use.

[Amazon](https://aws.amazon.com/polly/features/?nc=sn&loc=3)<BR>
Could have worked as well.

[TTS Maker](https://ttsmaker.com/)<BR>
I made some tests using the voice 'Swedish Rory' and liked them a lot.<BR>
The problem for me was that they didn't offer a API unless you have a subscription for at least $20/month.

[TTS Free](https://ttsfree.com/text-to-speech/swedish)<BR>
Had some quite fair voice - but required some more tweaking of the sentences to sound ok.


## Contact:
I'm part of Lunds OK (Orienteering club) in Sweden, and the Incoming-Orienteerer is developed by Björn in Malmö OK.
Please reach out if you have ideas or want to make contributions to make this more generic.

Happy Orienteering,
Johan Elmerfjord
