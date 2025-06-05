import os
import shutil


def copy_static_to_public(src, dest):
    print("Deleting public directory...")
    shutil.rmtree(dest, ignore_errors=True)
    os.mkdir(dest)
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory '{src}' does not exist.")
    print("Copying static files to public directory...")
    def copy_tree(src, dest):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            print(f"Copying {s} --> {d}")
            if os.path.isfile(s):
                shutil.copy(s, d)
                continue
            os.makedirs(d, exist_ok=True)
            copy_tree(s, d)
    return copy_tree(src, dest)