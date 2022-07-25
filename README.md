# Spotify Tracks dataset
Objective: compare the most popular and least popular tracks across Spotify’s metrics, using modular approach. Not intended for use.

_Data is avaialable here: https://drive.google.com/file/d/11PW4RD2VnE5qdiQ0eb64LmvUVnOauzhp/view?usp=sharing_

## Background and Motivation: 
After spending hours on DataCamp, I wanted to apply my skills without the training wheels. 

Being in the top 1% of listeners (by minutes) in 2019, my personal Spotify data seemed like a good place to start. Initially, I tried connecting to the API using the docs as guidance but hit a wall quickly. I considered requesting my own personal data, but that could take up to 30 days to process.

I settled for a Kaggle dataset containing Spotify track data with ~577k rows. Now I had to figure out what insights I wanted from this data. Whatever it was, I wanted it to challenge my data manipulation and error-resolution skills. I wanted to use lists, dictionaries, arithmetic operations and string manipulation as much as I could (even if it would not be used in practice). 

By avoiding functions that help do hard stuff easily, I thought that I could challenge myself to understand better what happens under the hood. 

## Objective goals:
At first glance of the top 300 rows or so in Excel, I saw that the tracks level data had all collaborating artists stored as a list in a single cell. Given my familiarity with the Spotify docs, I assume that before this CSV was created from a JSON file. 

To meet my objective, I had to:
  1.	Create a more granular dataset with an exploded artist column
  2.	Bin the dataset by popularity
  3.	Display this visually

## Next potential objectives:
One way of building this script application out is to have other modules created with different objectives. Potential objectives include: 
•	Top 100 Most Popular songs versus all of the dataset 
•	Comparing the Eras: Pre 90s versus Post 90s
•	Visualising the most popular artists

## How to Run
Steps:
  1.	Go to the following link and download the CSV: 
      https://drive.google.com/file/d/11PW4RD2VnE5qdiQ0eb64LmvUVnOauzhp/view?usp=sharing
  2.	In the script, go to the `if __name__=="__main__"` section, and change the CSV path 
  3.  Click run
  4.   ....
  5.  Profit $$

## Resources
https://drive.google.com/file/d/11PW4RD2VnE5qdiQ0eb64LmvUVnOauzhp/view?usp=sharing

https://developer.spotify.com/documentation/web-api/

https://support.spotify.com/uk/article/data-rights-and-privacy-settings/

https://support.spotify.com/uk/article/understanding-my-data/
