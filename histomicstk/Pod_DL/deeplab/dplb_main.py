import os
import shutil
import glob
import random


#''' Block: Create Train and val (10%) folder random split after augmentation'''
#'''============================================================'''
#MainfolderlocationImages = '/hdd/d8/dplb/PC1/PodCNN1/Imagesnoaug'  
#Mainfolderlocationlabels = '/hdd/d8/dplb/PC1/PodCNN1/labelsnoaug'  
#
#path = MainfolderlocationImages + '/train/'
#totalNumber_of_images_augmented = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
#
#Numval = int(round(totalNumber_of_images_augmented * .10))
#
#print('Creating val folder for Images and labels...')  
#valfolderIm = MainfolderlocationImages +'/val/'
#valfolderlab = Mainfolderlocationlabels + '/val/'
#
#if not os.path.exists(valfolderIm):
#    os.makedirs(valfolderIm)
#if not os.path.exists(valfolderlab):
#    os.makedirs(valfolderlab)
#
#dstA = MainfolderlocationImages + '/train/'
#dstB = Mainfolderlocationlabels + '/train/'

#endstyleA = '*.png'
#charsToremoveA = 4# i.e. if 4_5glom.png, remove last 8 to get 4_5 

#to_be_moved = random.sample(glob.glob(dstA+endstyleA), Numval)

#for f in to_be_moved:
#    print(f)
#    imname = os.path.basename(f)
#    patchname = imname[:-charsToremoveA]
#    print(patchname)
#    shutil.move((dstA+patchname+'.png'), valfolderIm)    
#    shutil.move((dstB+patchname+'.png'), valfolderlab)
    





#This block didnt work
#cmd1 = "export PYTHONPATH=$PYTHONPATH:/home/d8/dplb/research/:/home/d8/dplb/research/slim"
#os.system(cmd1)

#cmd2 = "python3.5 augmentImgs.py"
#os.system(cmd2)





#
#
#'''Transferring/copying train/test set'''
#MainDataLocation = "/hdd/d8/dplb/Main_Data/"
#setname = "all_wt1"
#
#trIm_location = "/hdd/d8/dplb/PC1/PodCNN1/Images/train/"
#tr_lab_location = "/hdd/d8/dplb/PC1/PodCNN1/labels/train/"
#
#srcholdoutPAS1 = MainDataLocation + "training/"+setname+"_images/" 
#dstholdoutPAS1 = trIm_location
#srcholdoutIF1 = MainDataLocation +"training/"+setname+"_labels/" 
#dstholdoutIF1 = tr_lab_location
#
#if not os.path.exists(dstholdoutPAS1):
#    os.makedirs(dstholdoutPAS1)
#if not os.path.exists(dstholdoutIF1):
#    os.makedirs(dstholdoutIF1)
#
#for f in glob.glob(srcholdoutPAS1+ '*.png'):
#    print(f)
#    shutil.copy(f, dstholdoutPAS1)           
#for f in glob.glob(srcholdoutIF1+ '*.png'):
#    print(f)
#    shutil.copy(f, dstholdoutIF1) 
#
#
#teIm_location = "/hdd/d8/dplb/PC1/PodCNN1/Images/val/"
#te_lab_location = "/hdd/d8/dplb/PC1/PodCNN1/labels/val/"
#
#srcholdoutPAS = MainDataLocation + "testing/"+setname+"_images/" 
#dstholdoutPAS = teIm_location
#srcholdoutIF = MainDataLocation +"testing/"+setname+"_labels/" 
#dstholdoutIF = te_lab_location
#
#if not os.path.exists(dstholdoutPAS):
#    os.makedirs(dstholdoutPAS)
#if not os.path.exists(dstholdoutIF):
#    os.makedirs(dstholdoutIF)
#
#for f in glob.glob(srcholdoutPAS+ '*.png'):
#    print(f)
#    shutil.copy(f, dstholdoutPAS)           
#for f in glob.glob(srcholdoutIF+ '*.png'):
#    print(f)
#    shutil.copy(f, dstholdoutIF) 
#
##--------
#
#
#cmd3 = "bash ./datasets/convert_pqr.sh"
#os.system(cmd3)


cmd4 = "python3.5 train.py \
    --logtostderr \
    --training_number_of_steps=50000 \
    --learning_rate_decay_step=500 \
    --train_split=\"train\" \
    --base_learning_rate=0.0001 \
    --adan_learning_rate=0.0001 \
    --model_variant=\"xception_65\" \
    --atrous_rates=6 \
    --atrous_rates=12 \
    --atrous_rates=18 \
    --output_stride=16 \
    --decoder_output_stride=4 \
    --train_crop_size=\"256,256\" \
    --train_batch_size=1 \
    --dataset=\"PC1\" \
    --Fine_tune_batch_norm=False \
    --tf_initial_checkpoint=\"/hdd/d8/dplb/xception/model.ckpt\" \
    --Initialize_last_layer = False \
    --Last_layers_contain_logits_only = True \
    --train_logdir=\"./models/train_log\" \
    --dataset_dir=\"/hdd/d8/dplb/PC1/tfrecord\""
os.system(cmd4)  

cmd5 = "python3 vis.py \
    --logtostderr \
    --vis_split=\"val\" \
    --model_variant=\"xception_65\" \
    --atrous_rates=6 \
    --atrous_rates=12 \
    --atrous_rates=18 \
    --output_stride=16 \
    --decoder_output_stride=4 \
    --vis_crop_size=\"1200,1200\" \
    --max_number_of_iterations=1 \
    --dataset=\"PC1\" \
    --checkpoint_dir=\"./models/train_log\" \
    --vis_logdir=\"./models/vis_log\" \
    --dataset_dir=\"/hdd/d8/dplb/PC1/tfrecord\""
os.system(cmd5)  