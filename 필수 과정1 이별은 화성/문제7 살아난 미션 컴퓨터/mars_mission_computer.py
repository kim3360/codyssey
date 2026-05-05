import json
import random
import threading
import time


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        return self.env_values.copy()


class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }
        self.ds = DummySensor()
        self._should_stop = False
        self._samples_5min = []
        self._last_avg_time = time.time()

    def _wait_for_stop_key(self):
        print("중지하려면 'q'를 입력하고 Enter를 누르세요.")
        while not self._should_stop:
            try:
                user_input = input().strip().lower()
            except EOFError:
                user_input = ''
            if user_input == 'q':
                self._should_stop = True

    def _print_five_minute_average(self):
        if not self._samples_5min:
            return

        sums = {key: 0.0 for key in self.env_values}
        for _, sample in self._samples_5min:
            for key, value in sample.items():
                sums[key] += value

        count = len(self._samples_5min)
        avg_values = {key: round(total / count, 3) for key, total in sums.items()}

        print('5분 평균 환경값:')
        print(json.dumps(avg_values, ensure_ascii=False, indent=2))

    def get_sensor_data(self):
        stop_listener = threading.Thread(target=self._wait_for_stop_key, daemon=True)
        stop_listener.start()

        while not self._should_stop:
            self.ds.set_env()
            self.env_values = self.ds.get_env()

            print(json.dumps(self.env_values, ensure_ascii=False, indent=2))

            now = time.time()
            self._samples_5min.append((now, self.env_values.copy()))

            cutoff = now - 300
            self._samples_5min = [
                sample_item
                for sample_item in self._samples_5min
                if sample_item[0] >= cutoff
            ]

            if now - self._last_avg_time >= 300:
                self._print_five_minute_average()
                self._last_avg_time = now

            for _ in range(50):
                if self._should_stop:
                    break
                time.sleep(0.1)

        print('System stoped...')


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
