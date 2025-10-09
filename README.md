# fivem-launcher
Stupid simple python app to auto launch fivem with specific params. 

Made to help dev workflow & stop annoying relaunches if you play on multiple servers

## Features

- Auto launch with pure mode
- Auto launch with specific FiveM build
- Auto-connects to server (Sometimes, I swear this doesn't work most of the time)
- **Per-server mod management** - Install different mods for different servers using hardlinks
- **Per-server game settings** - Automatically swap graphics/game settings based on which server you're joining
- **Benefits:** Stops annoying fivem relaunch & keeps your mods/settings organized

### Mod & Settings Presets
- Create presets in `%APPDATA%/houseoffun/fivem_launcher/modpresets/[PresetName]/`
- Each preset can contain:
    - `mods/` - FiveM mods that will be hardlinked to `%LOCALAPPDATA%/FiveM/FiveM.app/mods`
    - `plugins/` - FiveM plugins that will be hardlinked to `%LOCALAPPDATA%/FiveM/FiveM.app/plugins`
    - `settings/gta5_settings.xml` - Custom game settings for this preset
- Assign presets to servers in config with `"mod_preset": "PresetName"`
- Leave `"mod_preset": ""` for no mods/default settings
- The launcher automatically:
    - Installs only the mods needed for the selected server
    - Removes mods that shouldn't be there
    - Swaps game settings before launch
    - Backs up your original settings

### Devs & CL2
- Set your Fxserver.exe in the config
    - This adds "Launch Server" button in the UI
- Set your dev server with type: "dev"
    - Does not support multiple dev servers, only have one type "dev" configured.
- Enable cl2 config option
    - This adds cl2 launch button in the UI, which will launch cl2 with required params

## How
1. Launch app
2. Click `Edit` button
3. Add servers and required info
    - Optionally add `"mod_preset": "PresetName"` to use custom mods/settings for that server
4. Click `Refresh` button
5. Click server in the list. Enjoy.

## Config
- Just do it in the application UI. It auto opens your default text editor.
    - But, it's located at `%APPDATA%/houseoffun/fivem_launcher/config.json`

### Example Server Config
```json
{
  "name": "My Awesome Server",
  "connection": "cfx.re/join/abcd1234",
  "pure_mode": 2,
  "gamebuild": 2189,
  "type": "play",
  "mod_preset": "HighQuality"
}
```

## Setting Up Mod/Settings Presets

### Creating a Preset
1. Navigate to `%APPDATA%/houseoffun/fivem_launcher/modpresets/`
2. Create a new folder with your preset name (e.g., `HighQuality`)
3. Inside, you can add:
   - `mods/` folder - Place your FiveM mods here
   - `plugins/` folder - Place your FiveM plugins here
   - `settings/gta5_settings.xml` - Copy your desired game settings here

### Example Preset Structure
```
modpresets/
├── HighQuality/
│   ├── mods/
│   │   └── my-cool-mod.asi
│   ├── plugins/
│   │   └── some-plugin.dll
│   └── settings/
│       └── gta5_settings.xml
├── LowPerformance/
│   ├── mods/
│   ├── plugins/
│   └── settings/
│       └── gta5_settings.xml
└── DevMode/
    ├── mods/
    └── plugins/
```

### How It Works
- **Hardlinks**: Mods/plugins use hardlinks (not copies), saving disk space
- **Auto-sync**: When you select a server, the launcher:
  1. Removes mods that shouldn't be there
  2. Installs mods for the selected preset
  3. Swaps to the preset's game settings
- **Backup**: Your original settings are backed up to `settings_backup/`
- **No preset**: Servers without a preset get clean install (no mods) and default settings


# Preview (Simple, Stupid, and Ugly)

![Launcher UI](assets/launcher_img.png)
