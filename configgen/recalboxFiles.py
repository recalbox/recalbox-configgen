#!/usr/bin/env python
HOME = '/recalbox/share/system'
CONF = HOME + '/configs'

esInputs = HOME + '/.emulationstation/es_input.cfg'
esSettings = HOME + '/.emulationstation/es_settings.cfg'
recalboxConf = HOME + '/recalbox.conf'

retroarchRoot = CONF + '/retroarch'
retroarchCustom = retroarchRoot + '/retroarchcustom.cfg'
retroarchCustomOrigin = retroarchRoot + "/retroarchcustom.cfg.origin"
retroarchCoreCustom = retroarchRoot + "/cores/retroarch-core-options.cfg"

retroarchBin = "retroarch"
retroarchCores = "/usr/lib/libretro/"
shadersRoot = "/recalbox/share/shaders/presets/"
shadersExt = '.gplsp'
libretroExt = '_libretro.so'

fbaRoot = CONF + '/fba/'
fbaCustom = fbaRoot + 'fba2x.cfg'
fbaCustomOrigin = fbaRoot + 'fba2x.cfg.origin'
fba2xBin = '/usr/bin/fba2x'

mupenConf = CONF + '/mupen'
mupenCustom = mupenConf + "/mupen64plus.cfg"
mupenInput = mupenConf + "InputAutoCfg.ini"

shaderPresetRoot = "/recalbox/share/system/configs/shadersets/"

kodiJoystick = HOME + '/.kodi/userdata/keymaps/recalbox.xml'
kodiMapping  = CONF + '/kodi/input.xml'

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

logdir = HOME + '/logs/'
#!/usr/bin/env python

esInputs = HOME + '/.emulationstation/es_input.cfg'
esSettings = HOME + '/.emulationstation/es_settings.cfg'
recalboxConf = HOME + '/recalbox.conf'

retroarchRoot = CONF + '/retroarch'
retroarchCustom = retroarchRoot + '/retroarchcustom.cfg'
retroarchCustomOrigin = retroarchRoot + "/retroarchcustom.cfg.origin"
retroarchCoreCustom = retroarchRoot + "/cores/retroarch-core-options.cfg"

retroarchBin = "retroarch"
retroarchCores = "/usr/lib/libretro/"
shadersRoot = "/recalbox/share/shaders/presets/"
shadersExt = '.gplsp'
libretroExt = '_libretro.so'

fbaRoot = CONF + '/fba/'
fbaCustom = fbaRoot + 'fba2x.cfg'
fbaCustomOrigin = fbaRoot + 'fba2x.cfg.origin'
fba2xBin = '/usr/bin/fba2x'

mupenConf = CONF + '/mupen64'
mupenCustom = mupenConf + '/mupen64plus.cfg'
mupenInput = mupenConf + '/InputAutoCfg.ini'

shaderPresetRoot = "/recalbox/share/system/configs/shadersets/"

kodiJoystick = HOME + '/.kodi/userdata/keymaps/recalbox.xml'
kodiMapping  = CONF + '/kodi/input.xml'

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

logdir = HOME + '/logs/'
