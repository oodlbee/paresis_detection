import sys
import os
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

sys.path.append(str(Path(__file__).parent.parent))
from computation.start_calculations import main_start



if __name__ == '__main__':
    # clear computation logger
    with open(Path('computation\\comp_loggers\\comp_logger.log'), 'w'):
        pass
    video_folder = Path('E:\\projects\\paresis_emg\\videos')
    markup_folder = Path('E:\\projects\\paresis_emg\\markup')
    save_folder = Path('E:\\projects\\paresis_emg\\results_by_3d_old_eyebrow')

    args = []
    for video in video_folder.iterdir():
        video_name = video.stem
        for markup in markup_folder.iterdir():
            markup_name = markup.stem.split('_markup')[0]
            if video_name == markup_name:
                save_to_path = save_folder/Path(video).stem
                save_to_path.mkdir(parents=True, exist_ok=True)
                args.append((str(video), str(markup), str(save_to_path)))
                continue
    pool = Pool(os.cpu_count() - 1)
    pool = Pool(1)
    pool.starmap(main_start, args)

# for video in tqdm(video_markup_dict):
#     print(video, video_markup_dict[video])
#     save_to_path = save_folder/Path(video).stem
#     print(save_to_path)
#     save_to_path.mkdir(parents=True, exist_ok=True)
#     main_start(video, video_markup_dict[video], str(save_to_path))