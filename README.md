# Archlinux Post-Installation Configuration

The following files represent the post-installation configuration for an Archlinux environment based on 2 possible GUI providers (Qtile or Hyperland); however, **Qtile environment is no logner updated or mantained**. Keep in mind that dispide Hyperland been an electron GUI managed, most of the apps used are rocomended to be GTK, in order to apply the corresponding themes that match the overall configuration.

## OS & Hardware Recommendations
- OS: Most recent **Archlinux image** with updated Key's
- ~ partition: Used for files and NOT FOR SOFTWARE (Recommended 50% or less if you are a developer that uses a lot of tools)
- / partition: Used for the OS and al, of the packages (Recommended 50% or more if you are a developer)
- Swap: Should be the amount of space your RAM has
- WM/Compositor: Hyperland
- Intel or AMD drivers should be installed depending on your CPU

## Hyperland
- All hyperland related configurations (Including addintion depending software) is at the folder **hypr/**
- Use waybar for the navbar and the styles and modules on **waybar/**
  - You sould have a Nerd-Font installed of your choise
  - Use **wofi** package for menu management
  - Install Thunar File explorer based on GTK and delete Dolphin
  - Install a browser of your choise. Current configuration: Zen-Browser on WIN+B
- Install Hyprshot for screenshots in HD

## Terminal (Kitty)
- You should have installed at least one or more Nerd-Font of your choise
- Use the configuration files for the Kitty terminal
- Use fish with OMF (Oh My Fish -> Chain Theme)
- For a better terminal experience you should install **htop, fastfetch and cmatrix** packages through pacman

## Additional Software
- PortMaster: Firewall and overall connection security
- NetworkManager (nmcli): Connection interface for Wifi and Ethernet managment
- ProtonVPN: Free VPN for IP Mask at public spaces
- Sublime Text and (Neovim, Code OSS): Text and Code editors
- PulseAudio: Audio and Mic managment
