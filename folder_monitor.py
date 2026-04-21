import time
import signal
import sys
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class NewFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.processed_files = set()

    def on_created(self, event):
        if not event.is_directory:
            if event.src_path not in self.processed_files:
                self.processed_files.add(event.src_path)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                filename = event.src_path
                print(f'[{timestamp}] 新文件: {filename}')


def signal_handler(sig, frame):
    print('\n监控已停止，正在退出...')
    observer.stop()
    observer.join()
    sys.exit(0)


def main():
    global observer

    if len(sys.argv) < 2:
        print('用法: python folder_monitor.py <要监控的文件夹路径>')
        sys.exit(1)

    folder_to_watch = sys.argv[1]

    print(f'开始监控文件夹: {folder_to_watch}')
    print('按 Ctrl+C 停止监控')

    signal.signal(signal.SIGINT, signal_handler)

    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    main()
