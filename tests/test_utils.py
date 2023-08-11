import os
import sys

def add_src_to_path()->None:
    """
    # Сalling the function at the beginning of the file
    from test_utils import add_src_to_path
    add_src_to_path()
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    src_dir = os.path.join(project_dir, "src")
    sys.path.append(src_dir)