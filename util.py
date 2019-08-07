import os, time, importlib, threading, subprocess, glob

def cwd():
    return os.getcwd()

def find_extension(extension, minutes = 0, hours = 0, days = 0, weeks = 0):
    extension = extension if "." in extension else "." + extension
    files = []
    for file in os.listdir(cwd()):
        if file.endswith(extension):
            if (minutes or hours or days or weeks):
                if (delta.within(file, minutes, hours, days, weeks)):
                    files.append(os.path.join(cwd(), file))
    return files

def find_timestamp(file):
    return os.path.getmtime(file)

class timedelta:
    def minute(self):
        return (60)

    def hour(self):
        return (60 * self.minute())

    def day(self):
        return (24 * self.hour())

    def week(self):
        return (7 * self.day())

    def get(self, minutes = 0, hours = 0, days = 0, weeks = 0):
        return (self.minute() * minutes + self.hour() * hours + self.day() * days + self.week() * weeks)

    def within(self, timestamp, minutes = 0, hours = 0, days = 0, weeks = 0):
        if (isinstance(timestamp, str)):
            timestamp = find_timestamp(timestamp)
        now = time.time()
        if ((now - self.get(minutes = minutes, hours = hours, days = days, weeks = weeks)) <= timestamp):
            return True
        return False

delta = timedelta()