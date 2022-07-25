# -*- coding: utf-8 -*-

"""
Created on Mon Mar 21 15:07:55 2022

@author: AD676KL

Spotify Project, finding:
    compare the most popular and least popular tracks across Spotify’s metrics

Download data here: https://drive.google.com/file/d/11PW4RD2VnE5qdiQ0eb64LmvUVnOauzhp/view?usp=sharing
    
    reference links:
    https://rstudio-pubs-static.s3.amazonaws.com/594440_b5a14885d559413ab6e57087eddd68e6.html
    https://jakevdp.github.io/PythonDataScienceHandbook/04.14-visualization-with-seaborn.html
    https://medium.com/m2mtechconnect/spotify-data-exploration-with-python-74dcc292031d
    https://towardsdatascience.com/spotify-data-project-part-1-from-data-retrieval-to-first-insights-f5f819f8e1c3
    https://medium.com/swlh/analysis-of-my-spotify-streaming-history-57a6088c3d3
    https://medium.com/@rafaelnduarte/how-to-retrieve-data-from-spotify-110c859ab304
    https://towardsdatascience.com/explore-your-activity-on-spotify-with-r-and-spotifyr-how-to-analyze-and-visualize-your-stream-dee41cb63526
    https://python-graph-gallery.com/391-radar-chart-with-several-individuals
    https://towardsdatascience.com/explore-your-activity-on-spotify-with-r-and-spotifyr-how-to-analyze-and-visualize-your-stream-dee41cb63526
    https://towardsdatascience.com/get-your-spotify-streaming-history-with-python-d5a208bbcbd3#:~:text=Getting%20the%20data,but%20it's%20usually%20much%20faster.
    
    https://www.youtube.com/watch?v=w_Jo4heVKT4&ab_channel=SimpliCode
    
"""

import pandas as pd
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import seaborn as sns
import ast

class AnalysingTrackData:
    def __init__(self,input_data):
        self.tracks_df = input_data        
        self.columns = self.tracks_df.columns.tolist()
        self.num_tracks = len(self.tracks_df['id'])
        self.popularity_agg_df = pd.DataFrame()
        self.artist_agg_df = pd.DataFrame()
        print(self.columns, self.num_tracks)
        
    
    def run(self):
        self.expanding_artists_per_track_short() # this code is complete and works
        #self.expanding_artists_per_track_long() # work no longer in progress.. rip
        self.binning_data_popularity() # this code is complete and works
        self.create_radial_plot() # this code is complete and works
        #self.aggregating_data_artist()
        
    def expanding_artists_per_track_short(self):
        """
        **Optimised version**
        If a track has multiple artists, then the artist column contains a list of the people who were on this track
        this code breaks out the artists and expodes the dataset out
        """
        temp_df = self.tracks_df
        print(temp_df['artists'])
        # converting the artist column from a list string to list 
        temp_df['artists'] = [ast.literal_eval(x) for x in temp_df['artists']]
        
        # expanding the df per artist
        temp_df = temp_df.explode('artists')        
        
        self.tracks_df = temp_df
        
    def expanding_artists_per_track_long(self):
        """
        **long version**
        If a track has multiple artists, then the artist column contains a list of the people who were on this track
        this code breaks out the artists and expodes the dataset out
        """        
        temp_df = self.tracks_df
        #print(type(temp_df['artists'][0]))
        
        # 1. turning the string list into a list
        
        # taking out the unnecessary characters and list verbage from each item in the artists column,
        # & splitting the string by , into a list format
        
        temp_df['index'] = temp_df.index
        print(temp_df[['index','artists']])
        
        
        temp_df['artists'] = [x.replace("'", "").replace("[","").replace("]","").split(", ") for x in temp_df['artists']]
        #print(type(temp_df['artists'][586670]))
        #print(temp_df['artists'][586670][1])
        
        temp_df2 = temp_df.explode('artists')
        print(temp_df2.head())

        
        # 2. exploding by each artist

        temp_df2 = temp_df.iloc[90:100]
        
        # creating a copy of the index to use as a key to merge on later
        temp_df2['index'] = temp_df2.index
        
        print(temp_df2[['index','artists']].head(3))
        
        # creating the expanded list of artists
        artists_df = temp_df2[['index','artists']]
        #print(artis)
        # unpacking the list of lists and flattening the data structure
        print('original length is:', len(artists_df['artists']))
        expanded = []
        for sub_list in artists_df['artists']:
            for item in sub_list:
                print(item)
                expanded.append(item)
        print('expanded length is:', len(expanded))
        
        
        # next: merging on the key column to repeat each index for each key
      #  artists_df = artists_df.merge(artists, left_on="")
        
        #temp_df3 = pd.merge(left=temp_df2, )
        
        
        
    def binning_data_popularity(self):
        """
        Aggregates the data in bins of 1000 tracks, where they are ordered by popularity
        """
        # sorting by popularity
        temp_df = self.tracks_df.sort_values("popularity", ascending=False, inplace=False)
        
        # deciding bin size
        num_bins = int(len(temp_df['id'])/1000)
        print('number of bins', num_bins)
        
        #########               creating bins 
        dict1 = {}
        for i in range(1,num_bins, num_bins-2):  #selecting first and last bin to analyse
            name = "bin"+str(i)
            print(name)
            vals = temp_df[(i-1)*1000:i*1000]
            vals['grp'] = i
            vals['count'] = 1
            vals = vals[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'grp', 'count']]
            vals=vals.groupby('grp').agg({'danceability':'mean', 
                                           'energy':'mean','loudness':'mean', 
                                           'speechiness':'mean','acousticness':'mean', 
                                           'instrumentalness':'mean','liveness':'mean', 
                                           'valence':'mean','tempo':'mean', 
                                           'grp':'sum','count':'sum'})
            
            dict1[name] = vals # storing first and last aggregated bins into a dictionary 
            
        # unpacking the dictionary and storing it in a df
        final_df = pd.DataFrame()
        for key, value in dict1.items():
            print(key)
            df = value
            final_df = pd.concat([df, final_df], 0) # adding new value from dict as a row in dict
            
        self.popularity_agg_df = final_df
        print('print', self.popularity_agg_df.head(10))
        
    def create_radial_plot(self):
        """
        Creates a radial plot based on the aggregated dataframe
        """
        radial_df = self.popularity_agg_df.transpose().rename_axis("category", axis=0).reset_index(drop=False)
        
        specific_categories = ['danceability', 'energy', 'liveness', 'valence', 'speechiness', 'instrumentalness']
        radial_df = radial_df[:][radial_df['category'].isin(specific_categories)]        
        N = len(specific_categories)
        print('radial properties', N, radial_df, specific_categories)
        AnalysingTrackData.plotradial(radial_df, N, specific_categories)
        
    def aggregating_data_artist(self):
        """
        Creates aggregated df by artist
        """
        temp_df = self.tracks_df.groupby('artists').agg("mean").sort_values("popularity", ascending=False).reset_index()[:10]
        print(list(temp_df.columns))
        g = sns.FacetGrid(temp_df) # defining the categroical example
        g.map(sns.barplot, "popularity", "artists")
        #plt.xticks(rotation=45)
        #plt.show()
        #print(len(self.tracks_df.index))
        #print(len(temp_df.index))
       
    @staticmethod
    def plotradial(df, N, categories):
        plt.clf()
        angles = [n/float(N)*2*pi for n in range(N)]
        angles += angles[:1]
        
        # initialise
        ax = plt.subplot(111,polar=True)
        
        # if you want the first axis to be on top
        ax.set_theta_offset(pi/2)
        ax.set_theta_direction(-1)
        
        plt.xticks(angles[:-1], categories)
        
        ax.set_rlabel_position(0)
        plt.yticks([0.2,0.4,0.6,0.8], ["0.2", "0.4","0.6","0.8"], color="grey", size=7)
        plt.ylim(0,1)
        
        # Ind1
        values=df.iloc[:,1].values.flatten().tolist()
        values += values[:1]
        print(angles, values)
        ax.plot(angles, values, linewidth=1, linestyle='solid', label="First Group")
        ax.fill(angles, values, 'b', alpha=0.1)
         
        # Ind2
        values=df.iloc[:,2].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label="Last Group")
        ax.fill(angles, values, 'r', alpha=0.1)
         
        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

        # Show the graph
        plt.show()
            
if __name__=="__main__":
    condition = input("Have you downloaded the data and updated the CSV path? y/n :")
    if condition == "n":
        print("Navigate to line 11 of this script to download the \
              data, update line 240, and then run again.")
        sys.exit()
    elif condition == "y":
        print("Thanks - running script.")
        pass
    else:
        print("Unrecognised value, re-run script")
        sys.exit()

    
    data = pd.read_csv(r"C:\myworkspace\data\tracks.csv")
    engine = AnalysingTrackData(data)
    engine.run()
