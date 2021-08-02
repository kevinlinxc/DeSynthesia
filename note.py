

class Note:
    def __init__(self, note, starttime):
        self.note = note
        self.starttime = starttime
        self.duration = 0
        self.endtime = starttime

    def set_end_time(self, endtime):
        self.endtime = endtime
        self.duration = endtime - self.starttime

    def get_start_time(self):
        return self.starttime

    def get_duration(self):
        return self.duration

    def __repr__(self):
        return "\n" + self.note + " " + str(self.starttime) + " " + str(self.endtime)

