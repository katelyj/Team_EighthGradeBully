import os
import errno

def assure_directory_path_exists(directory_path):
    '''
    Assure that the given path exists

    Attempts to create the directory on the given path and ignore the error
    if the directory already exist.

    Args:
        directory_path (str): the directory path we want to assure exist

    Returns:

    Raises:
        OSError: Exception preventing the creation of directory but ignoring the case
            where the cause is that the directory already exist
    '''
    try:
        os.makedirs(directory_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
