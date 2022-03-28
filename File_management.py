import shutil
import glob
import os


# Move downloaded files
def move_files(download_dir, project_directory):
    os.mkdir(project_directory)  # Create the directory
    os.chdir(download_dir)
    for downloaded_files in glob.glob("*geo_jpg*.zip"):  # Specify the files. jpegs in this case
        shutil.move(downloaded_files, project_directory)
    print(f"Files moved to {project_directory}.")
