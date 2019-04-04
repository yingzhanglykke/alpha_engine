import os
from tempfile import NamedTemporaryFile
import shutil
import csv

from config import ConfigScalingLawTesting


def main():

    file_dir = ConfigScalingLawTesting.data_path
    # file_name = ConfigScalingLawTesting.file_name_test_jforex_two_days
    file_name = ConfigScalingLawTesting.file_name_test_jforex_four_year
    file_read = os.path.join(file_dir, file_name)
    file_write = os.path.join(file_dir, 'copy_'+file_name)

    with open(file_write, 'w', newline='') as csvOutput:
        writer = csv.writer(csvOutput, delimiter=',')
        with open(file_read, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            for row in reader:
                writer.writerow(row[0:2])



if __name__ == '__main__':
    main()