class GPSSignalLostError(Exception):
     """Ngoại lệ tùy chỉnh khi thiết bị mất tín hiệu định vị GPS."""


def get_current_location():
     """Mô phỏng truy cập phần cứng GPS để lấy tọa độ."""
     return (10.0, 105.0)