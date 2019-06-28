# Padchest preprocessing

 ![Compatibility](https://img.shields.io/badge/Python-2.7%2F3.6-blue.svg) [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/lvapeab/nmt-keras/blob/master/LICENSE)

Preprocessing stages for the PadChest dataset. 

We assume that we are working under `/home/user/padchest` directory. Modify this conveniently.

1. Download the dataset described by [Bustos et al., 2019](https://arxiv.org/abs/1901.07441). Request acess from [the bimcv website](http://bimcv.cipf.es/bimcv-projects/padchest).

2. Follow the preprocessing steps from [Rx-thorax-automatic-captioning](https://github.com/auriml/Rx-thorax-automatic-captioning):

   2.1. Resize each image to 1024x1024px:

        mkdir 1024 ; find . -iname "*.png" | parallel convert -resize "1024x1024^" {} 1024/{}

3. *General structure*: We will organize the dataset in 3 folders:

    3.1. `Annotations`: Contains all the non-image related information. E.g. Captions, labels, lists containing image/feature paths for each split, etc.
    
    3.2. `Images`: Contains the raw images from the dataset (conveniently resized).
    
    3.3. `Features`: Contains the features extracted for the images.

4. Following this structure, lets organize our folders:

    4.1. Create the directories: 
      
      ``mkdir Features Images Annotations``
      
    4.2. Put the padchest csv into the Annotations folder: 
      
      ``cp PADCHEST_chest_x_ray_images_labels_160K_01.02.19.csv Annotations``
    
    4.3. Move all (resized) images to the Images folder: 
      
      ``for folder in `seq 54` ; do mv ${folder}/1024/* Images; done``


5. Generate the lists for the dataset. You need to create 3 files. Typically, for split in ['train', 'val', 'test']:

    5.1. *split_list_ids.txt*: Contains the sample ids for each split. 
    
    5.2. *split_list_images.txt*: Contains the path to each image for each split.
    
    5.3. *split_list.txt*:  sample_id \t data_column1 \t ... \t data_columnN.
                            Where data_column are labels (e.g. the reports).

    These lists can be generated with the `generate_lists.py` script. For example, for using a 96% of the dataset for training (142k samples), a 2% for development (~3k samples) and a 8% for testing (~13k samples), execute: 
     ```
     python padchest_preprocessing/generate_lists.py --root-dir /home/user/DATASETS/padchest/ --labels Annotations/PADCHEST_chest_x_ray_images_labels_160K_01.02.19.csv --fraction 0.9 0.02 0.08 -v
     ```
        
6. Extract features from images.

    6.1. Make sure you correclty installed [Mulimodal Keras Wrapper](https://github.com/lvapeab/multimodal_keras_wrapper) and [Keras](https://github.com/keras-team/keras) ([or our version of Keras](https://github.com/MarcBS/keras)).  
    
    6.2. Select the configuration of the extractor in `feature_extraction/config.py`.
    
    6.3. Extract the features!
      ```
      python padchest_preprocessing/eature_extraction/keras/simple_extractor.py
      ```


7. Generate a list pointing to the extracted features: `split_list_features.txt`. Note that we also want to remove the MIME extension from the features, so we call this scrpit with the option  --replace-extension 4:  
```
python padchest_preprocessing/generate_feature_lists.py --root-dir /home/lvapeab/DATASETS/padchest --features-dir Features/padchest_NASNetLarge/ --features NASNetLarge --lists-dir Annotations --extension .npy --replace-extension 4
```

        
        
8. Retrieve only the captions from split_list.txt:       
```
bash padchest_preprocessing/process_captions.sh /home/lvapeab/DATASETS/padchest/Annotations _list.txt captions
```



9. Profit! This file structure can be directly applied on [interactive-keras-captioning](https://github.com/lvapeab/interactive-keras-captioning).


## TO-DO list.

    * Make `feature_extraction/keras/simple_extractor.py` work in batch.
    * There are some pre-defined splits?
