#/bin/dash

fatal() {
  echo "$1"
  exit 1
}

warn() {
  echo "$1"
}

# Find a source mirror near you which supports rsync on
# https://launchpad.net/ubuntu/+archivemirrors
# rsync://<iso-country-code>.rsync.archive.ubuntu.com/ubuntu should always work
export RSYNC_CONNECT_PROG='nc -x192.168.90.247:1080 %H 873'
RSYNCSOURCE=rsync://mirrors.ustc.edu.cn/ubuntu/

# Define where you want the mirror-data to be on your mirror
BASEDIR=`pwd`

if [ ! -d ${BASEDIR} ]; then
  warn "${BASEDIR} does not exist yet, trying to create it..."
  mkdir -p ${BASEDIR} || fatal "Creation of ${BASEDIR} failed."
fi

#  --bwlimit=6120 \
rsync --recursive --times --links --hard-links \
  --log-file=/tmp/rsync_log.txt \
  --stats \
  --exclude "Packages*" --exclude "Sources*" \
  --exclude "Release*" \
  --exclude "openoffice.org-l10n*" \
        --exclude="calligra*" \
        --exclude="vtk*" \
        --exclude="wesnoth*" \
        --exclude="virtualbox*" \
        --exclude="vegastrike*" \
        --exclude="triplea*" \
        --exclude="supertuxkart*" \
        --exclude="chromium*" \
        --exclude="eclipse*" \
        --exclude="spring*" \
        --exclude="*libreoffice*" \
        --exclude="*koffice*" \
        --exclude="thunderbird*" \
        --exclude="*i386*" \
        --exclude="linux-ec2*" \
        --exclude="*kde*" \
        --exclude="*gnome*" \
        --exclude="*firefox*" \
        --exclude="*hardy*" \
        --exclude="hardy-backports*" \
        --exclude="hardy-proposed*" \
        --exclude="hardy-security*" \
        --exclude="hardy-updates*" \
        --exclude="*lucid*" \
        --exclude="lucid-backports*" \
        --exclude="lucid-proposed*" \
        --exclude="lucid-security*" \
        --exclude="lucid-updates*" \
        --exclude="*natty*" \
        --exclude="natty-backports*" \
        --exclude="natty-proposed*" \
        --exclude="natty-security*" \
        --exclude="natty-updates*" \
        --exclude="*oneiric*" \
        --exclude="oneiric-backports*" \
        --exclude="oneiric-proposed*" \
        --exclude="oneiric-security*" \
        --exclude="oneiric-updates*" \
        --exclude="*quantal*" \
        --exclude="quantal-backports*" \
        --exclude="quantal-proposed*" \
        --exclude="quantal-security*" \
        --exclude="quantal-updates*" \
        --exclude="*raring*" \
        --exclude="raring-backports*" \
        --exclude="raring-proposed*" \
        --exclude="raring-security*" \
        --exclude="raring-updates*" \
  ${RSYNCSOURCE} ${BASEDIR} || fatal "First stage of sync failed."

rsync --recursive --times --links --hard-links \
  --log-file=/tmp/rsync_log.txt \
  --stats --delete --delete-after \
  ${RSYNCSOURCE} ${BASEDIR} || fatal "Second stage of sync failed."

date -u > ${BASEDIR}/project/trace/$(hostname -f)
