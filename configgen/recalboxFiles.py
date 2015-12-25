#!/usr/bin/env python

esInputs = '/recalbox/share/system/.emulationstation/es_input.cfg'
esSettings = '/recalbox/share/system/.emulationstation/es_settings.cfg'
recalboxConf = '/recalbox/share/system/recalbox.conf'

retroarchRoot = '/recalbox/share/system/configs/retroarch'
retroarchCustom = retroarchRoot + '/retroarchcustom.cfg'
retroarchCustomOrigin = retroarchRoot + "/retroarchcustom.cfg.origin"
retroarchCoreCustom = retroarchRoot + "/cores/retroarch-core-options.cfg"

retroarchBin = "retroarch"
retroarchCores = "/usr/lib/libretro/"
shadersRoot = "/recalbox/share/shaders/presets/"
shadersExt = '.gplsp'
libretroExt = '_libretro.so'

fbaRoot = '/recalbox/share/system/configs/fba/'
fbaCustom = fbaRoot + 'fba2x.cfg'
fbaCustomOrigin = fbaRoot + 'fba2x.cfg.origin'
fba2xBin = '/usr/bin/fba2x'

mupenCustom = "/recalbox/share/system/configs/mupen64/mupen64plus.cfg"

shaderPresetRoot = "/recalbox/share/system/configs/shadersets/"

kodiJoystick = '/recalbox/share/system/.kodi/userdata/keymaps/recalbox.xml'
kodiMapping  = '/recalbox/share/system/configs/kodi/input.xml'

kodiBin  = '/recalbox/scripts/kodilauncher.sh'

moonlightBin = '/usr/bin/moonlight'
moonlightCustom = '/recalbox/share/config/moonlight'
moonlightConfig = moonlightCustom + '/moonlight.conf'
moonlightGamelist = moonlightCustom + '/gamelist.txt'
moonlightMapping = dict()
moonlightMapping[1] = moonlightCustom + '/mappingP1.conf'
moonlightMapping[2] = moonlightCustom + '/mappingP2.conf'
moonlightMapping[3] = moonlightCustom + '/mappingP3.conf'
moonlightMapping[4] = moonlightCustom + '/mappingP4.conf'

logdir = '/recalbox/share/system/logs/'
