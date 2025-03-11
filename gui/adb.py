import os.path
import subprocess


def run_adb_command(command) -> list[str]:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout
    lines = []
    for line in output.splitlines():
        if line.startswith('*') or len(line) == 0:
            continue
        lines.append(line)
    return lines


class Adb:

    def __init__(self):
        self.devices = []
        self.device = ''
        self.isdir_map = {'': False}
        self.scan_devices()

    def scan_devices(self):
        """
        获取连接的设备列表
        :return:
        """
        self.devices.clear()
        lines = run_adb_command('adb devices')
        for i in range(1, len(lines)):
            line = lines[i]
            if len(line) <= 0 or line.startswith('*'):
                continue
            device = line.split()[0]
            if len(device) > 0:
                self.devices.append(device)
        if len(self.devices) > 0:
            self.device = self.devices[0]

    def listdir(self, path: str) -> list[str]:
        command = f'adb -s {self.device} shell ls {path}'
        names = run_adb_command(command)
        return names

    def isdir(self, path: str) -> bool:
        if path not in self.isdir_map.keys():
            command = f'adb -s {self.device} shell ls {path}'
            lines = run_adb_command(command)
            is_dir = True
            if len(lines) == 1 and lines[0] == path:
                is_dir = False
            self.isdir_map[path] = is_dir
        return self.isdir_map[path]

    def pull(self, device_path: str, out_path: str) -> list[str]:
        if os.path.exists(out_path) and not os.path.isdir(out_path):
            return []
        os.makedirs(out_path, exist_ok=True)
        command = f'adb -s {self.device} pull {device_path} {out_path}'
        lines = run_adb_command(command)
        for line in lines:
            print(line)
        return lines


if __name__ == '__main__':
    adb = Adb()
    adb.scan_devices()
    adb.pull('/sdcard/IMG_20240711_213547.jpg', '/Users/zhouzhenliang/zhouzhenliang/device_temp/a/')
