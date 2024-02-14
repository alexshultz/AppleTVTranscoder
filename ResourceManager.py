import psutil
import shutil

class ResourceManager:
    """
    Monitors and manages system resources to ensure transcoding jobs
    do not exceed system capacity.
    """

    def check_cpu_load(self, threshold=75):
        """
        Checks if the CPU load is below the given threshold.
        :param threshold: The upper acceptable limit of CPU load percentage.
        :return: True if CPU load is below the threshold, False otherwise.
        """
        cpu_load = psutil.cpu_percent(interval=1)
        return cpu_load < threshold

    def check_memory_usage(self, threshold=75):
        """
        Checks if the memory usage is below the given threshold.
        :param threshold: The upper acceptable limit of memory usage percentage.
        :return: True if memory usage is below the threshold, False otherwise.
        """
        memory_usage = psutil.virtual_memory().percent
        return memory_usage < threshold

    def check_disk_space(self, path='/', threshold=10):
        """
        Checks if the available disk space on the given path is above the threshold.
        :param path: Path to check disk space for, default is root '/'.
        :param threshold: The minimum acceptable limit of available disk space in percentage.
        :return: True if available disk space is above the threshold, False otherwise.
        """
        disk_usage = shutil.disk_usage(path).free / shutil.disk_usage(path).total * 100
        return disk_usage > threshold

    def check_resources(self):
        """
        Implements logic to check CPU, memory usage, and disk space.
        :return: True if resources are sufficient, False otherwise.
        """
        return (self.check_cpu_load() and
                self.check_memory_usage() and
                self.check_disk_space())
