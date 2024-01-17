def _fromat_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    milliseconds = seconds % 1 * 100
    return "{:02}:{:02}:{:02}".format(int(minutes), int(seconds), int(milliseconds))

# Пример использования:
seconds_float = 2.75  # замените это значение на ваше
time_string = _fromat_seconds(seconds_float)
print(time_string)
