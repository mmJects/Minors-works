from datetime import datetime

def sorting_time(data):
    time = datetime.now()
    timee = int(time.strftime("%H%M"))
    day = int(time.strftime("%d"))
    near,far = [] , []
    track = {}
    for value in data.values():
        timeee = value[1].split(":")
        timestamp = int(timeee[0]+timeee[1])
        if timestamp < timee:
            far.append(timestamp)
        elif int(timeee[2]) > day:
            far.append(timestamp)
        else:
            near.append(timestamp)
        track[timestamp] = [value[0],value[1]]
    near.sort()
    far.sort()
    near.extend(far)
    i = 0
    for key in data.keys():
        data[key] = track[near[i]]
        i += 1
    return data

day_max = [31,28,31,30,31,30,31,31,30,31,30,31]
month_count = ["Janurary","Februrary","March","April","May","June","July","August","September","Ocotber","November","December"]
allowed_day_range = 10

def my_nums(start,month,year=2023):
    day = start
    count = 0
    while count != allowed_day_range:
        if day > day_max[month-1]:
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
        yield month , day , year
        day += 1
        count += 1

def give_the_days_range():
    time = datetime.now()
    day = int(time.strftime("%d"))
    month = int(time.strftime("%m"))
    day_range = {}
    for m,d,y in my_nums(day,month):
        day_range[day] = f"{month_count[m-1]} {d} , {y}"
        day += 1
    return day_range

def give_the_month(will_day):
    time = datetime.now()
    day = int(time.strftime("%d"))
    month = int(time.strftime("%m"))
    max_range_day = allowed_day_range - ( day_max[month-1] - day)
    r_month = month_count[month] if 1 <= will_day <= max_range_day else month_count[month-1]
    return f"{r_month} {will_day}"