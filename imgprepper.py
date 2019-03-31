import os
import time
import subprocess
import argparse

from PIL import Image
import yaml


class ImageObject:

    def __init__(self, filepath):
        # Check if the file exists
        if os.path.isfile(filepath):
            self.srcFilepath = filepath
        else:
            raise OSError('File does not exist:', filepath)

        # Split its directory, name and extension for us to work with
        self.srcDirectory, self.srcFilename = os.path.split(filepath)
        self.srcName, self.srcExt = os.path.splitext(self.srcFilename)
        # Trim off the "."
        self.srcExt = self.srcExt[1:]

        # Open an Image object
        self.PillowImage = Image.open(self.srcFilepath)

        # Get parameters
        self.srcSize = self.PillowImage.size


class Process:

    def __init__(self, object):
        self.i = object

    def resize(self, desiredW, targetName):
        sourceW, sourceH = self.i.srcSize

        ratio = sourceW / desiredW

        outW = desiredW
        outH = round( sourceH / ratio )
        outDimen = ( outW, outH )

        start = time.time()

        out = self.i.PillowImage.resize( outDimen, resample=Image.LANCZOS )
        out.save(targetName, optimize=True)

        end = time.time()

        info = {
            'filepath': targetName,
            'time': end - start,
            'outW': outW,
            'outH': outH
        }

        return info


class ImageOptim:

    def run(path):
        cmd = 'imageoptim ' + path
        print('COMMAND:', cmd)
        subprocess.run(cmd, shell=True)


#######

parser = argparse.ArgumentParser()
parser.add_argument( "PRESETS_PATH", help="path to a YAML file with your presets", type=str)
args = parser.parse_args()


if args.PRESETS_PATH:
    pass
else:
    raise Exception('Run the script again, including the path to your YAML file containing presets')

if os.path.isfile(args.PRESETS_PATH):
    presets_file = open(args.PRESETS_PATH, 'r')
else:
    raise FileNotFoundError('Could not find this file). Check the path for typos?\n' + args.PRESETS_PATH)

presets_data = yaml.safe_load(presets_file)

TARGET_PRESETS = presets_data['presets']
SOURCE_FILES = presets_data['file_paths'].strip().splitlines()

#######

objects = [ ImageObject(f) for f in SOURCE_FILES ]


def createDirectories():
    # Create directories, so there are no missing directory errors thrown
    directories = { preset['directory'] for preset in TARGET_PRESETS }
    for dir in directories:
        if not os.path.isdir(dir):
            os.makedirs(dir)
    return directories


def processPresets():
    TOTAL_FILE_LIST = set()
    for preset in TARGET_PRESETS:
        # Treat each preset as a group

        print('Directory out:', preset['directory'])

        for sourceImg in objects:
            # And then process all images per that preset
            process = Process(sourceImg)
            outFilename = preset['nameFormat'].format(name=sourceImg.srcName, ext=sourceImg.srcExt)
            outPath = os.path.join( preset['directory'], outFilename)

            if preset['action'] == 'resize':
                resize = process.resize( preset['width'], outPath )
                print(
                    '    ' + outFilename,
                    '| Dimensions: {} x {}'.format( resize['outW'], resize['outH'] ),
                    '| Resize:',
                    round(resize['time'], 3),
                    's'
                )
                TOTAL_FILE_LIST.add(resize['filepath'])
            else:
                raise Exception('Preset action needs to be set. At the moment, I only accept `resize`.')
    return TOTAL_FILE_LIST


def imageOptimDirectories(directories):
    # ImageOptim all the directories listed in the presets
    all_paths = ' '.join( '"{}"'.format(dir) for dir in directories )
    ImageOptim.run(all_paths)


def imageOptimFiles(fileList):
    # ImageOptim all the individual paths, separated by space
    all_paths = ' '.join( '"{}"'.format(f) for f in fileList )
    ImageOptim.run(all_paths)


#####

directories = createDirectories()
TOTAL_FILE_LIST = processPresets()

# imageOptimDirectories(directories)
imageOptimFiles(TOTAL_FILE_LIST)
