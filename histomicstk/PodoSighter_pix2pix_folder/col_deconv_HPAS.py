import matplotlib.pyplot as plt

from skimage import data
from skimage.color import rgb2hed
from matplotlib.colors import LinearSegmentedColormap

def col_deconv_HPAS(ihc_rgb):
    
    # Create an artificial color close to the original one
    cmap_hema = LinearSegmentedColormap.from_list('mycmap', ['white', 'navy'])
    cmap_dab = LinearSegmentedColormap.from_list('mycmap', ['white',
                     'saddlebrown'])
    cmap_eosin = LinearSegmentedColormap.from_list('mycmap', ['darkviolet',
                       'white'])
    
    ihc_hed = rgb2hed(ihc_rgb)
    
    H_deconv = ihc_hed[:, :, 0]
    
    return H_deconv
