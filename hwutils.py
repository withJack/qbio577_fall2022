# useful libraries to import

import pandas as pd
import numpy as np
import sklearn.decomposition
import matplotlib.pyplot as plt
import seaborn as sns
from more_itertools import locate

def plot_pca(pca , 
             bigwig_metadata=None,
             metadata_label_column=None, 
             alpha=0.5, 
             lw=0, 
             figsize=(10,8),
             label_display=False,
             filter_label_column=False,
             filterby=False,
             showonly_column=False,
             showonly=False,
             showlabels=True,
             ax = None, i = None, ax_col_size=6, ax_row_size=6):
    
    """ 
    Skeleton for plotting PCA and annotating the plot. 
    Can be modified/extended to answer various questions.
    """
    
    plt.figure(figsize=figsize)

    if metadata_label_column is not None:
        if bigwig_metadata is None: 
            raise ValueError("must provide metadata table to label by a metadata column") 
        labels = [bigwig_metadata.query(
                    "`File accession`==@ file_accession ").loc[:,metadata_label_column].values[0]
                  for file_accession in pca.feature_names_in_]
        le = sklearn.preprocessing.LabelEncoder()
        le.fit(labels)
        labels_transformed = le.transform(labels)


        if filterby is not False:
            labels_filter = [bigwig_metadata.query(
                        "`File accession`==@ file_accession ").loc[:,filter_label_column].values[0]
                        for file_accession in pca.feature_names_in_]
            filter_idx = list(locate(labels_filter, lambda x: x == filterby))

            if showonly is not False:
                labels_show = [bigwig_metadata.query(
                            "`File accession`==@ file_accession ").loc[:,showonly_column].values[0]
                            for file_accession in pca.feature_names_in_]
                show_idx = list(locate(labels_show, lambda x: x == showonly))

                pc1 = [ pca.components_[0][i] for i in show_idx]
                pc2 = [ pca.components_[1][i] for i in show_idx]
                c = [ labels_transformed[i] for i in show_idx]
                
                labels = list(le.inverse_transform(c))

                if ax is not None:
                    if ax_row_size > 1:
                        ax[np.floor(i/ax_col_size).astype(int)][i%ax_col_size].scatter(pc1, pc2, c = c, alpha=0.8, lw=0)
                    else:
                        ax[i].scatter(pc1, pc2, c = c, alpha=0.8, lw=0)

                else:
                    plt.scatter(pc1, pc2, c = c, alpha=0.8, lw=0)


            else:
                if ax is not None:
                    # just good for 1-row subplots
                    ax[i].scatter(np.delete(pca.components_[0], filter_idx, 0),
                                                            np.delete(pca.components_[1], filter_idx, 0),
                                                            c = np.delete(labels_transformed, filter_idx, 0),
                                                            alpha=0.8,
                                                            lw=0)
                else:
                    plt.scatter(np.delete(pca.components_[0], filter_idx, 0),
                                np.delete(pca.components_[1], filter_idx, 0),
                                c = np.delete(labels_transformed, filter_idx, 0),
                                alpha=0.8,
                                lw=0)


        else:
            if showonly is not False:
                labels_show = [bigwig_metadata.query(
                            "`File accession`==@ file_accession ").loc[:,showonly_column].values[0]
                            for file_accession in pca.feature_names_in_]
                show_idx = list(locate(labels_show, lambda x: x == showonly))
                
                labels = [ labels_show[i] for i in show_idx]
                
                pc1 = [ pca.components_[0][i] for i in show_idx]
                pc2 = [ pca.components_[1][i] for i in show_idx]
                c = [ labels_transformed[i] for i in show_idx]

                labels = list(le.inverse_transform(c))
                
                plt.scatter(pc1, pc2, c = c, alpha=0.8, lw=0)

            else:
                plt.scatter(pca.components_[0],
                            pca.components_[1],
                            c = labels_transformed,
                            alpha=alpha,
                            lw=lw)

    
    
    else: 
        labels_transformed = None
        plt.scatter(pca.components_[0],
                    pca.components_[1],
                    alpha=alpha,
                    lw=lw)

    
    if showlabels is not False:
        plt.xlabel("PC-1 (%f)" % pca.explained_variance_ratio_[0])
        plt.ylabel("PC-2 (%f)" % pca.explained_variance_ratio_[1])


    # display labels for data points on the plot
    if label_display is True:
        label_plot(showonly, pc1, pc2, labels, ax, pca, ax_row_size, ax_col_size, i)
        """ if showonly is not False:
            for idx, (x,y) in enumerate(zip(pc1,pc2)):
                label = labels[idx]
                if ax is not None:
                    ax[np.floor(i/ax_col_size).astype(int)][i%ax_col_size].annotate(label, # this is the text
                                (x,y), # these are the coordinates to position the label
                                textcoords="offset points", # how to position the text
                                xytext=(0,10), # distance from text to points (x,y)
                                ha='center',
                                fontsize=8) # horizontal alignment can be left, right or center
                else:
                    plt.annotate(label, # this is the text
                                (x,y), # these are the coordinates to position the label
                                textcoords="offset points", # how to position the text
                                xytext=(0,10), # distance from text to points (x,y)
                                ha='center',
                                fontsize=8) # horizontal alignment can be left, right or center

        else:
            for idx, (x,y) in enumerate(zip(pca.components_[0],pca.components_[1])):
                label = labels[idx]
                if ax is not None:
                    ax[np.floor(i/ax_row_size).astype(int)][i%ax_row_size].annotate(label, # this is the text
                                (x,y), # these are the coordinates to position the label
                                textcoords="offset points", # how to position the text
                                xytext=(0,10), # distance from text to points (x,y)
                                ha='center',
                                fontsize=8) # horizontal alignment can be left, right or center
                else:
                    plt.annotate(label, # this is the text
                                (x,y), # these are the coordinates to position the label
                                textcoords="offset points", # how to position the text
                                xytext=(0,10), # distance from text to points (x,y)
                                ha='center',
                                fontsize=8) # horizontal alignment can be left, right or center """

def label_plot(showonly, component1, component2, labelList, axes, pca, ax_row_size, ax_col_size, index):
    """
    Labels each point on the PCA plot with given metadata labels

    Keyword arguments:
    showonly -- use the prefiltered list of labels, given by showonly_column
    component1 -- the first PCA component, possibly subject to prior modification
    component2 -- the second PCA component, possibly subject to prior modification
    labeList -- the list of labels for each data point
    axes -- the labels for the axes 
    pca -- PCA object
    index -- the adjusting index for column index 
    ax_row_size -- the size of the labels for the row index
    ax_col_size -- the size of the labels for the column index
    """
    if showonly is not False:
            for idx, (x,y) in enumerate(zip(component1,component2)):
                label = labelList[idx]
                if axes is not None:
                    axes[np.floor(index/ax_col_size).astype(int)][index%ax_col_size].annotate(label, # this is the text
                                (x,y), # these are the coordinates to position the label
                                textcoords="offset points", # how to position the text
                                xytext=(0,10), # distance from text to points (x,y)
                                ha='center',
                                fontsize=8) # horizontal alignment can be left, right or center
                else:
                    plt.annotate(label, # this is the text
                                (x,y), # these are the coordinates to position the label
                                textcoords="offset points", # how to position the text
                                xytext=(0,10), # distance from text to points (x,y)
                                ha='center',
                                fontsize=8) # horizontal alignment can be left, right or center

    else:
        for idx, (x,y) in enumerate(zip(pca.components_[0],pca.components_[1])):
            label = labelList[idx]
            if axes is not None:
                axes[np.floor(index/ax_row_size).astype(int)][index%ax_row_size].annotate(label, # this is the text
                            (x,y), # these are the coordinates to position the label
                            textcoords="offset points", # how to position the text
                            xytext=(0,10), # distance from text to points (x,y)
                            ha='center',
                            fontsize=8) # horizontal alignment can be left, right or center
            else:
                plt.annotate(label, # this is the text
                            (x,y), # these are the coordinates to position the label
                            textcoords="offset points", # how to position the text
                            xytext=(0,10), # distance from text to points (x,y)
                            ha='center',
                            fontsize=8) # horizontal alignment can be left, right or center

    