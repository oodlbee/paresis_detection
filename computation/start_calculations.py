import logging
from pathlib import Path
from get_video_symmetries import get_video_symmetries


def main_start(video_file_path:str, markup_file_path:str, save_to_path:str, event=None, queue=None):
    
    # initialize output computation logger
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s/%(funcName)s] - %(levelname)s - %(message)s')

    # initialize computation logger
    comp_logger_folder = Path('computation/comp_loggers').absolute()
    comp_logger = logging.getLogger('comp_logger')
    comp_handler = logging.FileHandler(str(comp_logger_folder / Path('comp_logger.log')), mode='a')
    format = logging.Formatter('%(asctime)s [%(filename)s/%(funcName)s] - %(levelname)s - %(message)s')
    comp_handler.setFormatter(format)
    comp_logger.addHandler(comp_handler)
    comp_logger.setLevel(logging.DEBUG)
    
    # Changing file paths type
    video_file_path = Path(video_file_path)
    markup_file_path = Path(markup_file_path)
    save_to_path = Path(save_to_path)

    get_video_symmetries(video_file_path, markup_file_path, save_to_path, event=event, queue=queue)
    comp_logger.debug('Calculations ended successfully')
    
    

def get_list_of_files(dir_path):
    """Makes a list of strings of file's paths from directiory"""
    list_of_file = Path.iterdir(dir_path)           
    all_files = []
    for file in list_of_file:
        full_path = dir_path.joinpath(file)
        if Path.is_dir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)             
    return all_files


if __name__ == "__main__":
    main_start(
        'application/app_handlers/temp/20180125_Mordashov_1.mp4',
        'application/app_handlers/temp/markup.xlsx',
        'application/app_handlers/temp'
        )