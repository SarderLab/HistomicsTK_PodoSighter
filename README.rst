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

