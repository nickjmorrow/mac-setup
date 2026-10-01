#!/usr/bin/env zsh
# Keep this Mac's secrets in ~/Sync/secrets (Sync.com, end-to-end encrypted) so a dead Mac loses nothing.
# What to manage is listed in ~/Sync/secrets/manifest.tsv, which stays private:
#   link <TAB> ~/usual/path <TAB> path/inside/secrets   the file lives in Sync; the usual path is a symlink to it
#   copy <TAB> ~/usual/path <TAB> path/inside/secrets   kept in both places (for files like SSH keys)
# Safe to re-run. For each entry:
#   - already in place               → ok
#   - only on this Mac               → moved (or copied) into Sync, then linked   (first run on a Mac)
#   - only in Sync                   → linked (or copied) into place              (restoring onto a new Mac)
#   - in both, different             → left alone and reported; sort it out by hand
set -euo pipefail
SECRETS=~/Sync/secrets
MANIFEST=$SECRETS/manifest.tsv

[[ -f $MANIFEST ]] || { print "$MANIFEST is missing: sign in to Sync.com and let it finish syncing."; exit 1 }
chmod 700 $SECRETS

lock() { chmod -R go-rwx "$1" }

while IFS=$'\t' read -r kind here rel; do
  [[ -z $kind || $kind == \#* ]] && continue
  here=${here/#\~/$HOME}
  there=$SECRETS/$rel
  case $kind in
    link)
      if [[ -L $here && $(readlink $here) == $there ]]; then
        print "ok       $here"
      elif [[ -e $here && ! -L $here && ! -e $there ]]; then
        mkdir -p ${there:h} && mv $here $there && lock $there && ln -s $there $here
        print "moved    $here"
      elif [[ ! -e $here && ! -L $here && -e $there ]]; then
        [[ -d ${here:h} ]] || { print "skipped  $here (no ${here:h} on this Mac)"; continue }
        ln -s $there $here
        print "linked   $here"
      elif [[ ! -e $here && ! -e $there ]]; then
        print "absent   $here"
      else
        print "CONFLICT $here exists here and in $there; fix by hand"
      fi ;;
    copy)
      if [[ -f $here && -f $there ]] && cmp -s $here $there; then
        print "ok       $here (copy)"
      elif [[ -f $here && ! -e $there ]]; then
        mkdir -p ${there:h} && cp -p $here $there && lock $there
        print "copied   $here → Sync"
      elif [[ ! -e $here && -f $there ]]; then
        mkdir -p ${here:h} && chmod 700 ${here:h} && cp -p $there $here && chmod 600 $here
        print "restored $here"
      elif [[ -f $here && -f $there ]]; then
        print "CONFLICT $here differs from $there; fix by hand"
      else
        print "absent   $here"
      fi ;;
    *) print "unknown kind '$kind' in $MANIFEST" ;;
  esac
done < $MANIFEST
lock $SECRETS
