#!/usr/bin/env python
HOME_INIT = '/recalbox/share_init/system/'
HOME = '/recalbox/share/system'
CONF = HOME + '/configs'
SAVES = '/recalbox/share/saves'
SCREENSHOTS = '/recalbox/share/screenshots'
BIOS = '/recalbox/share/bios'
OVERLAYS = '/recalbox/share/overlays'


esInputs = HOME + '/.emulationstation/es_input.cfg'
esSettings = HOME + '/.emulationstation/es_settings.cfg'
recalboxConf = HOME + '/recalbox.conf'
logdir = HOME + '/logs/'

retroarchRoot = CONF + '/retroarch'
retroarchCustom = retroarchRoot + '/retroarchcustom.cfg'
retroarchCustomOrigin = retroarchRoot + "/retroarchcustom.cfg.origin"
retroarchCoreCustom = retroarchRoot + "/cores/retroarch-core-options.cfg"

retroarchBin = "retroarch"
retroarchCores = "/usr/lib/libretro/"
shadersRoot = "/recalbox/share/shaders/presets/"
shadersExt = '.gplsp'
libretroExt = '_libretro.so'
screenshotsDir = "/recalbox/share/screenshots/"
savesDir = "/recalbox/share/saves/"

fbaRoot = CONF + '/fba/'
fbaCustom = fbaRoot + 'fba2x.cfg'
fbaCustomOrigin = fbaRoot + 'fba2x.cfg.origin'
fba2xBin = '/usr/bin/fba2x'


mupenBin = '/usr/bin/mupen64plus'
mupenConf = CONF + '/mupen64/'
mupenCustom = mupenConf + "mupen64plus.cfg"
mupenInput = mupenConf + "InputAutoCfg.ini"
mupenSaves = SAVES + "/n64"
mupenMappingUser    = mupenConf + 'input.xml'
mupenMappingSystem  = '/recalbox/share_init/system/configs/mupen64/input.xml'

shaderPresetRoot = "/recalbox/share_init/system/configs/shadersets/"

kodiJoystick = HOME + '/.kodi/userdata/keymaps/recalbox.xml'
kodiMappingUser    = CONF + '/kodi/input.xml'
kodiMappingSystem  = '/recalbox/share_init/system/configs/kodi/input.xml'

kodiBin  = '/recalbox/scripts/kodilauncher.sh'

moonlightBin = '/usr/bin/moonlight'
moonlightCustom = CONF+'/moonlight'
moonlightConfig = moonlightCustom + '/moonlight.conf'
moonlightGamelist = moonlightCustom + '/gamelist.txt'
moonlightMapping = dict()
moonlightMapping[1] = moonlightCustom + '/mappingP1.conf'
moonlightMapping[2] = moonlightCustom + '/mappingP2.conf'
moonlightMapping[3] = moonlightCustom + '/mappingP3.conf'
moonlightMapping[4] = moonlightCustom + '/mappingP4.conf'

reicastBin = '/usr/bin/reicast.elf'
reicastCustom = CONF + '/reicast'
reicastConfig = reicastCustom + '/emu.cfg'
reicastConfigInit = HOME_INIT + 'configs/reicast/emu.cfg'
reicastSaves = SAVES
reicastBios = BIOS

dolphinBin = '/usr/bin/dolphin-emu-nogui'
dolphinConfig = CONF + "/dolphin-emu"
dolphinData = SAVES + "/dolphin-emu"

ppssppBin = '/usr/bin/PPSSPPSDL'
ppssppControls = CONF + '/ppsspp/PSP/SYSTEM/controls.ini'
ppssppControlsInit = HOME_INIT + 'configs/ppsspp/PSP/SYSTEM/controls.ini'

dosboxBin = '/usr/bin/doxbox'
dosboxCustom = CONF + '/dosbox'
dosboxConfig = dosboxCustom + '/dosbox.conf'

linappleBin = '/usr/bin/linapple'

scummvmBin = '/usr/bin/scummvm'
scummvmSaves = SAVES + '/scummvm'

viceBin = '/usr/bin/x64'
viceConfig = CONF + "/vice/vice.conf"

# Please keep this one at the end, and complete with your new binaries
recalboxBins = {"dosbox" : dosboxBin,
				"fba2x" :fba2xBin,
				"kodi" : kodiBin,
				"libretro" : retroarchBin,
				"linapple" : linappleBin,
				"moonlight" : moonlightBin,
				"mupen64plus" : mupenBin,
				"ppsspp" : ppssppBin,
				"reicast" : reicastBin,
				"scummvm" : scummvmBin,
				"vice" : viceBin,
				"dolphin" : dolphinBin
}
