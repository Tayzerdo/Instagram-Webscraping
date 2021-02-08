# Instagram-scraping-to-extract-information-from-the-last-posts

The goal for this work is to extract information regarding the posts to check if there is a variant regardging the best day/time to post the pictures

The Project is divided into :

### The first step 0 is to import the libraries:
#### import pandas as pd
#### import time
#### from selenium.webdriver import Chrome
#### from instascrape import *
#### from datetime import datetime

### The step 1 is to extract the last 100 posts link and store on a list

### Step 2 is to create a Data frame to store information that we will extract from the posts links, we used a library that is called instascrape, this library helps to extract the following information from each post:
#### timestamp
#### comments
#### likes
#### is_video
#### post link
#### caption
