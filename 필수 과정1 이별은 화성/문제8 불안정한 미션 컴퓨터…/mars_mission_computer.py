import json
import os
import platform
import subprocess

try:
    import psutil  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    psutil = None


class MissionComputer:
    def __init__(self, setting_path='setting.txt'):
        self.setting_path = setting_path

    def _read_setting_fields(self):
        if not os.path.exists(self.setting_path):
            return None

        fields = []
        with open(self.setting_path, 'r', encoding='utf-8') as file:
            for line in file:
                item = line.strip()
                if not item or item.startswith('#'):
                    continue
                fields.append(item)
        return fields or None

    @staticmethod
    def _filter_output(data, fields):
        if fields is None:
            return data
        filtered = {}
        for key in fields:
            if key in data:
                filtered[key] = data[key]
        return filtered

    @staticmethod
    def _get_total_memory_bytes():
        if psutil is not None:
            return psutil.virtual_memory().total

        try:
            output = subprocess.check_output(
                ['sysctl', '-n', 'hw.memsize'],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            return int(output)
        except Exception:  # pylint: disable=broad-except
            return None

    @staticmethod
    def _get_memory_usage_percent():
        if psutil is not None:
            return psutil.virtual_memory().percent

        try:
            total = MissionComputer._get_total_memory_bytes()
            if not total:
                return None

            vm_stat = subprocess.check_output(['vm_stat'], text=True)
            page_size = 4096
            for line in vm_stat.splitlines():
                if 'page size of' in line:
                    tokens = line.split()
                    page_size = int(tokens[7])
                    break

            pages = {}
            for line in vm_stat.splitlines():
                if ':' not in line:
                    continue
                key, value = line.split(':', 1)
                pages[key.strip()] = int(value.strip().rstrip('.'))

            free_pages = pages.get('Pages free', 0) + pages.get('Pages speculative', 0)
            free_bytes = free_pages * page_size
            used_percent = (1.0 - (free_bytes / total)) * 100.0
            return round(used_percent, 2)
        except Exception:  # pylint: disable=broad-except
            return None

    @staticmethod
    def _get_cpu_usage_percent():
        if psutil is not None:
            return psutil.cpu_percent(interval=1.0)

        try:
            one_minute_load = os.getloadavg()[0]
            cpu_cores = os.cpu_count() or 1
            return round((one_minute_load / cpu_cores) * 100.0, 2)
        except Exception:  # pylint: disable=broad-except
            return None

    def get_mission_computer_info(self):
        try:
            memory_total_bytes = self._get_total_memory_bytes()

            info = {
                'operating_system': platform.system(),
                'operating_system_version': platform.version(),
                'cpu_type': platform.processor() or platform.machine(),
                'cpu_core_count': os.cpu_count(),
                'memory_size_gb': (
                    round(memory_total_bytes / (1024 ** 3), 2)
                    if memory_total_bytes is not None
                    else 'N/A'
                ),
            }
        except Exception as error:  # pylint: disable=broad-except
            info = {'error': f'system info 조회 실패: {error}'}

        output = self._filter_output(info, self._read_setting_fields())
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return output

    def get_mission_computer_load(self):
        try:
            load = {
                'cpu_usage_percent': self._get_cpu_usage_percent(),
                'memory_usage_percent': self._get_memory_usage_percent(),
            }
        except Exception as error:  # pylint: disable=broad-except
            load = {'error': f'system load 조회 실패: {error}'}

        output = self._filter_output(load, self._read_setting_fields())
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return output


if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
