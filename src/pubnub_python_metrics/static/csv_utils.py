import os


def get_csv_file_path(csv_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, f"{csv_name}.csv")
    return csv_path
