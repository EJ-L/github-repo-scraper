from datetime import datetime, timedelta, timezone

# Define start and end times with GMT+8 timezone
start_time = datetime(2023, 1, 1, 0, 0, tzinfo=timezone(timedelta(hours=8)))
end_time = datetime(2024, 1, 1, 0, 0, tzinfo=timezone(timedelta(hours=8)))

# Calculate the total duration and interval duration
total_duration = end_time - start_time
interval_duration = total_duration / 6

# Generate the list of tuples with equally divided intervals
time_intervals = []
current_start = start_time

for _ in range(6):
    current_end = current_start + interval_duration
    # Format each datetime with the specified format
    start_str = current_start.strftime('%Y-%m-%dT%H:%M:%S%z')
    end_str = current_end.strftime('%Y-%m-%dT%H:%M:%S%z')
    time_intervals.append((start_str, end_str))
    current_start = current_end

# Print the result as a list of tuples
print(time_intervals)
