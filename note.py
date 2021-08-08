

class Note:
    def __init__(self, note, start_time):
        self.note = note
        self.start_time = start_time
        self.duration = 0
        self.endtime = start_time

    def set_end_time(self, endtime):
        self.endtime = endtime
        self.duration = endtime - self.start_time

    def get_start_time(self):
        return self.start_time

    def get_duration(self):
        return self.duration

    def __repr__(self):
        return "\n" + self.note + " " + str(self.start_time) + " " + str(self.endtime)
