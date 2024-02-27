================================================
Performance Metrics:
================================================
In the base directory, have folders with the PAS WSI name (Ex: JPH1) and in that folder have the following:

PAS WSI
gloms.xml
podocount.xml
podosighter.xml
nuclei.xml
Command to run the script:

'python performance_analysis.py --base_dir base_directory_path --input_list JPH1.svs JPH2.svs'
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
PodoSighter (V1): A cloud-based tool for label-free podocyte detection in renal tissue sections 
=============================================================================================

Podocytes play a crucial role in maintaining the structural and functional integrity of the glomerulus. Several renal diseases like diabetic kidney disease, minimal change disease, glomerulonephritis, etc. lead to podocyte injury, causing their eventual detachment from the glomerular basement membrane. Therefore, quantifying podocyte loss is of high clinical significance, especially in tracking disease progression. The current clinical standard for podocyte detection involves their manual identification from standard periodic acid-Schiff (PAS)-stained renal sections, which are extremely subjective and time consuming. In research practice, these limitations can be overcome by the use of podocyte-specific antibodies like p57, WT1, nephrin, etc., which is expensive and not in routine clinical practice. To address these limitations, we have developed 'PodoSighter', a cloud-based application to identify podocytes from brightfield images of renal tissue sections, stained using the standard clinical stain of PAS counterstained with hematoxylin. Our application framework utilizes state-of-the-art deep learning technique: convolutional neural network (CNN). The PodoSighter pipeline is deployed using HistomicsTK, creating an online, interactive platform enabling multiple users from various locations to quantify podocytes on their respective PAS-stained whole slide images (WSIs). This pipeline not only detects detects podocyte nuclei, but also generates a CSV file containing the podocyte counts, apparent mean nuclear caliper diameter, true mean nuclear caliper diameter, correction factor, and podocyte volume densities estimated using the Wiggins method.

This code has been modified by Darshana Govind to include the PodoSighter pipeline (for automated podocyte detection from PAS-stained renal tissue sections) via Google's deeplab v3+ architecture (https://github.com/tensorflow/models/tree/master/research/deeplab).

**Installation**

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

1 - Register/log in at https://athena.rc.ufl.edu/

2 - Upload your slide and the respective glomerulus annotation file (.xml) via the upload button on the top right corner of the screen

3 - Open your slide in HistomicsUI

4 - On the top right corner of the screen, select the 'Analyses' button, and from the drop down menu, select 'sarderlab/podosighter>V1>PodoSighter_cnn'.

5 - Once the plugin has been selected, a user input section is displayed on the left. For user inputs, follow the instructions below:


**PodoSighter_CNN user inputs**

- **Data Folder**: Select the folder containing the slide and xml annotations.
- **Input PAS whole slide image**: Select the whole slide image (WSI) to be analyzed.
- **Input Glomerular Annotation File**: Select the xml file containing glomerulus annotations (either manually annotated or automatically extracted using the H-AI-L pipeline). 
- **Model**: Select the trained model (for eg. mou_wt1_model.ckpt-50000.data-00000-of-00001).
- **Model chkpt**: Select the latest checkpoint of trained model (for eg. mou_wt1_checkpoint).
- **Model idx**: Select the index file of trained model (for eg. mou_wt1_model.ckpt-50000.index).
- **JSON format podocyte nuclei annotation filename**: Select the name of output (podocyte) json file (for eg. "abc_json").
- **XML format podocyte nuclei annotation filename**: Select the name of output (podocyte) xml file (for eg. "abc_xml").
- **CSV output filename**: Select the name of output csv file containing podocyte metrics (for eg. "abc_csv").

**User parameters for plugins**

Since each WSI is different in terms of staining, imaging, resolution, etc., we provide the option for users to adjust the parameters to generate optimal results for their       respective WSIs. Listed below are the different parameters and their definitions:

- **Tissue thickness**: Enter your tissue thickness (in microns).
- **PAS nuclei intensity threshold**: This parameter selects the threshold to segment hematoxylin stained nuclei (ranging from 0 to 1).
- **Gaussian filter size parameter**: This parameter blurs the PAS image prior to application of threshold.
- **Morphological disc size**: This parameter specifies the disc size of the structuring element to perform morphological opening of segmented nuclei. 
- **Species**: Specify mouse, rat, or human.
- **gpu_id**: Setting this parameter to 0, would enable the code to run on the GPU. (-1 for CPU: not recommended).
- **resolution**: This parameter can be used to specify if the analysis should be done in high resolution (0) or a downsampled (1) version of the WSI to save time. 
- **Size threshold**: This parameter is used to remove unwanted noise from the segmented nuclei.
- **watershed_thre**: This parameter sets the distance parameter for the watershed segmentation of segmented nuclei (ranging from 0 to 1).


Listed below are the parameters we used for our study

+---------------------------+-------------+--------------------+------------------+---------------+-----------------+---------------+--------------------+
| Dataset                   | species     | PASnucleiThreshold | gauss_filt_size  | disc_size     | resolution      | size_thre     | watershed_thre     |
+===========================+=============+====================+==================+===============+=================+===============+====================+
| Mouse WT1 data            | mouse       | 0.3                | 4                | 6             | 0               | 1800          | 0.2                |
+---------------------------+-------------+--------------------+------------------+---------------+-----------------+---------------+--------------------+
| Mouse p57 data            | mouse       | 0.4                | 5                | 4             | 0               | 800           | 0.2                |
+---------------------------+-------------+--------------------+------------------+---------------+-----------------+---------------+--------------------+
| Rat WT1 data              | rat         | 0.5                | 5                | 4             | 0               | 400           | 0.2                |
+---------------------------+-------------+--------------------+------------------+---------------+-----------------+---------------+--------------------+
| Rat p57 data              | rat         | 0.5                | 5                | 4             | 0               | 400           | 0.2                |
+---------------------------+-------------+--------------------+------------------+---------------+-----------------+---------------+--------------------+
| Human autopsy WT1 data    | human       | 0.5                | 5                | 6             | 0               | 400           | 0.2                |
+---------------------------+-------------+--------------------+------------------+---------------+-----------------+---------------+--------------------+
| Human autopsy p57 data    | human       | 0.5                | 5                | 6             | 0               | 400           | 0.2                |
+---------------------------+-------------+--------------------+------------------+---------------+-----------------+---------------+--------------------+
| Human pediatric WT1 data  | human       | 0.4                | 5                | 6             | 0               | 400           | 0.2                |
+---------------------------+-------------+--------------------+------------------+---------------+-----------------+---------------+--------------------+
| Human pediatric p57 data  | human       | 0.4                | 5                | 6             | 0               | 400           | 0.2                |
+---------------------------+-------------+--------------------+------------------+---------------+-----------------+---------------+--------------------+



