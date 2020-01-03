#!/bin/bash
set -evx

mkdir ~/.dashcore

# safety check
if [ ! -f ~/.merakicore/.meraki.conf ]; then
  cp share/meraki.conf.example ~/.merakicore/meraki.conf
fi
