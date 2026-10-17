from pathlib import Path
base_dir = str(Path(__file__).resolve().parent / 'data')
Path(base_dir).mkdir(exist_ok=True)
input_file_path = str(Path(base_dir) / 'input.xlsx')
routeplan_input_file_path = str(Path(base_dir) / 'routeplan_input.xlsx')
time_cost_path = str(Path(base_dir) / 'line_time_cost')
add_time_points_path = str(Path(base_dir) / 'add_time_points.xlsx')
routeplan_result_path = str(Path(base_dir) / 'routeplan_result.xlsx')
