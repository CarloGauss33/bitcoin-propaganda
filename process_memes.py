import random
import time
import os

class Meme:
    def __init__(self, path) -> None:
        self.filename, self.file_extension = os.path.splitext(path)
        self.path = path
        self.last_opened = None
        self.times_opened = 0

    def open(self) -> None:
        self.last_opened = os.path.getmtime(self.path)
        self.times_opened += 1


class MemeManager:
    def __init__(self, folder_path, state_file) -> None:
        self.path = folder_path
        self.state_file = state_file
        self.memes = []
        self.load_state()
        self.load_new_memes()

    def get_random_meme(self) -> Meme:
        ONE_WEEK = 60 * 60 * 24 * 7
        memes = [ meme for meme in self.memes if meme.last_opened is None or meme.last_opened < time.time() - ONE_WEEK ]

        if len(memes) == 0:
            return random.choice(self.memes)

        return random.choice(memes)

    def load_state(self) -> None:
        if not os.path.exists(self.state_file):
            open(self.state_file, "w").close()
            return

        with open(self.state_file, "r") as f:
            for line in f:
                filename, path, times_opened, last_opened = line.split(",")
                times_opened = int(times_opened)
                last_opened = last_opened.strip()
                last_opened = float(last_opened) if last_opened != "None" else None
                self.memes.append(self.load_meme(path, times_opened, last_opened))

    def save_state(self) -> None:
        with open(self.state_file, "w") as f:
            for meme in self.memes:
                f.write(f"{meme.filename},{meme.path},{meme.times_opened},{meme.last_opened}\n")

    def load_new_memes(self) -> None:
        for filename in os.listdir(self.path):
            path = os.path.join(self.path, filename)
            if os.path.isfile(path) and not self.meme_exists(path):
                self.memes.append(self.load_meme(path))

    def load_meme(self, path, times_opened=0, last_opened=None) -> Meme:
        meme = Meme(path)
        meme.times_opened = times_opened
        meme.last_opened = last_opened if last_opened else None
        return meme

    def meme_exists(self, path) -> bool:
        for meme in self.memes:
            if meme.path == path:
                return True
        return False

if __name__ == "__main__":
    memes = MemeManager("memes", "data/memes.csv")
    memes.save_state()
    print("Memes loaded: ", len(memes.memes))