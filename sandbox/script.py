import os
import time
import subprocess

from PIL import Image, ImageFilter

TARGET_FILE = 'test1.jpg'

#####
filename, extension = os.path.splitext(TARGET_FILE)

im = Image.open(TARGET_FILE)
sourceW = im.size[0]
sourceH = im.size[1]

print(im.size)

target = 1280
targetName = filename + '-' + str(target) + 'px' + extension
print(targetName)
ratio = sourceW / target

print(ratio)

outW = target
outH = round( sourceH / ratio )
outDimen = ( outW, outH )

print(outDimen)

start = time.time()

out = im.resize( outDimen, resample=Image.LANCZOS )
out.save(targetName, optimize=True)

end = time.time()
print( 'Resize:', round(end - start, 6), 'seconds' )

###
print( 'ImageOptim...')

print("Compress " + targetName + " ...")
print("/Applications/ImageOptim.app/Contents/MacOS/ImageOptim " + targetName)
subprocess.check_call('/Applications/ImageOptim.app/Contents/MacOS/ImageOptim ' + targetName, shell=True)
print("Compressed!")
