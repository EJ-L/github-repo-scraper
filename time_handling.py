from datetime import datetime, timedelta

def next_hour(full_date, end_time, extra_hour=1, extra_min=0, extra_sec=0):
    date_string = full_date.replace("+08:00", "")
    date_time_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    next_hour = date_time_obj + timedelta(hours=extra_hour, minutes=extra_min, seconds=extra_sec)
    end_time = end_time.replace("+08:00", "")
    end_time_obj = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
    if end_time_obj < next_hour:
        next_hour = end_time_obj
    
    next_hour_string = next_hour.strftime("%Y-%m-%dT%H:%M:%S")
    return next_hour_string + "+08:00"

def time_smaller_than(time, end_time):
    time = time.replace("+08:00", "")
    end_time = end_time.replace("+08:00", "")
    dt_obj1, dt_obj2 = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S"), datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
    return dt_obj1 < dt_obj2

def get_next_period(start_time, end_time, **kwargs):
    return "stars:>100 created:" + start_time + ".." + next_hour(start_time, end_time,**kwargs)
    # return "stars:>100 created:>=" + start_time