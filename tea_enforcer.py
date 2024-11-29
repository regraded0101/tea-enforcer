from typing import Set, Iterable, Dict
import re
import requests
import argparse

class TeaEnforcer:
    def __init__(self):
        self._url_gb = "https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_GB.dic"
        self._url_us = "https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.dic"
        
        self._words_gb = self._download_words(self._url_gb)
        self._words_us = self._download_words(self._url_us)

        self._split_words = " "
        self._split_lines = "\n+"
        self._split_snake_case = "_"
        self._split_CamelCase = "(?<=[a-z]){1}(?=[A-Z]){1}"

        self._split_var_names = f"{self._split_words}|{self._split_lines}|{self._split_snake_case}|{self._split_CamelCase}"

    def _download_words(self, url: str) -> Set[str]:
        response = requests.get(url=url)
        response.raise_for_status()
        content = response.content.decode("utf-8")
        words_list = [word.split('/')[0].lower() for word in content.split("\n")]
        return set(words_list)

    def _read_file(self, python_filepath: str) -> Dict:
        with open(python_filepath, "r") as file:
            file_lines = file.readlines()
        
        return {i+1: re.split(self._split_var_names, line) for i, line in enumerate(file_lines)}

    def _is_american_spelling(
            self,
            word: str, 
            words_gb: Iterable, 
            words_us: Iterable,
        ) -> bool:
        word = word.lower()
        return word in words_us and word not in words_gb
    
    def review_british_spelling(
            self,
            python_filepath
        ):

        file_lines = self._read_file(python_filepath=python_filepath)
        american_spellings = {}

        for line, words in file_lines.items():
            line_american_spellings = [word for word in words if self._is_american_spelling(word, self._words_gb, self._words_us)]
            if line_american_spellings:
                american_spellings[line] = line_american_spellings

        if american_spellings:
            print("American spelling detected!")
            for line, words in american_spellings.items():
                print(f"Line {line}: {'; '.join(words)}")
            return exit(1)
        return exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        nargs="*"
    )
    args = parser.parse_args()
    
    if not args.file:
        exit(0)

    tea_enforcer = TeaEnforcer()
    for file in args.file:
        tea_enforcer.review_british_spelling(file)

if __name__ == "__main__":
    main()
