import os
import sys
import traceback
from pathlib import Path
import logging.config

import yaml


class WordCount(object):
    """
    This class is used to prints a word count of its contents. It takes file path as an input parameter.
    """
    def __init__(self, abs_file_path):
        self.log = WordCount._setup_logger()
        self.log.info("logging configured")
        self.abs_file_path = abs_file_path
        self.word2occur = {}

    def word_count(self):
        """
        It is used to find the given files word count of its contents. It opens the given file and read line by line
        and calls helper method to find given word and its occurrences. It also uses another helper method to
        sort(descending) the word count dict based on its occurrences.
        :return:
        """
        with open(self.abs_file_path) as inp_file:
            file_cont = inp_file.read()
            self.populate_word_count_dict(file_cont)

        self.display_sorted_word2occur()

    def populate_word_count_dict(self, file_content: str):
        """
        It populates the word count dictionary with its occurrences
        :param file_content: It takes each line as a content.
        :return:
        """
        for word in file_content.split():
            # remove special chars and convert the word into lower case.
            # assumption: Considered case-insensitive words, hence converted into lowercase.
            word = ''.join(e for e in word.lower() if e.isalnum())
            if word in self.word2occur:
                self.word2occur[word] += 1
            else:
                self.word2occur[word] = 1

    def display_sorted_word2occur(self):
        for w in sorted(self.word2occur, key=self.word2occur.get, reverse=True):
            print(w + ': ' + str(self.word2occur[w]))
            self.log.info(w + ': ' + str(self.word2occur[w]))

    @staticmethod
    def setup_logging(filename):
        try:
            with open(filename, 'r') as f:
                cfg = yaml.safe_load(f)

            if cfg is not None:
                logging.config.dictConfig(cfg['logging'])

        except IOError as ioe:
            logging.error(str(ioe))
        except yaml.YAMLError as ymle:
            logging.error(str(ymle))

    @staticmethod
    def _setup_logger():
        """ Setup logging object """
        log_yml = "logging.yml"
        log_file = Path(log_yml)

        if log_file.is_file():
            print("logging.yml exists" + log_file.name)
            WordCount.setup_logging(log_yml)
        else:
            print("logging.yml doesn't exist")
        return logging.getLogger("WORD_COUNT")


if __name__ == "__main__":
    try:
        file_input = str(sys.argv[1])
        print("file_input: " + file_input)

        if os.path.isfile(file_input):
            print(file_input + " exists")
            word_count = WordCount(file_input)
            word_count.word_count()
        else:
            print("Given file path is incorrect. Please provide the correct path.")
            sys.exit(1)
    except OSError as oe:
        print("OSError occurred: " + traceback.format_exc())
    except IndexError as ie:
        print("IndexError occurred: " + traceback.format_exc())
        print("Please provide absolute path of the input file. "
              "For example 'python3 word_count.py /Users/tramasamy/Documents/scripts/python/adaptavist/test_input.txt'")
        sys.exit(1)
    except:
        print("GenericException occurred: " + traceback.format_exc())
        sys.exit(1)
