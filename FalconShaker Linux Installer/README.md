# CachyOS Wine/Proton Shortcut Creator Tool

A lightweight, automated Bash script designed for CachyOS (and Arch-based Linux distributions) to quickly generate Linux desktop shortcuts (`.desktop` files) for Windows applications running under Wine or Proton. 

While optimized to automatically detect and map **FalconShaker** versions inside a `falcon-bms` directory structure, it can be used to generate shortcuts for any target executable.

## 🚀 Features (Slop generated. May or may not be true)

*   **Smart Auto-Detection**: Automatically reads the current system user to build safe, absolute environment paths.
*   **FalconShaker Integration**: Searches for folders matching `FalconShaker *` dynamically and opens the file picker directly inside the latest discovered version directory.
*   **GUI-Driven Selection**: Uses `zenity` dialogs for simple, intuitive point-and-click selection of target executables, Wine prefixes, and custom compatibility runners.
*   **Automated Dependency Check**: Checks for `zenity` upon launch and automatically installs it via `pacman` if it is missing.
*   **Icon Auto-Mapping**: Automatically extracts and links the first `.ico` file found in the application's root folder to the final desktop shortcut.
*   **Executable Shortcuts**: Builds standard XDG-compliant desktop entries and automatically flags them as executable so they are ready to launch immediately.

## 📋 Prerequisites

*   An Arch Linux-based operating system (like **CachyOS**).
*   Sudo privileges (only required if `zenity` needs to be installed automatically).
*   A pre-configured Wine Prefix and Wine/Proton runner.

The script defaults to scanning target folders within `~/Games/falcon-bms/`. If your paths differ, you can freely browse to them when the graphical picker opens.

## 🛠️ Installation & Setup

1. **Download Falcon**  
   Download FalconShaker and place it somewhere. Script default is within the falcon-bms directory created by the BMS helper script.

2. **Download the FalconShaker Linux Installer**
    Place this anywhere.
    Right click and run it as a program.
    
3.  **Follow the Prompts**  
    Select your FalconShaker executable. The script will default to the latest version and should find the correct directory if it is placed in the falcon-bms directory.
    Select your wine prefix. Again, if you have used the BMS helper script, this should land on the default.
    Select the proton runner. Same as above, should land on the default.

4.  **Make Executable**
    The desktop executable should now be on your desktop. Right click it and select Allow Launching.
    
5. **Launch Order Matter**
    If you launch FalconShaker before the BMS launcher, it will just exit when the BMS launcher runs. Instead launch the BMS launcher first, then run FalconShaker. Usage should otherwise be the same as on Windows.
    
6. **Use it on other stuff!**
    Just navigate to another exe that you would like to run along side BMS. A good example is kungfoo's BMS control Server. Selecting an exe that is not FalconShaker related will add an additional prompt if the application needs to run in terminal mode.
    
    

### What Happens Step-by-Step:
1. **System Check**: The script identifies your username and ensures `zenity` is ready.
2. **Select executable (`.exe`)**: A window opens (defaulted to your active `FalconShaker` folder) for you to pick the target Windows application.
3. **Select WINEPREFIX**: A folder selection window prompts you to pick the specific Wine prefix directory driving the application.
4. **Select Runner**: A window prompts you to pick the directory containing your intended compatibility binaries (defaults to `runners/GE-Proton10-32/files/bin`).
5. **Shortcut Created**: Your desktop file is compiled, injected with the application's icon, and delivered cleanly to your `~/Desktop/`.

## ⚙️ Configuration Defaults

The script uses the following internal structure as its primary baseline, fallback, and initial folder viewport:

*   **Base BMS Directory**: `~/Games/falcon-bms`
*   **Target Runner Directory**: `~/Games/falcon-bms/runners/GE-Proton10-32/files/bin`

If you routinely utilize alternative root installations, open the script in a text editor and modify the environment variables directly under section `# Set base folder paths`.

