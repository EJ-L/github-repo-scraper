from datetime import datetime, timedelta, timezone

def time_list_generation(num_of_tokens):
    # Define start and end times with GMT+8 timezone
    start_time = datetime(2023, 1, 1, 0, 0, tzinfo=timezone(timedelta(hours=8)))
    end_time = datetime(2024, 1, 1, 0, 0, tzinfo=timezone(timedelta(hours=8)))

    # Calculate the total duration and interval duration
    total_duration = end_time - start_time
    interval_duration = total_duration / num_of_tokens

    # Generate the list of tuples with equally divided intervals
    time_intervals = []
    current_start = start_time

    for _ in range(num_of_tokens):
        current_end = current_start + interval_duration
        # Use isoformat() to get the correct timezone format
        start_str = current_start.strftime('%Y-%m-%dT%H:%M:%S') + current_start.strftime('%z')[:3] + ':' + current_start.strftime('%z')[3:]
        end_str = current_end.strftime('%Y-%m-%dT%H:%M:%S') + current_end.strftime('%z')[:3] + ':' + current_end.strftime('%z')[3:]
        time_intervals.append((start_str, end_str))
        current_start = current_end

    # Print the result as a list of tuples
    return time_intervals
