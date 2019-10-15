import datetime,calendar
class MyDate():
    def __init__(self):
        now = datetime.datetime.now()
        self.year = now.year
        self.month = now.month
        self.result = []
    def get_date(self):
        days = calendar.monthrange(year=self.year, month=self.month)[1]
        ## 某年某月第一天周几
        first_week = datetime.date(self.year, self.month, 1).weekday()
        ### 某年某月最后一天周几
        # last_week = datetime.date(self.year, self.month, days).weekday()
        all_day = [x for x in range(7-first_week+1,days)]
        line = []
        for i in range(first_week):
           line.append('empty')
        for j in range(7-first_week):
            line.append(j+1)
        self.result.append(line)
        while all_day:
            line = []
            for i in range(7):
                if len(line) < 7 and all_day:
                    line.append(all_day.pop(0))
                else:
                    line.append('empty')
            self.result.append(line)


        return self.result
    def print_result(self):
        result = self.get_date()
        return result






