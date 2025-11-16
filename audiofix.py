import psutil
import time
import os
import sys
import threading

PROCESS_NAME = "audiodg.exe"
THRESHOLD_MB = 350
CHECK_INTERVAL = 1  # seconds

def get_process():
    """Return the first audiodg.exe process found, or None."""
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        if proc.info['name'] and proc.info['name'].lower() == PROCESS_NAME:
            return proc
    return None


# Attempt to import tray libraries (pystray + Pillow). If they're not available,
# fall back to the original console-only loop.
try:
    from PIL import Image, ImageDraw
    import pystray
except Exception:
    pystray = None


def make_image(color):
    """Create a simple 16x16 RGBA circle image of the given color."""
    image = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((1, 1, 14, 14), fill=color)
    return image


def monitor_loop(icon, stop_event):
    """Background monitor that updates the tray icon/title and kills audiodg if needed."""
    while not stop_event.is_set():
        proc = get_process()

        if proc:
            mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
            title = f"audiodg.exe: {mem_mb:.1f} MB"

            if mem_mb > THRESHOLD_MB:
                title += " — HIGH (killing)"
                try:
                    proc.kill()
                except Exception:
                    # ignore kill errors; keeping the icon updated is the main goal
                    pass
                try:
                    icon.icon = make_image('red')
                except Exception:
                    pass
            else:
                title += " — OK"
                try:
                    icon.icon = make_image('green')
                except Exception:
                    pass

        else:
            title = "audiodg.exe not found"
            try:
                icon.icon = make_image('gray')
            except Exception:
                pass

        try:
            # tooltip text shown on hover
            icon.title = title
        except Exception:
            # some backends don't allow changing title while running; ignore
            pass

        time.sleep(CHECK_INTERVAL)


def console_loop():
    """Fallback: original console loop if tray libs are unavailable."""
    while True:
        proc = get_process()

        if proc:
            mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
            print(f"audiodg.exe memory: {mem_mb:.1f} MB")

            if mem_mb > THRESHOLD_MB:
                print(f"[!] Memory exceeded {THRESHOLD_MB} MB — killing audiodg.exe (PID {proc.pid})")
                try:
                    proc.kill()
                except Exception as e:
                    print("Failed to kill process:", e)
            else:
                print("OK (below threshold)")

        else:
            print("audiodg.exe not found — waiting for it to start...")

        time.sleep(CHECK_INTERVAL)


if pystray is None:
    # If pystray or Pillow not installed, print a helpful message and run console loop.
    print("pystray and/or Pillow not available. Install requirements from requirements.txt and run with pythonw.exe to get a tray icon.")
    console_loop()
else:
    # Create tray icon, start monitor thread, and run the tray event loop.
    stop_event = threading.Event()

    def on_quit(icon, item):
        stop_event.set()
        # Stop the icon main loop; after this the program will exit.
        icon.stop()

    icon = pystray.Icon(
        "audiofix",
        make_image('gray'),
        "audiofix",
        menu=pystray.Menu(pystray.MenuItem('Quit', on_quit))
    )

    monitor_thread = threading.Thread(target=monitor_loop, args=(icon, stop_event), daemon=True)
    monitor_thread.start()

    # This blocks until icon.stop() is called (for example via the Quit menu).
    icon.run()

    # Ensure background thread is told to stop and we wait a moment.
    stop_event.set()
    monitor_thread.join(timeout=1)
