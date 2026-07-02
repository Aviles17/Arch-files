# hyprland-config

Configuración activa del escritorio Hyprland: compositor, barra de estado, lanzador, terminal, shell, explorador de archivos y theming GTK. Esta guía explica qué hace cada archivo y cómo dejarlo funcionando en un sistema Arch Linux nuevo.

## Índice de configuraciones

### `hypr/` — Compositor Hyprland

| Archivo | Qué hace |
|---|---|
| `hyprland.conf` | Configuración principal: monitores, programas por defecto (`kitty`, `thunar`, `wofi`), autostart, apariencia (bordes, gaps, blur, animaciones), input (layout de teclado `es`), keybindings y reglas de ventana. |
| `hypridle.conf` | Reglas de inactividad: apaga la pantalla (DPMS off) a los 10 min de inactividad y bloquea la sesión (`loginctl lock-session`) a los 8 min mediante `hyprlock`. |
| `hyprlock.conf` | Apariencia de la pantalla de bloqueo (fondo, blur, reloj, campo de contraseña). |
| `hyprpaper.conf` | Wallpaper del escritorio (`~/Pictures/v6-background.jpg`), con `splash = false` para quitar las frases random de Hyprland. |
| `hyprlock.png` | Imagen de fondo usada por `hyprlock.conf`. |

Puntos a tener en cuenta de `hyprland.conf`:
- `$mainMod` es la tecla **Super**.
- `SUPER + Return` abre kitty, `SUPER + E` abre Thunar, `SUPER + M` abre wofi, `SUPER + B` abre Zen Browser.
- `SUPER + S` / `SUPER + SHIFT + S` disparan `hyprshot` (región / ventana).
- `SUPER + SHIFT + L` bloquea la sesión con `hyprlock`.
- Al final del archivo se lanza `battery_alert.fish` (ver más abajo) vía `exec-once`.

### `waybar/` — Barra de estado

| Archivo | Qué hace |
|---|---|
| `config.jsonc` | Módulos activos: workspaces de Hyprland, reloj, batería, red, bluetooth, audio, brillo, CPU, logo de Arch, tray, modo avión, etc. |
| `style.css` / `colors.css` | Estilos visuales de la barra (paleta de colores separada del layout para facilitar cambios de tema). |
| `scripts/battery_alert.fish` | Script en segundo plano (lanzado desde `hyprland.conf`) que revisa la batería cada 5 min y dispara una notificación crítica vía `notify-send` si queda ≤10% y está descargando. |

### `wofi/` — Lanzador de aplicaciones

`style.css` define la apariencia del menú (`wofi --show drun`, invocado con `SUPER + M`).

### `kitty/` — Terminal

- `kitty.conf`: configuración general de la terminal.
- `current-theme.conf`: tema de color **Catppuccin Mocha**.

### `fish/` — Shell

Solo se versiona `config.fish`. Ese archivo llama a `fastfetch` al abrir una sesión interactiva y desactiva el saludo por defecto de fish (`fish_greeting`).

**Deliberadamente no se versionan:**
- `fish_variables` — base de datos interna de variables universales de fish. Cambia de formato entre versiones de fish (se detectó una migración de 3.8 a 4.3 entre el repo viejo y el sistema actual) y no es apta para portar a mano.
- `conf.d/fish_frozen_*.fish` — archivos que fish genera automáticamente al migrar de versión; sus propios comentarios indican que no deben editarse ni versionarse.
- `conf.d/omf.fish` y `functions/fish_prompt.fish` — generados/gestionados por el instalador de Oh My Fish; se recrean solos al instalar OMF y un tema (ver instalación abajo).

### `gtk-3.0/` — Theming GTK

`settings.ini` fija el tema `adw-gtk3-dark` (+ iconos Adwaita, cursor Adwaita). Es el archivo que realmente controla la apariencia de las apps GTK3 (Thunar, wofi) sin necesidad de variables de entorno adicionales.

### `Thunar/` — Explorador de archivos

- `accels.scm`: atajos de teclado personalizados.
- `uca.xml`: acciones personalizadas del menú contextual.

### `mimeapps.list`

Define las aplicaciones por defecto: **Zen Browser** para http/https/html, entre otras asociaciones.

### `Pictures/`

Wallpapers e imagen de usuario usados por `hyprpaper.conf`, `hyprlock.conf` y el login.

## Qué se descartó y por qué

- **Kvantum / qt5ct**: se evaluaron pero no se incluyen. Auditoría de cableado: `hyprland.conf` no exporta `QT_QPA_PLATFORMTHEME`, y `qt5ct.conf` estaba fijado en `style=Fusion` (no en Kvantum), por lo que las apps Qt lanzadas desde Hyprland o wofi no heredan el tema. Sí se encontraron las variables `QT_QPA_PLATFORMTHEME=qt5ct` y `QT_STYLE_OVERRIDE=kvantum` como variables **universales exportadas de fish** — esto significa que una app Qt abierta escribiendo el comando en una terminal (kitty/fish) sí toma el tema Kvantum, pero cualquier app lanzada por wofi o por `exec-once` no, porque esos procesos no heredan el entorno de una sesión fish. Al no haber prácticamente apps Qt en el flujo de trabajo (se recomienda Thunar sobre Dolphin), no se consideró justificado mantener esa configuración.
- **SDDM (tema Astronaut)**: no se vendorea el tema completo (assets, fuentes y componentes QML de terceros) dentro de este repo. Se instala aparte — ver sección de instalación.
- **fastfetch**: no tiene archivo de configuración propio en este setup; se invoca como comando dentro de `fish/config.fish`. Se lista como dependencia de pacman, no como configuración.
- **PortMaster**: aplicación standalone sin configuración de usuario relevante para versionar.
- **Neovim**: instalado en el sistema pero sin uso activo ni configuración; no se documenta como parte del flujo.

## Instalación en un sistema nuevo

### 1. Paquetes base (pacman / AUR)

```bash
# Compositor y utilidades de Hyprland
sudo pacman -S hyprland hypridle hyprlock hyprpaper xdg-desktop-portal-hyprland

# Barra, lanzador y terminal
sudo pacman -S waybar wofi kitty

# Shell
sudo pacman -S fish

# Explorador de archivos (GTK) y GTK theming
sudo pacman -S thunar gtk3 adw-gtk-theme

# Utilidades varias mencionadas en el repo
sudo pacman -S htop cmatrix fastfetch networkmanager brightnessctl playerctl pipewire pipewire-pulse wireplumber

# AUR (usando yay u otro helper)
yay -S hyprshot zen-browser-bin protonvpn-cli sddm sublime-text-4
```

> Instalar además el driver de GPU correspondiente (`intel-media-driver` o el stack de AMD) y al menos una Nerd Font (ej. `ttf-jetbrains-mono-nerd`).

### 2. Copiar las configuraciones

```bash
git clone git@github.com:Aviles17/Arch-files.git
cd Arch-files/hyprland-config

mkdir -p ~/.config
cp -r hypr waybar wofi kitty gtk-3.0 Thunar ~/.config/
cp mimeapps.list ~/.config/mimeapps.list
mkdir -p ~/Pictures
cp Pictures/*.jpg ~/Pictures/
chmod +x ~/.config/waybar/scripts/battery_alert.fish

mkdir -p ~/.config/fish
cp fish/config.fish ~/.config/fish/config.fish
```

### 3. Fish + Oh My Fish

```bash
curl -L https://get.oh-my-fish.org | fish
omf install chain    # o el tema que prefieras
```

> Nota: en el sistema de referencia el tema activo real era **boxfish**, aunque el estado interno de OMF (`~/.config/omf/theme`) seguía marcando **chain** — es una inconsistencia conocida de OMF cuando se cambia de tema sin que actualice su propio archivo de estado. Verificá con `omf theme` cuál está realmente activo y fijalo explícitamente con `omf theme <nombre>`.

### 4. SDDM y tema de login

```bash
sudo pacman -S sddm
sudo systemctl enable sddm
```

Instalar el tema desde uno de estos repos (el segundo es el original, el primero el fork de respaldo usado en este setup):
- https://github.com/Aviles17/sddm-backup-repo
- https://github.com/Keyitdev/sddm-astronaut-theme

Seguí las instrucciones de instalación de ese repo (clonar en `/usr/share/sddm/themes/` y setear `Current=` en `/etc/sddm.conf.d/`).

### 5. Verificaciones post-instalación

- `hyprctl reload` tras cualquier cambio en `hypr/hyprland.conf`.
- Confirmar que `~/.config/waybar/scripts/battery_alert.fish` tiene permisos de ejecución (`chmod +x`) — el `exec-once` de `hyprland.conf` depende de eso.
- Si algún ícono no se ve en waybar/kitty, falta una Nerd Font instalada y seleccionada.
