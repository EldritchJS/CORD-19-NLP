import sys
import wget

if len(sys.argv) == 3:
    url = sys.argv[1]
    destination = sys.argv[2]
    wget.download(url, destination)
else:
    print('Usage: ' + sys.argv[0] + ' <SOURCE_URL> <DESTINATION_PATH>')
