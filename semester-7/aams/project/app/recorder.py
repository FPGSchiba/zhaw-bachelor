"""CSV recording of per-step measurements (one file per recording, in ./runs)."""
import csv
import os
import time

COLUMNS = ("step", "rule", "channels", "kernels", "mass", "live", "speed", "activity", "concentration",
           "mu", "sigma", "theta")


class CsvRecorder:
    def __init__(self, folder="runs"):
        self.folder = folder
        self.file, self.writer, self.path = None, None, None

    @property
    def active(self):
        return self.file is not None

    def start(self):
        os.makedirs(self.folder, exist_ok=True)
        self.path = os.path.join(self.folder, f"run_{time.strftime('%Y%m%d_%H%M%S')}.csv")
        self.file = open(self.path, "w", newline="")  # noqa: SIM115 - stays open across writes, closed in stop()
        self.writer = csv.writer(self.file)
        self.writer.writerow(COLUMNS)
        return self.path

    def write(self, step, params, stats):
        if not self.active:
            return
        k = params["kernels"][params["selected"]]
        self.writer.writerow([step, params["rule"], params["channels"], len(params["kernels"]),
                              f"{stats['mass']:.4f}", stats["live"], f"{stats['speed']:.5f}",
                              f"{stats['activity']:.6f}", f"{stats['concentration']:.4f}",
                              k["mu"], k["sigma"], params["theta"]])

    def stop(self):
        if self.active:
            self.file.close()
        self.file, self.writer = None, None
