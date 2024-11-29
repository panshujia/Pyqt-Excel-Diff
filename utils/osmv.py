import os
def find_files_starting_with(path, prefix, file_extension=None):
    # 获取指定路径下的所有文件和文件夹
    files = os.listdir(path)
    
    # 筛选出以指定前缀开头的文件，且文件扩展名符合要求
    matching_files = [
        file
        #os.path.splitext(file)[0]
        for file in files
        if file.startswith(prefix) and os.path.isfile(os.path.join(path, file)) and (file.endswith(file_extension) if file_extension else True)
    ]
    
    return matching_files