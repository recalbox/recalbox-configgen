#!/usr/bin/env python

esInputs = '/root/.emulationstation/es_input.cfg'
esSettings = '/root/.emulationstation/es_settings.cfg'
recalboxConf = '/recalbox/share/system/recalbox.conf'

retroarchRoot = '/recalbox/configs/retroarch'
retroarchCustom = retroarchRoot + '/retroarchcustom.cfg'
retroarchCustomOrigin = retroarchRoot + "/retroarchcustom.cfg.origin"
retroarchCoreCustom = retroarchRoot + "/cores/retroarch-core-options.cfg"

retroarchBin = "retroarch"
retroarchCores = "/usr/lib/libretro/"
shadersRoot = "/recalbox/share/shaders/presets/"
shadersExt = '.gplsp'
libretroExt = '_libretro.so'

fbaRoot = '/recalbox/configs/fba/'
fbaCustom = fbaRoot + 'fba2x.cfg'
fbaCustomOrigin = fbaRoot + 'fba2x.cfg.origin'
fba2xBin = '/usr/bin/fba2x'

mupenCustom = "/recalbox/configs/mupen64/mupen64plus.cfg"

shaderPresetRoot = "/recalbox/configs/shadersets/"

kodiJoystick = '/root/.kodi/userdata/keymaps/recalbox.xml'
kodiMapping  = '/recalbox/configs/kodi/input.xml'

kodiBin  = '/usr/lib/kodi/kodi.bin'
