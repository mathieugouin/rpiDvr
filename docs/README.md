# Overview

A semi-detailed guide on how to setup a DVR using Raspberry Pi 3 to watch and record free over the air HDTV.

These instructions will allow 2 simultaneous programme recording while watching another already recorder programme.

It aims at providing and addressing the following:
* ATSC Signal: Outdoor/indoor antenna
* Decoding of the signal: USB ATSC TV Tuner
* Channel guide: third party source from <https://tvlistings.zap2it.com> & download script
* Recordings management & scheduling: <https://tvheadend.org/>
* Recordings playing: Kodi + XBian + Tvheadend HTSP Client
* Recordings storage: high capacity external USB hard drive

## Bill of Material

* Raspberry Pi 3 kit
* 2 TB (or more) USB external hard drive
* ATSC USB Tuners:
  * 2 Digital TV Tuner for Xbox One (1 is enough if dual recording is not a must)
  * (alternate option) Hauppauge 1595 WinTV-DualHD
* Raspberry MPEG-2 License (to enable HW decoding of ATSC Streams when playing back)
* Coax cable splitter (not required if dual recording is not a must)
* MicroSD card
* MicroSD card USB reader

# LibreELEC Install

Download from <https://libreelec.tv/>

The version that was causing less issue is 9.2.1 for my Raspberry Pi 3.  <http://archive.libreelec.tv/LibreELEC-RPi2.arm-9.2.1.img.gz>

Extract downloaded file and unzip it.

Plug micro sd card in PC.

Check where mounted: `lsblk`

Unmount card partition (if mounted): `sudo umount /dev/sdx#`

Write to micro sd card:
```bash
sudo dd if=XXX.img of=/dev/sdx bs=4M conv=fsync status=progress
sync
```

* Plug sdcard on the PI
* Boot PI
* Wait for full initial setup, including partition resize
* Follow wizzard to setup Wifi, etc...
* Disable auto update:
  * Settings
  * LibreELEC
  * Updates
  * Change "Automatic Updates" to "manual"
* Set proper timezone:
  * Settings
  * Interface
  * Regional
  * Timezone country


## MPEG-2 License
Need to buy a license from <http://www.raspberrypi.com/mpeg-2-license-key/>

For my PI, the license is: `0x16baa230`

Enable the license by sshing on the PI:
* `ssh root@192.168.1.23`
* The default password is `libreelec` all lowercase.
* In the SSH session mount the /flash directory with read and write privileges:
  * `mount -o remount,rw /flash`
* Edit the /flash/config.txt file to add the MPEG-2 license key:
  * nano /flash/config.txt
  * Locate the `decode_MPG2` line, remove the # and space at the front, and add your MPEG-2 license key, ex: `decode_MPG2=0x16baa230`

# Tvheadend

## Backend (tvheadend)

Install the *Tvheadend Server* add-on from the "Service" category in the add-ons repos.

Configure the addon to have a delayed startup of 20 seconds.  This is to make sure that the externally mounted drive are available when tvheadend starts:
* My Addons
* Tvheadend Server
* Configure
* DVB section
* Delay Start of tvheadend: active
* Seconds delay: 20

The rest of the tvheadend configuration is done from its web interface: `http://ip:9981` (mine is: <http://192.168.1.23:9981>)

Goto Configuration > General > Base:
* Set User interface level to Expert
* Picon section:
  * Uncheck prefer picon
  * Set channel icon path: `https://raw.githubusercontent.com/mathieugouin/rpiDvr/master/zap2xml/iconsMan/%C.png`
  * Channel icon name scheme: "All lower case"

Goto Configuration > General > User:
* Set proper users login (as required).
  * Admin:
    * `tvheadend`
    * `xxxxx`
  * User:
    * `*`
    * `<blank>`

### DVR Setup

The following is done using tvheadend web interface.

Refer to <http://docs.tvheadend.org/webui/config_dvr/>

Goto Configuration > Recording > Digital Video Recorder Profiles:
* Select the <Default profile)
* In the Parameters right section:
  * DVR file retention period: Forever
  * Recording system path: `/storage/DVR/recordings`
  * Format string: `$t$-e_%F$n.$x`

### Channel setup

The following is done using tvheadend web interface.

Goto Configuration > DVB Input:
* Network tab: Add network
  * type = ATSC-T
  * Name = ATSC-T
  * Predefined muxes: United States: us-ATSC-center-frequencies-8VSB-062009
* TV Adapters tab:
  * Enable only the ATSC-T sub tuner
  * Assign network to tuner for ATSC-T (for terrestial)
* Network tab: Select ATSC-T, then click Force scan
* Muxes tab:
  * Check scan results.
  * For frequency 575.028 (ICI Television), enable:
    * Accept zero value for TSID
    * EIT - skip TSID check
* Services tab: map all selected, map all services.

Goto Configuration > Channel/EPG
* Channel Tags tab (optional): create the following tags to help when searching:
  * French
  * English
  * Canada
  * USA
  * En-Can
* Channels tab:
  * Adjust channel name & number, ex: CBC, 6.1
  * Make sure user icon is set properly (use reset icon + save).
  * Manually add channel and map to services if not all services were correctly mapped.  Refer to <https://en.wikipedia.org/wiki/List_of_Canadian_television_stations#Digital> and <https://en.wikipedia.org/wiki/North_American_television_frequencies#Channel_frequencies> to find the corresponding frequency for each channel.


### EPG Downloader

These steps explains how to install an addon that will download the updated EPG (Electronic Program Guide) every night and make it available for tvheadend.

Download the addon *script.module.zap2epg* from <https://github.com/mathieugouin/script.module.zap2epg>

Direct download link <https://github.com/mathieugouin/script.module.zap2epg/releases/download/v1.3.3/script.module.zap2epg-1.3.3.zip>

Copy the file on the PI.

Install the addon.

Configure the Addon as follows
* Option section:
  * Nb days download: 14
  * Nb days delete cache: 3
* Location section:
  * ZIP Code: J3B2X8
  * Lineup: local over the air

The following is done using tvheadend web interface.

Goto Configuration > Channel/EPG:
* EPG Grabber Modules tab: Enable only "Internal: XMLTV: tv_grab_zap2epg"
* EPG Grabber tab:
  * General configuration: enable save to disk after import
  * Internal grabber: Set EPG frequency (Expert mode) for Internal grabber `0 4 * * *`
* EPG Grabber Channels tab: Assign channels to each EPG channel

## Frontend (Kodi)
In Kodi TV interface:
* Install/Enable PVR addon: *Tvheadend HTSP Client*
* Config: point to localhost

# Miscelaneous

## Clear Icons Cache

When changing tvheadend channel icons, it is required to clear the cache to force Kodi to reload the new icons
```bash
rm $HOME/.kodi/userdata/Thumbnails/*/*.png
rm $HOME/.kodi/userdata/Database/Textures13.db
sudo reboot
```

## Enable debug log
If required to help debugging an issue with kodi, activate debug logging without the annying onscreen debug overlay as follows:
* Connect through ssh on the PI: `ssh root@192.168.1.23`
* If not already present, create the following text file: `/storage/.kodi/userdata/advancedsettings.xml`
* Edit to contains:

```xml
<advancedsettings version="1.0">
    <!-- That should enable debug logging but without that annoying overlay on the screen. -->
    <loglevel>1</loglevel>
</advancedsettings>
```

# References

**SSH**

Connect: `ssh root@192.168.1.23`

File copy *from* PI: `scp root@192.168.1.23:/home/xbian/zap2xml.tar.gz .`

File copy *to* PI: `scp file.tar.gz root@192.168.1.23:/path/to/copy/file.tar.gz`

* <https://en.wikipedia.org/wiki/List_of_Canadian_television_stations#Digital>
* <https://en.wikipedia.org/wiki/North_American_television_frequencies#Channel_frequencies>
* <https://en.wikipedia.org/wiki/List_of_United_States_stations_available_in_Canada>
* <http://docs.tvheadend.org/before_you_begin/>
* <http://kodi.wiki/view/Tvheadend_PVR>
* <http://wiki.xbian.org/doku.php/snapshots>
* <http://www.tvfool.com>
* <https://www.satlogo.com/tvcountry/ca_1.html>
* <https://en.wikipedia.org/wiki/User:Mgouin/Raspberry_Pi>
* <https://linuxtv.org/downloads/firmware/>
* <https://www.linuxtv.org/wiki/index.php/Hauppauge_WinTV-HVR-955Q>
* <http://zap2xml.awardspace.info/>
* <https://mathieugouin.github.io/rpiDvr>
