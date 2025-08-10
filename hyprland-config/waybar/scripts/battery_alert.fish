#!/usr/bin/fish

while true
  set battery_level (cat /sys/class/power_supply/BAT*/capacity)
  set battery_status (cat /sys/class/power_supply/BAT*/status)

  if test $battery_level -le 10 -a "$battery_status" = "Discharging"
    notify-send \
      -u critical \
      -a "Battery Alert" \
      -i "battery-empty-symbolic" \
      "Battery Critical: $battery_level%" \
      "Connect charger immediately."
    # Optional: Play a sound
    # paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga &
  end

  sleep 300  # Check every 5 minutes
end
