# Padchest preprocessing
Preprocessing scripts for the PadChest dataset.


## Downloading

1. Download the dataset described by [1], request acess from [the bimcv website](http://bimcv.cipf.es/bimcv-projects/padchest).

2. Follow the preprocessing steps from [Rx-thorax-automatic-captioning](https://github.com/auriml/Rx-thorax-automatic-captioning):

   2.1. Resize each image to 1024x1024px:

        mkdir 1024 ; find . -iname "*.png" | parallel convert -resize "1024x1024^" {} 1024/{}


3. Generate the lists for the dataset. You need to create 3 files. Typically, for split in ['train', 'val', 'test']:

    3.1. 
    3.2. 
    3.3. 

    This can be done with the generate_lists script (e.g.):
    
        python padchest_preprocessing/generate_lists.py --labels Annotations/PADCHEST_chest_x_ray_images_labels_160K_01.02.19.csv  -v

4. Extract features from images.





Refs:

[1] A. Bustos, A. Pertusa, JM. Salinas, M. de la Iglesia. PadChest: A large chest x-ray image dataset with multi-label annotated reports. (Publication Ongoing)


