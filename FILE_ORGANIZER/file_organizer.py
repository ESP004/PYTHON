import argparse
import os
import shlex
import shutil
import textwrap
import threading

#FILE types
FILE_TYPES = {
    "audio" : [".mp3", ".wav"],
    "images" : [".png", ".gif", ".jpg", ".jpeg"],
    "documents" : [".pdf", ".dox", ".txt", ".xlsx"],
    "videos" : [".mp4", ".mkv", ".mov"],
    "archives" : [".rar", ".tar", ".zip"],
}



#function to organize files by types
def organize_files(directory):

    if not os.path.exists(directory):
        print(f"ERROR: The directory {directory} does not exists")
        return
    
    #Ensure subfolder exists
    for folder in FILE_TYPES:
        folder_path = os.path.join(directory, folder)
        os.makedirs(folder_path, exist_ok=True)

    #function to move files into correct sub folders
    def move_file(file, file_path):
        _,ext =os.path.splitext(file)
        for folder, extensions in FILE_TYPES.items():
            if ext.lower() in extensions:
                destination = os.path.join(directory, folder, file)
                shutil.move(file_path, destination)
                print(f"moved: {file} --> {destination}")

    #create and start thread for each file
    threads = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            thread = threading.Thread(target=move_file, args=(file, file_path))
            threads.append(thread)
            thread.start()
    #weight thread to compute then join them    
    for thread in threads:
        thread.join()
    
    print("\n Files organize sucrssfully......")

def main():
    parser =argparse.ArgumentParser(description=textwrap.dedent('''
FILE ORGANIZER CLI
-------------------------------
Organize file ine a direstory into sub folder by file types.
Supportes types: Images, Documents, Audio, videos, Archives.
'''),
    formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('directory', type=str, help='Path to the directory to organize')
    parser.add_argument('--preview', action='store_true', help='privew changes without moveing files')
    
    args = parser.parse_args()
    if args.preview:
        print(f"\nPrivew: files in '{args.directory}' will be stored")
    else:
        organize_files(args.directory)
    
if __name__ == '__main__':
    main()

