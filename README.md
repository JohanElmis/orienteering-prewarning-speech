# orienteering-prewarning-speech

This is a small tool to generate pre-warning speech-files using TTS.

When hosting orienteering events - especially relays, it's very useful to get an announcement
that your team is about to come in for the switch - so the next runner can get ready.

The pre-warning feature is built in to several tools - where support for playing files exists in some tools as well.

We are currently using MeOS, so this is what I use to pull out info here.
You can put the files in a directory for MeOS to read them - or use 


# Setup environment according to Pipfile
$ pipenv install
```

If you have `pyenv` installed and configured, Pipenv will automatically ask you if you want to install a required version of Python if you don’t already have it available.

## Run the Python env

commands:

```shell
# Enter the environment
$ pipenv shell

# Exit the environment
() $ exit

$
```

https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python
