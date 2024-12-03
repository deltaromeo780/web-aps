import os
import shutil

def normalize(text):
    normalization_dict = {
        "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n",
        "ó": "o", "ś": "s", "ż": "z", "ź": "z"
    }
    
    normalized_text = "".join(normalization_dict.get(char, char) for char in text)
    return "".join(char if char.isalnum() or char.isspace() else "_" for char in normalized_text)

def sort_files(path):
    image_ext = (".jpeg", ".png", ".jpg", ".svg", ".bmp")
    video_ext = (".avi", ".mp4", ".mov", ".mkv")
    document_ext = (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx")
    music_ext = (".mp3", ".ogg", ".wav", ".amr")
    archive_ext = (".zip", ".gz", ".tar", ".rar")

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            dot_position = file.rfind(".")
            file_name = file[0:dot_position]
            file_ext = file[dot_position:]

            if file_ext in image_ext:
                category = "images"

            elif file_ext in video_ext:
                category = "video"

            elif file_ext in document_ext:
                category = "documents"

            elif file_ext in music_ext:
                category = "music"

            elif file_ext in archive_ext:
                category = "archives"

            else:
                category = "other"
            
            target_dir = os.path.join(path, category)
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            new_file_name = normalize(file_name)

            file_name_length = len(new_file_name)
            target_path = os.path.join(target_dir, (new_file_name + file_ext))
            count = 0
            
            if not target_path == file_path:

                while os.path.exists(target_path):
                    count += 1
                    new_file_name = new_file_name[0:file_name_length] + "_" + str(count)
                    target_path = os.path.join(target_dir, (new_file_name + file_ext))
                shutil.move(file_path, target_path)

    
    for root, dirs, files in os.walk(path, topdown=False): # removes empty directories
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                
    print("Success")



path = input("Input path to directory you want to sort e.g: C:/Users/john/Desktop/all_files\nPath: ")

sort_files(path)