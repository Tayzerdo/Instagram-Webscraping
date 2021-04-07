# Instagram-scraping

### The goal for this work is to extract information from my instagram personal account Tayzerdo and check if there is a parttern related to the time/day I post and related to the hashtags that I use.

First of all, I used python with libraries to help me out to extract, manipulate and save the data into an excel file to export to Tableau for data visualization.

The library instascrape is the main component of the script part as allow us to retrieve the information regarding the posts. 

For this work the method was:

1. Retrieve the last 200 posts for each account.

2. Created some manual calculation to extract the:
  - Day of the week;
  - Part of the day that is divided into:
      - Night  From 00h until 6h;
      - Morning  From 6h until 12h;
      - Afternoon  From 12h until 18h;
      - Evening  From 18h until 00h.

3. Hashtag Ratio that is the number of likes per posts used.

4. Hashtag Quantity that is the number of posts that this specific hashtag has inside Instagram.



![IG Tayzerdo](https://user-images.githubusercontent.com/64328213/113900961-49a80900-97c6-11eb-851a-8bcdc72adf3a.png)


#### The link for the dashboard visualization in tableau
https://public.tableau.com/profile/tayzer.damasceno.de.oliveira#!/vizhome/IGtayzerdo/Dashboard1
