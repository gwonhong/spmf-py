"""
Python 3 Wrapper for SPMF
http://www.philippe-fournier-viger.com/spmf

Inspiration from:
https://github.com/fandu/maximal-sequential-patterns-mining
http://forum.ai-directory.com/read.php?5,5510
"""

__author__ = "Lorenz Leitner"
__version__ = "1.4"
__license__ = "GNU GPL v3.0"

import os
import subprocess
import tempfile


class Spmf:
    def __init__(
        self,
        algorithm_name,
        input_direct=None,
        input_type="",  # file, normal_str, text_str, normal_list, text_list
        input_filename="",
        output_filename="spmf-output.txt",
        print_to_stdout=True,
        arguments=[],
        spmf_bin_location_dir=".",
        memory=0,
    ):
        self.executable_dir_ = spmf_bin_location_dir
        self.executable_ = "spmf.jar"

        self.is_exist_executable_ = os.path.isfile(os.path.join(self.executable_dir_, self.executable_))

        if not self.is_exist_executable_:
            self.executable_dir_ = os.path.dirname(os.path.realpath(__file__))
            self.is_exist_executable_ = os.path.isfile(os.path.join(self.executable_dir_, self.executable_))

        if not self.is_exist_executable_:
            raise FileNotFoundError(self.executable_ + " not found. Please use the spmf_bin_location_dir argument.")

        self.agorithm_name_ = algorithm_name
        self.input_file_path_ = self.handle_input(input_type, input_filename, input_direct)
        self.output_file_path_ = output_filename
        self.print_to_stdout_ = print_to_stdout
        self.arguments_ = [str(a) for a in arguments]
        self.memory_ = memory

    def handle_input(self, input_type, input_filename, input_direct):
        if input_type == "":
            raise TypeError("You should specify input_type: file, normal_str, text_str, normal_list or text_list.")
        if input_type == "file":
            if input_filename:
                return input_filename
            else:
                raise TypeError("input_filename is empty. Use input_filename parameter to specify input_filename.")
        elif input_type == "normal_str":
            if type(input_direct) != str:
                raise TypeError("You should input str type for normal_str.")
            else:
                return self.write_temp_input_file(input_direct, ".txt")
        elif input_type == "text_str":
            if type(input_direct) != str:
                raise TypeError("You should input str type for text_str.")
            else:
                return self.write_temp_input_file(input_direct, ".text")
        elif input_type == "normal_list":
            if type(input_direct) != list:
                raise TypeError("You should input str type for normal_list.")
            else:
                seq_spmf = ""
                for seq in input_direct:
                    for item_set in seq:
                        for item in item_set:
                            seq_spmf += f"{item} "
                        seq_spmf += "-1 "
                    seq_spmf += "-2\n"
                return self.write_temp_input_file(seq_spmf, ".txt")
        elif input_type == "text_list":
            if type(input_direct) != list:
                raise TypeError("You should input str type for text_list.")
            else:
                seq_str = ""
                for seq in input_direct:
                    seq_str += seq + ". "
                return self.write_temp_input_file(seq_str, ".text")
        else:
            raise TypeError("input_type must be file, normal_str, text_str, normal_list or text_list.")

    def write_temp_input_file(self, input_text, file_ending):
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.write(bytes(input_text, "UTF-8"))
        name = tf.name
        os.rename(name, name + file_ending)
        return name + file_ending

    def run(self):
        """
        Start the SPMF process
        Calls the Java binary with the previously specified parameters
        """
        subprocess_arguments = ["java"]

        # http://www.philippe-fournier-viger.com/spmf/index.php?link=FAQ.php#memory
        if self.memory_:
            subprocess_arguments.append(f"-Xmx{self.memory_}m")

        subprocess_arguments.extend(
            [
                "-jar",
                os.path.join(self.executable_dir_, self.executable_),
                "run",
                self.agorithm_name_,
                self.input_file_path_,
                self.output_file_path_,
            ]
        )
        subprocess_arguments.extend(self.arguments_)

        proc = subprocess.check_output(subprocess_arguments)
        proc_output = proc.decode()
        if self.print_to_stdout_:
            print(proc_output)
        if "java.lang.IllegalArgumentException" in proc_output:
            raise TypeError("java.lang.IllegalArgumentException")

    def parse_output(self):
        """
        Returns a list of tuples, and each tuple is made of (support, pattern).
        """
        patterns = []
        with open(self.output_file_path_, "r") as f:
            for line in f:
                line = line.strip()
                _line = line.split(" -1 ")
                if _line[-1].startswith("#SUP: "):
                    support = int(_line[-1][6:])
                patterns.append((support, tuple(_line[:-1])))
        return patterns
