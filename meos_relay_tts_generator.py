#!/usr/bin/python3
# Tested with version 3.12

from __future__ import print_function
import os
import re
import xml.etree.ElementTree as Et
import pprint
import requests
import yaml

from google.cloud import texttospeech

pp = pprint.PrettyPrinter(indent=2)


def read_config(filename):
    config = None
    try:
        with open('settings.yml', 'r') as file:
            config = yaml.safe_load(file)
    except IOError:
        print("Could not open settings file: %s" % filename)
        return None
    return config


def load_meos_teams(meos_url):
    """
    Loads teams information from the MeOS Info-server
    :param meos_url:
    :return:
    """
    print("Fetching data from MeOS InfoServer")
    temp_xml_file = 'teams_tmp.xml'
    teams = None
    # creating HTTP response object from given url
    try:
        resp = requests.get(meos_url)
        # Save the XML file
        with open(temp_xml_file, 'wb') as f:
            f.write(resp.content)
    except requests.exceptions as req_exception:
        print("Error")
        print(req_exception)
        return None
    except OSError as ose:
        print("Error: {}".format(ose))
        return None
    except Exception as e:
        print("Error")
        print(e)
        return None

    try:
        tree = Et.parse(temp_xml_file)
        root = tree.getroot()
        teams = dict()
        for child in root:
            if 'id' in child.attrib:
                meos_team_id = child.attrib['id']
                for sc in child:
                    if 'bib' in sc.attrib:
                        team_id = sc.attrib['bib']
                        team_name = sc.text
                        # print(str(sc.attrib) + ' : ' + sc.text)
                        teams[meos_team_id] = {
                            'id': team_id,
                            'name': team_name
                        }

    except Et.ParseError as parsing_exception:
        print("Error")
        print(parsing_exception)
        return None
    os.remove(temp_xml_file)
    return teams


def split_words(s):
    return " ".join(re.findall(r"[A-Z]", s))


def tts_adjustments(tts_engine, number, name):
    #  We can add support for different TTS engines and languages that may need different tweaks.
    adj_text = name
    # split_repeated_capitals (Like OK, OL, SOK and so on)
    double_pattern = r'([A-Z]{2,})'
    all_doubles = re.findall(double_pattern, adj_text)
    for double in all_doubles:
        spaced = re.sub(r'([A-Z])', r'\1 ', double)
        adj_text = adj_text.replace(double, spaced, 1)

    ends_number = re.finditer(r'(\s+\d+$)', adj_text)
    if ends_number:
        # It ends with a number - do we need anything special?
        for m in ends_number:
            adj_text = adj_text.replace(m.group(1), "," + m.group(1))

        pass
    text = f"{number}, {adj_text}"

    return text


def google_tts_generator(number, read_text, output_dir):
    """
    Synthesizes speech from the input string of text.
    :param number: Team number
    :param read_text: Full text-string to read
    :param output_dir: Output directory to write synthesized speech to
    :return:
    """

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=read_text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="sv-SE",
        name="sv-SE-Standard-D",
        # name="sv-SE-Wavenet-D", Sounds better in Swedish - but costs more.
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(f"{output_dir}/{number}.mp3", "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file: {output_dir}/{number}.mp3")


def main():
    config = read_config("settings.conf")
    if config is None:
        print("No settings.conf found")
        exit(-1)

    meos_url = config['meos']['infoserver_url']
    meos_team_path = config['meos']['team_path']
    tts_output_dir = config['tts']['output_dir']
    tts_config = config['tts']['generator_config']
    tts_engine = config['tts']['engine']
    tts_language = config['tts']['language']
    tts_enabled = bool(config['tts']['enabled'])

    print("Generating TTS config")
    if os.path.isfile(tts_config):
        print("TTS config already exists - delete if you want a new one generated: %s" % tts_config)
        print("Can also be modified manually to get better speach for some teams")
        print("Continuing as we use that file for generating the TTS files - so there might be more to do..")
    else:
        teams = load_meos_teams(meos_url+meos_team_path)
        if teams:
            # pprint.pprint(teams)
            tts_data = dict()
            for tm in sorted(teams):
                team = teams[tm]
                tts_team = {
                    'id': team['id'],
                    'name': team['name'],
                    'language': tts_language,
                    'tts': tts_adjustments(tts_engine, team['id'], team['name'])
                }
                tts_data[team['id']] = tts_team

            # Store to yaml file
            # pp.pprint(tts_data)
            with open(tts_config, 'w') as outfile:
                yaml.dump(tts_data, outfile, default_flow_style=False, allow_unicode=True)
            print("TTS config generated and stored in %s" % tts_config)

    if tts_enabled:
        if not os.path.isdir(tts_output_dir):
            print("Error:")
            print("Output directory for TTS files doesn't exist, create it or update the config and try again.")
            exit(-1)

        stats_exists = list()
        stats_generated = list()
        # stats_to_delete = list()
        # We will only generate files that do not already exist.
        # This can be used to re-generate specific files that didn't sound good.
        # All is based on the tts config-file.
        with open(tts_config, 'r') as file:
            tts_gen = yaml.safe_load(file)

            # pp.pprint(tts_gen)
            for team_id in tts_gen:
                if os.path.isfile(f"{tts_output_dir}/{team_id}.mp3"):
                    # File already exists.
                    stats_exists.append(team_id)
                else:
                    google_tts_generator(team_id, tts_gen[team_id]['tts'], tts_output_dir)
                    stats_generated.append(team_id)

        print("TTS files generated: %s" % stats_generated)
        print("TTS files that already existed: %s" % stats_exists)
    else:
        print("TTS is not enabled - see config file.")

    print("Done")


if __name__ == '__main__':
    main()
