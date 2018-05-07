#! /bin/bash
################################################################################
# When changing tvheadend channel icons, it is required to clean the cache to
# force Kodi to reload the new icons.
################################################################################

rm $HOME/.kodi/userdata/Thumbnails/*/*.png
rm $HOME/.kodi/userdata/Database/Textures13.db

echo Don\'t forget to reboot:
echo sudo reboot
