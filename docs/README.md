# Raspberry Pi DVR

A short introduction on how to setup a DVR using Raspberry Pi 3 to watch and record free over the air HDTV.

## Initial Setup

The following rough guide applies to XBian.

### SSH

Connect:

```
ssh xbian@192.168.2.22
```

File copy *from* PI:

```
scp xbian@192.168.2.22:/home/xbian/zap2xml.tar.gz .
```

File copy *to* PI:
```
scp zap2xml.tar.gz xbian@192.168.2.22:/home/xbian/zap2xml.tar.gz
```

### Disabling WIFI power saving

```
sudo vi /etc/network/interfaces
```

Add the following line anywhere in the file:

```
wireless-power off
```

### Set proper timezone

TBD: There seems to be many possible location to set the timezone.

* SSH:

```
dpkg-reconfigure tzdata
```

* Kodi:
  * System > Config > TBD > TZ
  * System > Config > XBian > TBD > TZ

### Builds

Enable gcc, make...

```
sudo apt-get install build-essential
```

### Install perl missing libs

This is required for the EPG downloader.

```
sudo perl -MCPAN -e shell
install JSON::XS
```

### MPEG-2 License

Need to buy a license from http://www.raspberrypi.com/mpeg-2-license-key/

For my PI, the license is: ```0x16baa230```

Enable via:

```
sudo xbian-config
```

## Tvheadend

### EPG Downloader

* Copy zap2xml config to PI using scp.
* Set cron job to fetch EPG daily:

```
crontab -e

 # m  h  dom mon dow   command
   33 3  *   *   *     /home/xbian/zap2xml/runZap2Xml.sh
```

* Enable internal grabber in path:

```
cd /usr/local/bin
sudo ln -s /home/xbian/zap2xml/tv_grab_file
```

### Frontend (Kodi)

In Kodi TV interface:
* Install *Tvheadend HTSP Client*
* Config: point to localhost

### Backend (tvheadend)

#### Basic setup

* Create default user via ssh:

```
tvheadend -C
```

* Enable tvheadend services via:

```
sudo xbian-config
```

* Set proper users using the web interface: http://192.168.2.22:9981
  * Admin:
    * tvheadend
    * xxxxx
  * User:
    * <blank>
    * <blank>

* Goto Config > General > Base, set User interface level to Expert.

#### Channel setup

The following is done using the web interface: http://192.168.2.22:9981 while logged in as admin.

Goto Config > DVB Input

* Network tab: Add network *us_ATSC_center_frequencies*
* TV Adapters tab: Assign network to tuner
* Network tab: Force scan
* Muxes tab: Check scan results.
* Services tab: map all selected, map all services.

Goto Config > Channel/EPG

* EPG Grabber tab: Set EPG frequency (advanced mode)

```
# MGouin custom to run 04:00 after zap2xml
0 4 * * *
```

* EPG Grabber Modules tab: Enable Internal tv_grab_file
* EPG Grabber Channels tab: Assign channels to each EPG channel
* Channels tab: give proper channel names

### DVR Setup

Possible file naming scheme:

Refer to http://docs.tvheadend.org/webui/config_dvr/

Goto Configuration > Recording > Profile

```
$t$-e_%F$n.$x
```

### Debugging

Refer to: https://tvheadend.readthedocs.org/en/latest/Appendices/command_line_options/

Debug command:

```
tvheadend -d -u xbian -g xbian -c /home/xbian/.hts/tvheadend
```

Default command:

```
tvheadend -f -u xbian -g xbian -c /home/xbian/.hts/tvheadend
```

### General Infos

HD Recordings:
* 30 min = 4165 MB, 4 GB
* 1 h = 8330 MB, 8.1 GB

Recordings are stored in a textual DB:

```
/home/xbian/.hts/tvheadend/dvr/log
```


### Tuner Test

#### Hauppauge Xbox One

This tuner works well.  It has the same chip as the Hauppauge WinTV-HVR-955Q (refer to dmesg listing below:

```
  [35258.315869] usb 1-1.2: new high-speed USB device number 8 using dwc_otg
  [35258.406298] usb 1-1.2: New USB device found, idVendor=2040, idProduct=b123
  [35258.406312] usb 1-1.2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
  [35258.406319] usb 1-1.2: Product: Hauppauge Device
  [35258.406326] usb 1-1.2: Manufacturer: Hauppauge
  [35258.406333] usb 1-1.2: SerialNumber: 4035698510
  [35258.439050] media: Linux media interface: v0.10
  [35258.458527] Linux video capture interface: v2.00
  [35258.501645] cx231xx 1-1.2:1.1: New device Hauppauge Hauppauge Device @ 480 Mbps (2040:b123) with 7 interfaces
  [35258.502036] cx231xx 1-1.2:1.1: Identified as Hauppauge WinTV-HVR-955Q (111401) (card=21)
  [35258.502540] i2c i2c-4: Added multiplexed i2c bus 6
  [35258.502627] i2c i2c-4: Added multiplexed i2c bus 7
  [35258.627172] cx25840 3-0044: cx23102 A/V decoder found @ 0x88 (cx231xx #0-0)
  [35258.645376] cx25840 3-0044: Direct firmware load for v4l-cx231xx-avcore-01.fw failed with error -2
  [35258.645394] cx25840 3-0044: unable to open firmware v4l-cx231xx-avcore-01.fw
  [35258.701895] tveeprom 6-0050: Hauppauge model 111401, rev E3I6, serial# 4035698510
  [35258.701909] tveeprom 6-0050: MAC address is 00:0d:fe:8b:df:4e
  [35258.701916] tveeprom 6-0050: tuner model is SiLabs Si2157 (idx 186, type 4)
  [35258.701925] tveeprom 6-0050: TV standards NTSC(M) ATSC/DVB Digital (eeprom 0x88)
  [35258.701932] tveeprom 6-0050: audio processor is CX23102 (idx 47)
  [35258.701940] tveeprom 6-0050: decoder processor is CX23102 (idx 46)
  [35258.701947] tveeprom 6-0050: has no radio, has IR receiver, has no IR transmitter
  [35258.702946] cx231xx 1-1.2:1.1: v4l2 driver version 0.0.3
  [35258.754970] cx231xx 1-1.2:1.1: Unknown tuner type configuring SIF
  [35258.780088] cx231xx 1-1.2:1.1: Registered video device video0 [v4l2]
  [35258.780230] cx231xx 1-1.2:1.1: Registered VBI device vbi0
  [35258.780243] cx231xx 1-1.2:1.1: video EndPoint Addr 0x84, Alternate settings: 5
  [35258.780256] cx231xx 1-1.2:1.1: VBI EndPoint Addr 0x85, Alternate settings: 2
  [35258.780266] cx231xx 1-1.2:1.1: sliced CC EndPoint Addr 0x86, Alternate settings: 2
  [35258.780275] cx231xx 1-1.2:1.1: TS EndPoint Addr 0x81, Alternate settings: 6
  [35258.780549] usbcore: registered new interface driver cx231xx
  [35258.796429] cx231xx 1-1.2:1.1: audio EndPoint Addr 0x83, Alternate settings: 3
  [35258.796447] cx231xx 1-1.2:1.1: Cx231xx Audio Extension initialized
  [35258.896630] si2157 7-0060: Silicon Labs Si2147/2148/2157/2158 successfully attached
  [35258.896671] DVB: registering new adapter (cx231xx #0)
  [35258.896685] cx231xx 1-1.2:1.1: DVB: registering adapter 0 frontend 0 (LG Electronics LGDT3306A VSB/QAM Frontend)...
  [35258.902066] cx231xx 1-1.2:1.1: Successfully loaded cx231xx-dvb
  [35258.902086] cx231xx 1-1.2:1.1: Cx231xx dvb Extension initialized
  [35259.074624] si2157 7-0060: found a 'Silicon Labs Si2157-A30'
  [35259.123494] si2157 7-0060: firmware version: 3.0.5
  [35259.123547] cx231xx 1-1.2:1.1: DVB: adapter 0 frontend 0 frequency 0 out of range (55000000..858000000)
```

## Maintenance

### Check

```
mount
cat /etc/fstab
sudo fdisk -l
df -h
sudo btrfs-auto-snapshot list
```

Remove snapshots:

```
sudo -i
btrfs-auto-snapshot list | grep -v /@$ | grep auto-snap | xargs -L1 btrfs-auto-snapshot destroy
```

### Correction

TBD? btrfs how to check for filesystem integrity?

## References

* https://en.wikipedia.org/wiki/List_of_Canadian_television_stations#Digital
* https://en.wikipedia.org/wiki/List_of_United_States_stations_available_in_Canada
* https://en.wikipedia.org/wiki/North_American_television_frequencies#Channel_frequencies
* http://docs.tvheadend.org/before_you_begin/
* http://kodi.wiki/view/Tvheadend_PVR
* http://www.tvfool.com
* https://github.com/mathieugouin/rpiDvr
* http://www.asciidoctor.org/docs/asciidoc-syntax-quick-reference/
* https://en.wikipedia.org/wiki/User:Mgouin/Raspberry_Pi

