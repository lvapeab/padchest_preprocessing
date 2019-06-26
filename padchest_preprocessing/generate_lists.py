from __future__ import print_function
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

def parse_args():
    parser = argparse.ArgumentParser("Generate lists indexing the Padchest dataset.")
    parser.add_argument("-r", "--root-dir", required=False, default="./", help="Root directory of the dataset.")
    parser.add_argument("-i", "--image-dir", required=False, default="Images", help="Directory (under --root-dir) containing the dataset images.")
    parser.add_argument("-id", "--image-id", required=False, default="ImageID", help="Name of the field in the csv containing the samples ids.")
    parser.add_argument("-l", "--labels", required=False, default="./labels_csv/PADCHEST_chest_x_ray_images_labels_160K_01.02.19.csv", help="CSV with the dataset labels.")
    parser.add_argument("-sep", "--separator", required=False, default="\t", help="Field separator fields of output files.")
    parser.add_argument("-f", "--fields", required=False, nargs='+', default=['ImageID', 'Report'], help="Fields to store in the output files.")
    parser.add_argument("-s", "--splits", nargs='+', required=False, default=['train', 'val', 'test'], help="Splits to create.")
    parser.add_argument("-fr", "--fraction", nargs='+', required=False, default=[0.6, 0.2, 0.2], help="Fractions of data to (randomly) assign to a split.")
    parser.add_argument("-od", "--output-dir", required=False, default='Annotations', help="Output directory.")
    parser.add_argument("-os", "--output-suffix", required=False, default='_list.txt', help="Output suffix for all splits.")
    parser.add_argument("-v", "--verbose", required=False, action='store_true', default=False, help="Be verbose")
    return parser.parse_args()


def generate_lists(root_dir, image_dir, image_id, labels, separator, fields, splits, fraction, output_dir, output_suffix, verbose):
    """
    TODO
    :param root_dir: Root directory of the dataset.
    :param image_dir:
    :param image_id:
    :param labels:
    :param separator:
    :param fields:
    :param splits:
    :param fraction:
    :param output_annotations:
    :param verbose:
    :return:
    """
    print ("Reading CSV from:", root_dir + '/' + labels)
    padchest_csv = pd.read_csv(root_dir + '/' + labels, header=0, dtype=str)
    relevant_fields = padchest_csv.loc[:, fields]
    relevant_fields['full_path_images'] = root_dir + '/' + image_dir + '/' + padchest_csv.loc[:, image_id]
    relevant_fields['image_ids'] = padchest_csv[image_id].str[:-4]
    print ("Creating splits.")
    if len(fraction) >= 2:
        train, test = train_test_split(relevant_fields, train_size=1.-fraction[-1], test_size=fraction[-1])
        if verbose:
            print ("Test set size:", test.shape)
        split_name = splits[-1]
        test[fields].to_csv(output_dir + '/' + split_name  + output_suffix, sep=separator, header=0, index=False)
        test['full_path_images'].to_csv(output_dir + '/' + split_name + '_list_images.txt', sep=separator, header=0, index=False)
        test['image_ids'].to_csv(output_dir + '/' + split_name + '_list_ids.txt', sep=separator, header=0, index=False)
        if len(fraction) == 3:
            train, dev = train_test_split(relevant_fields, train_size=fraction[0], test_size=fraction[1])
            if verbose:
                print("Dev set size:", dev.shape)
            split_name = splits[1]
            dev[fields].to_csv(output_dir + '/' + split_name + output_suffix, sep=separator, header=0, index=False)
            dev['full_path_images'].to_csv(output_dir + '/' + split_name + '_list_images.txt', sep=separator, header=0, index=False)
            dev['image_ids'].to_csv(output_dir + '/' + split_name + '_list_ids.txt', sep=separator, header=0, index=False)
    else:
        train = relevant_fields
    if verbose:
        print("Train set size:", train.shape)
    split_name = splits[0]
    train[fields].to_csv(output_dir + '/' + split_name + output_suffix, sep=separator, header=0, index=False)
    train['full_path_images'].to_csv(output_dir + '/' + split_name + '_list_images.txt', sep=separator, header=0, index=False)
    train['image_ids'].to_csv(output_dir + '/' + split_name + '_list_ids.txt', sep=separator, header=0, index=False)
    print("Done")
    return


if __name__ == "__main__":
    args = parse_args()
    assert len(args.splits) == len(args.fraction), 'You should provide the same number of splits than fractions of data.'

    generate_lists(args.root_dir, args.image_dir, args.image_id, args.labels, args.separator, args.fields, args.splits, args.fraction, args.output_dir, args.output_suffix, args.verbose)
