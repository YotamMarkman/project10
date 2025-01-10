import sys
import re
from os import listdir
from os.path import isfile, isdir
from CompilationEngine import CompilationEngine

INVALID_ARGS_MESSAGE = "Invalid input file or directory provided."
EXPECTED_ARG_COUNT = 2
OUTPUT_EXTENSION = ".xml"
INPUT_EXTENSION = r"\.jack$"
INPUT_PATTERN = re.compile(INPUT_EXTENSION)
COMMENT_PATTERN = "//.*$"

class JackAnalyzer:
    """
    JackAnalyzer module for handling .jack file analysis and CompilationEngine execution.
    """
    @staticmethod
    def get_files(input_args):
        """
        :param input_args: Arguments passed to the program.
        :return: A list of .jack file paths.
        """
        file_paths = []
        if len(input_args) == EXPECTED_ARG_COUNT:
            if isfile(input_args[1]) and INPUT_PATTERN.match(input_args[1]):
                file_paths.append(input_args[1])
            elif isdir(input_args[1]):
                for filename in listdir(input_args[1]):
                    if INPUT_PATTERN.match(filename):
                        file_paths.append(f"{input_args[1]}/{filename}")
            return file_paths
        else:
            print(INVALID_ARGS_MESSAGE)
            sys.exit()

    @staticmethod
    def generate_output_path(input_path):
        """
        :param input_path: Path to the source .jack file.
        :return: Corresponding output .xml file path.
        """
        return re.sub(INPUT_EXTENSION, OUTPUT_EXTENSION, input_path)

if __name__ == "__main__":
    """
    Main driver for the JackAnalyzer program. Processes each .jack file using CompilationEngine.
    """
    source_files = JackAnalyzer.get_files(sys.argv)
    for source_path in source_files:
        engine_instance = CompilationEngine(source_path, JackAnalyzer.generate_output_path(source_path))
        engine_instance.compileClass()
