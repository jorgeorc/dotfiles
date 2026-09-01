# Fix intel GPU colors
xrandr --output HDMI-1 --set "Broadcast RGB" "Full"

# Run i3
exec dbus-launch --sh-syntax --exit-with-session i3
