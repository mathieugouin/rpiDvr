#! /bin/bash

################################################################################
# Help:
# zap2xml <zap2xml@gmail.com> (2016-01-08)
#   -u <username>
#   -p <password>
#   -d <# of days> (default = 7)
#   -n <# of no-cache days> (from end)   (default = 0)
#   -N <# of no-cache days> (from start) (default = 0)
#   -s <start day offset> (default = 0)
#   -o <output xml filename> (default = "xmltv.xml")
#   -c <cacheDirectory> (default = "cache")
#   -l <lang> (default = "en")
#   -i <iconDirectory> (default = don't download channel icons)
#   -m <#> = offset program times by # minutes (better to use TZ env var)
#   -b = retain website channel order
#   -x = output XTVD xml file format (default = XMLTV)
#   -w = wait on exit (require keypress before exiting)
#   -q = quiet (no status output)
#   -r <# of connection retries before failure> (default = 3, max 20)
#   -e = hex encode entities (html special characters like accents)
#   -E "amp apos quot lt gt" = selectively encode standard XML entities
#   -F = output channel names first (rather than "number name")
#   -O = use old tv_grab_na style channel ids (C###nnnn.zap2it.com)
#   -A "new live" = append " *" to program titles that are "new" and/or "live"
#   -M = copy movie_year to empty movie sub-title tags
#   -U = UTF-8 encoding (default = "ISO-8859-1")
#   -L = output "<live />" tag (not part of xmltv.dtd)
#   -T = don't cache files containing programs with "\bTBA\b|To Be Announced" titles
#   -P <http://proxyhost:port> = to use an http proxy
#   -C <configuration file> (default = "/home/mgouin/.zap2xmlrc")
#   -S <#seconds> = sleep between requests to prevent flooding of server
#   -D = include details = 1 extra http request per program!
#   -I = include icons (image URLs) - 1 extra http request per program!
#   -J <xmltv> = include xmltv file in output
#   -Y <lineupId> (if not using username/password)
#   -Z <zipcode> (if not using username/password)
#   -z = use tvguide.com instead of zap2it.com
#   -a = output all channels (not just favorites) on tvguide.com
#   -j = add "series" category to all non-movie programs
################################################################################

# Need to CD first...
cd "$(dirname "$0")"

#OUTPUT_LOG=runZap2Xml.log
OUTPUT_LOG=/dev/null

#OUTPUT_DEBUG_LOG=runZap2Xml.debug.log
OUTPUT_DEBUG_LOG=/dev/null

BACKUP_FOLDER=bak
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

echo "########## START ##########" >> $OUTPUT_LOG
echo $(date) >> $OUTPUT_LOG

echo "########## START ##########" >> $OUTPUT_DEBUG_LOG
echo $(date) >> $OUTPUT_DEBUG_LOG

# normal test w/ login (no icons)
# 14 days of EPG data
# 3 days of no cache data from start
# Copy movie year to subtitle
# Use UTF-8 encoding
./zap2xml.pl -u xxx@gmail.com -p xxx -d 14 -N 3 -M -U >> $OUTPUT_DEBUG_LOG 2>&1

# Correct bad encoding
./correctBadEncoding.py < xmltv.xml > xmltv.xml.new
mv -f xmltv.xml.new xmltv.xml

# Correct the bad categories
./category-update.pl < xmltv.xml > xmltv.xml.new 2>> $OUTPUT_DEBUG_LOG
mv -f xmltv.xml.new xmltv.xml

# Backup new xmltv.xml for debug purposes
cp xmltv.xml $BACKUP_FOLDER/xmltv_${TIMESTAMP}.xml

# Delete old backup files that are more than 15 days old
find ./$BACKUP_FOLDER -name "*.xml" -mtime +15 -type f -delete

echo $(date) >> $OUTPUT_LOG
echo "########## STOP ##########" >> $OUTPUT_LOG

echo $(date) >> $OUTPUT_DEBUG_LOG
echo "########## STOP ##########" >> $OUTPUT_DEBUG_LOG

