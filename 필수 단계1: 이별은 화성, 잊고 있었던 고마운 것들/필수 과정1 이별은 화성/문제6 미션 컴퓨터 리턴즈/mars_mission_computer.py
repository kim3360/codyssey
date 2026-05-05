import random
from datetime import datetime


class DummySensor:
    """테스트용 더미 센서. 환경 값을 랜덤 범위로 생성한다."""

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
        """random으로 지정 범위의 값을 생성해 env_values에 채운다."""
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        """env_values를 반환하고, 동일 항목을 파일 로그로 남긴다."""
        log_path = 'mars_mission_sensor.log'
        timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
        line = (
            f'{timestamp}\t'
            f"내부온도={self.env_values['mars_base_internal_temperature']}\t"
            f"외부온도={self.env_values['mars_base_external_temperature']}\t"
            f"내부습도={self.env_values['mars_base_internal_humidity']}\t"
            f"외부광량={self.env_values['mars_base_external_illuminance']}\t"
            f"내부CO2={self.env_values['mars_base_internal_co2']}\t"
            f"내부산소={self.env_values['mars_base_internal_oxygen']}\n"
        )
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(line)
        return self.env_values


if __name__ == '__main__':
    ds = DummySensor()
    ds.set_env()
    env = ds.get_env()
    print(env)
