# Padchest preprocessing
Preprocessing stages for the PadChest dataset. We assume that we are working under `/home/user/padchest` directory. Modify this conveniently.

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


4. Generate the lists for the dataset. You need to create 3 files. Typically, for split in ['train', 'val', 'test']:

    3.1. *split_list_ids.txt*: Contains the sample ids for each split. 
    
    3.2. *split_list_images.txt*: Contains the path to each image for each split.
    
    3.3. *split_list.txt*:  sample_id \t data_column1 \t ... \t data_columnN.
                            Where data_column are labels (e.g. the reports).

    These lists can be generated with the `generate_lists.py` script (e.g.):
    
     ```
     python ~/smt/software/padchest_preprocessing/padchest_preprocessing/generate_lists.py --root-dir /home/user/DATASETS/padchest/ --labels Annotations/PADCHEST_chest_x_ray_images_labels_160K_01.02.19.csv  -v
     ```
        
4. Extract features from images.

    4.1. Make sure you correclty installed [Mulimodal Keras Wrapper](https://github.com/lvapeab/multimodal_keras_wrapper) and [Keras](https://github.com/keras-team/keras) ([or our version of Keras](https://github.com/MarcBS/keras)).  
    
    4.2. Select the configuration of the extractor in `feature_extraction/config.py`.
    
    4.3. Extract the features!
        
  ```
  python feature_extraction/keras/simple_extractor.py
  ```
    
## TO-DO list.

    * Make `feature_extraction/keras/simple_extractor.py` work in batch.
    * There are some pre-defined splits?
