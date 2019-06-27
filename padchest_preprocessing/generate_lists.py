from __future__ import print_function
import argparse
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)


def file_exists(file):
    return os.path.isfile(file)


def parse_args():
    parser = argparse.ArgumentParser("Generate lists indexing the Padchest dataset.")
    parser.add_argument("-r", "--root-dir", required=False, default="./", help="Root directory of the dataset.")
    parser.add_argument("-i", "--image-dir", required=False, default="Images", help="Directory (under --root-dir) containing the dataset images.")
    parser.add_argument("-id", "--image-id", required=False, default="ImageID", help="Name of the field in the csv containing the samples ids.")
    parser.add_argument("-l", "--labels", required=False, default="./labels_csv/PADCHEST_chest_x_ray_images_labels_160K_01.02.19.csv", help="CSV with the dataset labels.")
    parser.add_argument("-sep", "--separator", required=False, default="\t", help="Field separator fields of output files.")
    parser.add_argument("-f", "--fields", required=False, nargs='+', default=['ImageID', 'Report'], help="Fields to store in the output files.")
    parser.add_argument("-s", "--splits", nargs='+', required=False, default=['train', 'val', 'test'], help="Splits to create.")
    parser.add_argument("-fr", "--fraction", nargs='+', required=False, type=float, default=[0.6, 0.2, 0.2], help="Fractions of data to (randomly) assign to a split.")
    parser.add_argument("-od", "--output-dir", required=False, default='Annotations', help="Output directory.")
    parser.add_argument("-os", "--output-suffix", required=False, default='_list.txt', help="Output suffix for all splits.")
    parser.add_argument("-v", "--verbose", required=False, action='store_true', default=False, help="Be verbose")
    return parser.parse_args()


def generate_lists(root_dir, image_dir, image_id, labels, separator, fields, splits, fraction, output_dir, output_suffix, verbose):
    """
    Generate the list files required for working with an image dataset.
    :param root_dir: Root directory of the dataset.
    :param image_dir: Directory where the image files are stored (under root_dir).
    :param image_id: Name of the field in the csv containing the samples ids.
    :param labels: CSV with the dataset labels.
    :param separator: Field separator fields of output files.
    :param fields: Fields to store in the output files.
    :param splits: Splits to create. Typically, ['train', 'val', 'test'].
    :param fraction: Fractions of data to (randomly) assign to a split.
    :param output_dir: Output directory.
    :param output_suffix: Output suffix for all splits.
    :param verbose: Be verbose
    :return:
    """
    print("Reading CSV from:", root_dir + '/' + labels)
    padchest_csv = pd.read_csv(root_dir + '/' + labels, header=0, dtype=str)
    original_shape = padchest_csv.shape
    padchest_csv['full_path_images'] = root_dir + '/' + image_dir + '/' + padchest_csv.loc[:, image_id]

    existing_padchest = padchest_csv.loc[lambda padchest_csv: map(lambda x: file_exists(x), padchest_csv['full_path_images'])]
    existing_shape = existing_padchest.shape
    if original_shape[0] != existing_shape[0]:
        logger.warning('There are %d missing images!' % (original_shape[0] - existing_shape[0]))
    relevant_fields = existing_padchest.loc[:, fields]
    relevant_fields['full_path_images'] = existing_padchest['full_path_images']
    relevant_fields['image_ids'] = existing_padchest[image_id]

    print("Creating splits.")
    if len(fraction) >= 2:
        train, test = train_test_split(relevant_fields, train_size=1. - fraction[-1], test_size=fraction[-1])
        if verbose:
            print("Test set size:", test.shape)
        split_name = splits[-1]
        test[fields].to_csv(root_dir + '/' + output_dir + '/' + split_name + output_suffix, sep=separator, header=0, index=False)
        test['full_path_images'].to_csv(root_dir + '/' + output_dir + '/' + split_name + '_list_images.txt', sep=separator, header=0, index=False)
        test['image_ids'].to_csv(root_dir + '/' + output_dir + '/' + split_name + '_list_ids.txt', sep=separator, header=0, index=False)
        if len(fraction) == 3:
            train, dev = train_test_split(relevant_fields, train_size=fraction[0], test_size=fraction[1])
            if verbose:
                print("Dev set size:", dev.shape)
            split_name = splits[1]
            dev[fields].to_csv(root_dir + '/' + output_dir + '/' + split_name + output_suffix, sep=separator, header=0, index=False)
            dev['full_path_images'].to_csv(root_dir + '/' + output_dir + '/' + split_name + '_list_images.txt', sep=separator, header=0, index=False)
            dev['image_ids'].to_csv(root_dir + '/' + output_dir + '/' + split_name + '_list_ids.txt', sep=separator, header=0, index=False)
    else:
        train = relevant_fields
    if verbose:
        print("Train set size:", train.shape)
    split_name = splits[0]
    train[fields].to_csv(root_dir + '/' + output_dir + '/' + split_name + output_suffix, sep=separator, header=0, index=False)
    train['full_path_images'].to_csv(root_dir + '/' + output_dir + '/' + split_name + '_list_images.txt', sep=separator, header=0, index=False)
    train['image_ids'].to_csv(root_dir + '/' + output_dir + '/' + split_name + '_list_ids.txt', sep=separator, header=0, index=False)
    print("Done")
    return


if __name__ == "__main__":
    args = parse_args()
    assert len(args.splits) == len(args.fraction), 'You should provide the same number of splits than fractions of data.'

    generate_lists(args.root_dir, args.image_dir, args.image_id, args.labels, args.separator, args.fields, args.splits, args.fraction, args.output_dir, args.output_suffix, args.verbose)
