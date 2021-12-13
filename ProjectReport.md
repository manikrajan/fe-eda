# DS5100 FINAL PROJECT REPORT - GROUP 2

**Topic: Food Deserts**

**Grace Lyons (kat3ac), Kaia Lindberg (pkx2ec), Mani Shanmugavel (fdf7gn), Maxwell Jones (maj3js)**


## INTRODUCTION

For our project, we wished to examine the relationships of food deserts across the US. According to the Annie E. Casey Foundation, food deserts are “geographic areas where residents have few to no convenient options for securing affordable and healthy foods — especially fresh fruits and vegetables.” With this project, we aimed to answer two questions:

1. Where do food deserts occur?
2. How can our project be used to analyze specific areas?	

By answering these questions, we hope to find areas where help can be provided appropriately to minimize the effects of food deserts. 

## DATA CLEANING

We first obtained our data from the USDA where we downloaded a zip file that includes some information on the data, a list of variables (to help decode the variable naming), the primary dataset, and some supplemental state and county data. We then read the csv file into Python so that we could reformat and clean the data. After reading the csv file into Python, we noticed several ways in which we needed to sanitize our data. To start, we noticed that some of the state codes had leading spaces, so we simply deleted those to make the names cleaner. Next, we noticed that there were many counties with very similar or duplicate names (which makes sense, given how many counties there are), so we realized that we could not reliably call on a county’s name to identify a particular county. To fix this, we researched county data and found a table with unique FIPS code identifiers for each county, thus giving us a method of calling on each individual county. We could not find an easily downloadable table, so we used BeautifulSoup to web scrape the FIPS table from the Natural Resources Conservation Service (https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697). We then removed the duplicate state and county columns and could join the FIPS table with our data set. After merging the two, we still had a few things to clean. Here, the FIPS table had a leading zero, so we had to convert it to an int to remove it. Additionally, we noticed that we dropped some data we still wanted to use, such as some of the state level data being dropped due to a lack of it having a FIPS code, so we used a left join to fix this issue. After merging again, the data was kept intact. Next, we reformat the data to have each variable as a column (as opposed to a row) to make the data much more readable. We then split the data into two dataframes--one for state level and one for county level--based on the FIPS code of the value (anything >60 was for state-level). Finally, we saved the cleaned data and are now ready for further analysis and visualizations to achieve our goal of understanding the relationships between these food environment factors.



## ANALYSIS

As we were analyzing the data we found that we were often repeating similar analysis so we wrote these processes as methods in a class so that we could test, share, and re-use these functions to complete our analysis more easily and efficiently. We didn’t want to include all of these in the initial data cleaning process because some of these decisions may differ depending on the specific analysis. One example is allowing users to select a single state for their analysis. In addition, handling missing values is always an important part of data analysis, but the decision on how to handle them may differ depending on the analysis and question of interest. To allow for flexibility we’ve written a function that drops columns with missing values over a chosen threshold. With this flexibility the analyst can choose their own threshold that makes sense given the question(s) they seek to answer.We also found some inconsistencies such as columns that appeared to be at a county level, but actually had the same value within a state. These “hidden” state level columns may be acceptable for some analysis, but in other cases we may only be interested in variables that are more granular (i.e. at a county level). To address this we’ve also added a function that would identify these columns by calculating the variance within each column within each state and identifying those with zero variance. In addition to identifying these zero variance columns, this function also gives the option of dropping them from the dataframe. This dataset contained over 250 different variables, but some of them were measuring the same metric for different years. For example, PCT_LACCESS_POP10 measures the percentage of the population with low access to stores in 2010 while PCT_LACCESS_POP15 measures the same in 2015. Again, the decision on how to handle these columns could be different for different questions. For some analysis we may be interested in comparing these values from year to year to identify which counties saw the greatest changes so we’d want to keep both of these. However, for other analysis, it may be redundant to include both (as in many cases they’re likely fairly similar and highly correlated) and thus we may be interested in only keeping the latest data (e.g. keep 2015 and drop 2010). Thus, we wrote a function to programmatically identify pairs of columns like these and give the option to remove the older columns. Finally, since one of the goals of our project is to analyze the relationships between variables we included functionality to select a variable of interest for their analysis (e.g. correlations, plotting) and then checks whether the user’s inputted column is in the dataframe. From there the user can calculate which other variables are most positively (or negatively) correlated with their variable of interest, which could give insight into interesting relationships to investigate further. Beyond facilitating our initial exploratory data analysis, these functions were helpful in analyzing and visualizing the data to answer our questions of interest.



## RESULTS	

We’ve broken our results into three main sections. First, we’ll discuss our analysis of the characteristics of food deserts. Then, we will showcase how we’ve added functionality to dive deeper to gain insight into food environment factors within a single state. Our final section will analyze poverty persistent counties to gain insight into differences between counties.

<u>Food Deserts</u>	

To analyze the relationships of food deserts, we decided to compare the low income and low access to food variable with the following variables:

● Population

● Metro 

● Status

● Region

● Ethnicity



**Population**

For population, we found that food deserts were likely to occur in places of smaller populations, meaning that the highest values for low income and low access to food occurred in areas of lower population. As stated earlier, this was expected--we next wanted to verify the difference in these populations was likely connected to metro status.

![img](https://lh6.googleusercontent.com/so_GK5gXtgBs9tX5ZEGqqjQC_ohsfv8MQl7yZoiQkPHvPA13GPaOm-FM8l_ciRSI1KlfiaAyyvylAsFn1ow8baITiQPbywbGXUJDCygmH3V33vqAWDDsC_FS2FB6cG_nAGl-0Iam)



**Metro Status**

Looking at metro status, almost all of the high values for low income and low access to food occur in non-metro areas with low population. The boxplot between non-metro and metro also shows us very clearly that almost all of the high values for low access come from non-metro areas, , thus again confirming that food deserts are more likely to occur in non-metro areas.

![img](https://lh4.googleusercontent.com/3e4xCr5qG_pewcR6HDh7RhyRkuGq1IITqSTCrDy2ppzbzIQbSAfr2ckM5oUP5j0c8IwGGG7JYx5UyXKtEN5Yr7psm-gBOiHuFq77ZIj47qn3WgiTfiw8A9Zv9cfWDKr-XC4Eg_ps)



![img](https://lh6.googleusercontent.com/Rg0ZyoNdhC2uOegrSGm_0U6mHj5SeF0YUC6ikricrTVIwwL0At-Ole3LUzbxqcPzi52VWrl-mrQU9QE0gtxYsHU0qtDohCHGiNT50_3iBb3hK4XvEL2UQHUNUBgwjMhqSzJj_Scw)



**Region**	

Across the four different regions, we found that food deserts were least likely to occur in the Northeast and most likely to occur in the West. Southern regions followed closely behind the Western ones, with Midwest around the same range. From this, we can determine that West, South, and Midwest appear to be the most at risk of containing food deserts, while the Northeast region seems relatively safe.

![img](https://lh3.googleusercontent.com/cDMHFbpisggGcJ14g1wNFGe-zd8BWVf9A7hp8pZuuKzou8esN8ScikI1wFH_YGhbgKpXK2RZ6hTFb_W8HRO78B0Mbnede54brgBm--ixKYu72hZKxqXfKEh5R0IYp_dwpZ7xjRPH)

**Ethnicity**	

Between ethnicities, as the population is around 72% White, we could only accurately analyze food deserts for varying population levels of counties for White vs non-White ethnicities. For areas with mostly White population levels, low access levels seem relatively steady at around 10%--in the lower areas of white population, however, the low access levels rise up to an average of 20% with a range of over 50% in some counties. From this, areas of low white population seem to be at the most risk of containing food deserts.

![img](https://lh4.googleusercontent.com/l2lYzZbI9ySoy_OV4Yjw5kvm2k8uQkhGhwHB_lSVuGMyCj-FQ7MM93rXreo5w-oOYyowvIk7zn5otR5dWe5iic_OF_MWZLqtpMWx_5sK33__nDrSrGYiKBa9S4zWxG8maY1Xd1m9)

<u>Analysis of a State: New York</u>	

For many of the variables there was so much variability and noise in the data that it was difficult to visualize relationships between variables of interest. In addition, we thought it would be useful for certain types of analysis to be able to dig deeper into the counties in a single state. For the purpose of this example, we’ve chosen New York, but we’ve built in the functionality to make this process repeatable for the analysis of any state. For this example we’ll investigate what variables are correlated with adult diabetes rates in New York. First, used many of the functions described in the Analysis section above to prepare our data for this analysis:

1. Filter data down to selected state
2. Remove columns/rows with large % missing values
3. Find and keep only the most recent data points (i.e. keep LACCESS_POP15 and drop LACCESS_POP10)
4. Find "hidden" state level columns (columns that don't vary within a state) and drop them

After selecting our target variable of interest, in this example Adult Diabetes Rate in 2013 (PCT_DIABETES_ADULTS13) we calculate correlations between diabetes rate and all of the remaining variables. From these correlations we can start to see an interesting relationship where counties with higher poverty rates (child poverty rates in particular) tend to also have higher adult diabetes rates. Similarly counties with a larger portion of students that are eligible for free lunch tend to have higher diabetes rates. In addition, the larger number or SNAP and WIC authorised stores per 1,000 population also tend to be associated with higher diabetes rates. The most surprising variable on this list of the top 5 positive correlations is PCH_VEG_ACRESPTH_07_12 with a correlation of 0.46, suggesting that percent change in vegetable acres harvested tends to be positively correlated with adult diabetes rates.

![image-20211121181254090](C:\Users\Max\AppData\Roaming\Typora\typora-user-images\image-20211121181254090.png)

We’ve also calculated which variables are the most negatively associated with adult diabetes rates. The amount of recreation and fitness facilities (both the number, RECFAC16, and the number per 1000 population, RECFACPTH16) are moderately negatively correlated with adult diabetes rates for counties in New York. In addition, counties with higher median income (MEDHHINC15) tend to have lower diabetes rates, which is unsurprising given the positive correlation between diabetes and poverty rates observed above. The last variable on this list (FMRKT_ANMLPROD18) is quite specific as it measures the number of farmers' markets that report selling animal products, but given its relatively weak correlation of -0.295 it likely doesn’t have as clear of an association with diabetes rates in New York.

![image-20211121181350609](C:\Users\Max\AppData\Roaming\Typora\typora-user-images\image-20211121181350609.png)

The analysis of these correlations helped us narrow our focus from the over 200 variables to only a few variables that are most closely related to diabetes rates that we could then analyze and visualize further. For example, we’ve further analyzed the relationship between child poverty and diabetes rates below. This scatterplot shows a generally positive, linear relationship between these two variables that we could expect based on their correlation coefficient. However, this visualization especially with the inclusion of the Metro indicator and population size we can gain more insight than from just looking at the correlation metrics. For example, we observe two outliers, one being the county with an above average poverty rate of around 25%, but the lowest adult diabetes rate of under 7%. The county with the highest child poverty rates also has the highest adult diabetes rate, but this county is still outlying in the fact that both of its rates are much larger than the other counties. We also observe some interesting relationships between the metro and population variables. For example, non-metro counties tend to have smaller populations than metro counties and metro counties look to be more likely to have lower poverty and diabetes rates because there are more blue dots towards the bottom left of the graph.

![img](https://lh6.googleusercontent.com/xKr82gCwhy1_yO2TadZOA93yW0smyD6d5qeQMD2kx5dJcfl1p3YqTQ0AiiznIU7kyfhmKscVQXxEdNdVlK1rrJ52sMpbTZ9Ce3H9w0WZj_xArzFTBek3mtuxeSvh6AT1OcRloECQ)

As another example, here is a scatterplot between diabetes and the most negatively correlated variable, RECFACPTH16, or the number of recreation and fitness facilities per 1,000 population. Once again the scatter plot confirms the negative correlation between these two variables, but also gives more insight into potential outliers and the added relationship with metro and population. We observe that non-metro counties (red dots) tend to have fewer recreation and fitness facilities than metro counties. One again, the county with the lowest diabetes rate stands out as an outlier and in this case actually has the largest number of fitness facilities per population. 

![img](https://lh5.googleusercontent.com/U0oFpWRwNFwEsAM61ObR7dkphnciNkhDs2xUrWH8wEFzUgjF6BxSv0t_UHkPvY-Zgkz82YsPf5zZJdNFqkCWt7VvY1RrafuW7JWb5oiHBYXQCMUkotmuP96IlKqOd8IPzcPycWbM)

While this state and these variables are just one example, the way we’ve designed our program makes this analysis flexible and repeatable in the future to answer numerous new questions. The analysis of correlations in particular have been very valuable in focusing our analysis from the hundreds of potential variables to just those that are the most closely related to whichever variable we’re interested in at the time. This process allowed us, and will allow future users, to prioritize their time in analyzing and digging deeper into the most important variables.

## UNIT TESTING

We developed a class each to clean the data and analyze the data. We performed unit testing on these classes to test the accuracy of the code for data cleaning and analysis. We thoroughly tested cleaning inconsistencies in the dataset like whitespaces using assertEqual(). We have used test fixtures like setup() to set up the test cases.
We observed that FIPS codes for a few states and counties were missing or unavailable in the dataset during analysis. These inconsistencies were fixed by web scraping. We performed unit testing on the data gathered using web scraping. Testing was done to validate the FIPS code for a State or County.

 ![image](https://user-images.githubusercontent.com/6862254/145697359-fc245afd-e313-46b2-9772-01abf7ec744e.png)

## PROJECT MANAGEMENT

The team decided to assign roles and responsibilities for everyone in the team. A project plan was prepared, and an owner was assigned for each milestone. The team met weekly over a Zoom call to assess the status of the project. The team discussed the progress and impediments that other team members might have. We, as a team, worked together to resolve any impediments identified. Tools like GitHub and Google Drive were used for collaboration, which proved effective in our development process. This approach enabled us to be more agile and helped us meet deadlines.

## EXTRA CREDIT

There were inconsistencies related to FIPS code for States and Counties in our dataset. The team decided to web scrape the FIPS code data from USDA’s website to fix the inconsistencies. The team also had used user interaction to analyze specific results. The class for County analysis has functions that would require user interaction to analyze a variable of interest. For instance, Top 10 most significant correlations of a variable with other variables.


## CONCLUSION

​	Answering our first question, we found that food deserts occur in places of small population, non-metro, West, Midwest, and South regions, and low White populations. To answer our second question, we analyzed New York to demonstrate how our project could be used to analyze specific areas–here, in particular, we found a negative correlation between adult diabetes rate and number of recreational facilities and a positive correlation between child poverty rate and adult diabetes rate, some things someone like a governor could certainly examine to help advise policy decisions.

​	Now that we’ve analyzed the areas that food deserts occur, the next step would be enacting real-word steps in those areas such as the following:

● Incentivizing grocery stores and supermarkets

● Funding city-wide programs to encourage healthier eating

● Extending support for small, corner-type stores and neighborhood-based farmers markets

By implementing these steps, the impact of food deserts should be greatly diminished, and many more people will have access to convenient, healthy food options.

​	Finally, for future investigation, we would do a few things to further lessen the effects of food deserts. One, we would’ve loved to have additional research into all 250 variables–given the scope of our project, we couldn’t quite get to every variable, but examining all of them would very likely yield useful insight. Second, we believe a machine learning model could more accurately predict food deserts than our characteristic analyses to more efficiently use resources to eliminate food deserts. For our final change, we could also look into finding a new variable for remaining food deserts–our low income, low access variable worked well, but we would have liked to have also had a variable that measures low access to healthy food and not just low access to all food in general.
