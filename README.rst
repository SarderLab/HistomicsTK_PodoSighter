================================================
HistomicsTK |build-status| |codecov-io| |gitter|
================================================

.. |build-status| image:: https://travis-ci.org/DigitalSlideArchive/HistomicsTK.svg?branch=master
    :target: https://travis-ci.org/DigitalSlideArchive/HistomicsTK
    :alt: Build Status

.. |codecov-io| image:: https://codecov.io/github/DigitalSlideArchive/HistomicsTK/coverage.svg?branch=master
    :target: https://codecov.io/github/DigitalSlideArchive/HistomicsTK?branch=master
    :alt: codecov.io

.. |gitter| image:: https://badges.gitter.im/DigitalSlideArchive/HistomicsTK.svg
   :target: https://gitter.im/DigitalSlideArchive/HistomicsTK?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
   :alt: Join the chat at https://gitter.im/DigitalSlideArchive/HistomicsTK

`HistomicsTK`_ is a Python package for the analysis of digital pathology images. It can function as a stand-alone library, or as a Digital Slide Archive plugin that allows users to invoke image analysis jobs through HistomicsUI. The functionality offered by HistomicsTK can be extended using `slicer cli web <https://github.com/girder/slicer_cli_web>`__ which allows developers to integrate their image analysis algorithms into DSA for dissemination through HistomicsUI. 

=============================================================================================
PodoSighter: A cloud-based tool for label-free podocyte detection in renal tissue sections 
=============================================================================================

Podocytes play a crucial role in maintaining the structural and functional integrity of the glomerulus. Several renal diseases like diabetic kidney disease, minimal change disease, glomerulonephritis, etc. lead to podocyte injury, causing their eventual detachment from the glomerular basement membrane. Therefore, quantifying podocyte loss is of high clinical significance, especially in tracking disease progression. The current clinical standard for podocyte detection involves their manual identification from standard periodic acid-Schiff (PAS)-stained renal sections, which are extremely subjective and time consuming. In research practice, these limitations can be overcome by the use of podocyte-specific antibodies like p57, WT1, nephrin, etc., which is expensive and not in routine clinical practice. To address these limitations, we have developed 'PodoSighter', a cloud-based application to identify podocytes from brightfield images of renal tissue sections, stained using the standard clinical stain of PAS counterstained with hematoxylin. Our application framework encompasses two independent pipleines, utilizing two state-of-the-art deep learning techniques: convolutional neural network (CNN) and generative adversarial network (GAN). The PodoSighter pipeline is deployed as two independent plugins (PodoSighter_CNN and PodoSighter_pix2pix), using HistomicsTK, creating an online, interactive platform enabling multiple users from various locations to quantify podocytes on their respective PAS-stained whole slide images (WSIs). 

This code has been modified by Darshana Govind to include the PodoSighter pipeline (for automated podocyte detection from PAS-stained renal tissue sections) via Google's deeplab v3+ architecture (https://github.com/tensorflow/models/tree/master/research/deeplab) and the pix2pix conditional GAN developed by Isola et al (https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).

Installation

HistomicsTK can be used in two ways:

- **As a pure Python package**: enables application of image analysis algorithms to data independent of the `Digital Slide Archive`_ (DSA). HistomicsTK provides a collection of fundamental algorithms for tasks such as color normalization, color deconvolution, nuclei segmentation, and feature extraction. Read more about these capabilities here:  `api-docs <https://digitalslidearchive.github.io/HistomicsTK/api-docs.html>`__ and `examples <https://digitalslidearchive.github.io/HistomicsTK/examples.html>`__ for more information.
  
  **Installation instructions on Linux:**
  
  *To install HistomicsTK using PyPI*:: 
  
  $ python -m pip install histomicstk
  
  *To install HistomicsTK from source*::
  
  $ git clone https://github.com/DigitalSlideArchive/HistomicsTK/
  $ cd HistomicsTK/
  $ python -m pip install setuptools-scm Cython>=0.25.2 scikit-image==0.15.0 cmake>=0.6.0 numpy>=1.12.1
  $ python -m pip install -e .

HistomicsTK uses the `large_image`_ library to read content from whole-slide and microscopy image formats. Depending on your exact system, installing the necessary libraries to support these formats can be complex.  There are some non-official prebuilt libraries available for Linux that can be included as part of the installation by specifying ``pip install histomicstk --find-links https://girder.github.io/large_image_wheels``. Note that if you previously installed HistomicsTK or large_image without these, you may need to add ``--force-reinstall --no-cache-dir`` to the ``pip install`` command to force it to use the find-links option.

The system version of various libraries are used if the ``--find-links`` option is not specified.  You will need to use your package manager to install appropriate libraries (on Ubuntu, for instance, you'll need ``libopenslide-dev`` and ``libtiff-dev``).
  
**To install from source on Windows**:
  
1- Run the following::
  
$ pip install large-image
$ pip install cmake
$ git clone https://github.com/DigitalSlideArchive/HistomicsTK/
$ cd HistomicsTK/
$ python -m pip install setuptools-scm Cython>=0.25.2 scikit-build>=0.8.1 cmake>=0.6.0 numpy>=1.12.1
  
2- Run ``pip install libtiff``
  
3- Replace ``large-image[sources]`` with ``large-image[pil,tiff]`` in ``setup.py``.
  
4- Install Visual Studio 15 2017 `Community Version <https://my.visualstudio.com/Downloads?q=visual%20studio%202017&wt.mc_id=o~msft~vscom~older-downloads>`_ 
  
5- Install C++ build tools. Under Tools > Get Tools and Features ... > Desktop Development with C++, ensure that the first 8 boxes are checked.

6- Run this::
  
$ python -m pip install -e .
$ pip install girder-client

--------------------------------
Running the PodoSighter plugin
--------------------------------

In order to run the PodoSighter plugin on your PAS-stained renal section, follow the following steps:

1 - Upload your slide and the respective glomerulus annotation file (.xml) via the upload button on the top right corner of the screen

2 - Open the slide in HistomicsUI

3 - On the top right corner of the screen, select the analysis button, and from the drop down menu, select darshanagovind/histo19_feb2021>latest>PodoSighter_cnn or darshanagovind/histo19_feb2021>latest>PodoSighter_pix2pix, depending on which pipeline (CNN or pix2pix) you would like to use.

4 - Once the plugin has been selected, a user input section is displayed on the left.


**PodoSighter_CNN**

- **Data Folder**: Select the folder containing the slide and xml annotations
- **Input Image**: Select the whole slide image (WSI) to be analyzed
- **Input Annotation File 1**: Select the xml file containing glomerulus annotations (either manually annotated or automatically extracted using our HAIL pipeline (...) 
- **Model**:
- **Model chkpt**:
- **Model idx**:
- **Output Annotation File 1**:
- **Output Annotation File 2**:


**PodoSighter_pix2pix**

- **Data Folder**: Select the folder containing the slide and xml annotations
- **Input Image**: Select the whole slide image (WSI) to be analyzed
- **Input Annotation File 1**: Select the xml file containing glomerulus annotations (either manually annotated or automatically extracted using our HAIL pipeline (...) 
- **Model**:
- **Model chkpt**:
- **Model idx**:
- **Output Annotation File 1**:
- **Output Annotation File 2**:



**User parameters for both plugins**

Since each WSI is different in terms of staining, imaging, resolution, etc., we provide the option for users to adjust the parameters to generate optimal results for their       respective WSIs. 
Listed below are the different parameters and their definitions:

- **Data Folder**: Select the folder containing the slide and xml annotations
- **Input Image**: Select the whole slide image (WSI) to be analyzed
- **Input Annotation File 1**: Select the xml file containing glomerulus annotations (either manually annotated or automatically extracted using our HAIL pipeline (...) 
- **Model**:
- **Model chkpt**:
- **Model idx**:
- **Output Annotation File 1**:
- **Output Annotation File 2**:


    Listed below are the parameters we used for our study:    
    Dataset                 | species  | PASnucleiThreshold | gauss_filt_size | disc_size | resolution | size_thre | watershed_thre 
    ----------------------  | -------- | ----------------   | --------------- | ----------| ------------------ | ----------------
    Mouse WT1 data          | mouse    | Content Cell       | Content Cell    |  Cell    |  Cell       | Content Cell    
    Mouse p57 data          | mouse    | Content Cell       | Content Cell    |  Cell    |  Cell       | Content Cell    
    Rat WT1 data            | rat      | Content Cell       | Content Cell    |  Cell    |  Cell       | Content Cell        
    Rat p57 data            | rat      | Content Cell       | Content Cell    |  Cell    |  Cell       | Content Cell    
    Human autopsy WT1 data  | human    | Content Cell       | Content Cell    |  Cell    |  Cell       | Content Cell    
    Human autopsy p57 data  | human    | Content Cell       | Content Cell    |  Cell    |  Cell       | Content Cell    
    Human pediatric WT1 data| human    | Content Cell       | Content Cell    |  Cell    |  Cell       | Content Cell    
    Human pediatric p57 data| human    | Content Cell       | Content Cell    |  Cell    |  Cell       | Content Cell    
