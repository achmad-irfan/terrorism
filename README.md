<p align="right"> <a href="https://achmadirfana.github.io/portofolio/portfolio-pizza-place.html">Back</a></p>


<h2 align="center">  Global Terrorism</h2>
<p> URL Dashoboard project : <a href="https://terrorism.onrender.com/">Global Terrorism</a></p>
<h3> Background Project :</h3>
<p style="margin-left: 20px"> This is project from stratascratch with level medium category of difficulty </p>
<h3>Purpose:</h3>
<p style="margin-left: 20px;text-align:justify">  Imagine you are a security or defense analyst. Analyze the data and draw conclusions on the distribution and nature of terrorist incidents recorded around the world. In your analysis, include maps that visualize the location of different incidents. Your analysis may also provide answers to the following questions:
</p>
<p style="margin-left: 30px">• How has the number of terrorist activities changed over the years? Are there certain regions where this trend is different from the global averages? </p>
<p style="margin-left: 30px">• Is the number of incidents and the number of casualties correlated? Can you spot any irregularities or outliers?</p>
<p style="margin-left: 30px">• What are the most common methods of attacks? Does it differ in various regions or in time?</p>
<p style="margin-left: 30px">• Plot the locations of attacks on a map to visualize their regional spread;</p>
					       
<h3>Datas:</h3>
<h4>Dataset:</h4>
<p style="text-align:justify">The provided compressed file globalterrorismdb_0718dist.tar.bz2 is an extract from the Global Terrorism Database (GTD) - an open-source database including information on terrorist attacks around the world from 1970 through 2017. The GTD includes systematic data on domestic as well as international terrorist incidents that have occurred during this time period and now includes more than 180,000 attacks. The database is maintained by researchers at the National Consortium for the Study of Terrorism and Responses to Terrorism (START), headquartered at the University of Maryland </p>
<p style="text-align:justify">Since the number of variables and instances is very large, for this project, only data from 2000 above will be hold as data:</p>
<p><p align="left"> <a href="https://platform.stratascratch.com/data-projects/terrorism-hotspots">Global Terrorism</a></p> </p>
<p>each file is data from 2015 and must be imported to jupyter notebook</p>


<h3>Data Preparation</h3>
<p> All files must be put in the same folder/directory as python </p>
<h4>Data Validation</h4>
<p style="margin-left: 30px"> All the data must be checked whetever there is blank data. The  queery for data checking blank data:</p>
<div style="margin-left: 30px;height:50px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
<p style="margin-left: 20px">import pandas as pd </p>
<p style="margin-left: 20px">data= pd.read_csv("data.csv") </p>
<p style="margin-left: 20px">data.isnull().sum()/len(data)*100</p>
</div> 
<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="Terror3.png" class="img-fluid" alt="">  
</p>

<h4>Data Duplicate Checking</h4>
<p style="margin-left: 30px"> Code for data duplicate checking :</p>
<div style="margin-left: 30px;height:50px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
  <p style="margin-left: 20px">data.duplicated('eventid').any() #Checking whetevr any duplicate data in data order column event_id </p>
</div> 

<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="Terror4.png" class="img-fluid" alt="">  
</p>
<h3>Dat Analyze</h3>
<h4>1. Terrorist activities changed over the years and regions where this trend is different from the global averages</h4>
<p style="margin-left: 30px"> The trend of terrorism over years </p>
<p style="margin-left: 30px"> Code: </p>
<div style="margin-left: 50px;height:50px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
<p style="margin-left: 20px">total_terrorisme = data.groupby('iyear').count()['eventid'].reset_index() </p>
<p style="margin-left: 20px">total_terrorisme </p>
</div>

<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="Terror5.png" class="img-fluid" alt="">  
</p>

<p style="margin-left: 30px"> The trend of terrorism over years by line chart</p>
<p style="margin-left: 30px"> Code: </p>
<div style="margin-left: 50px;height:50px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
<p style="margin-left: 20px">total_terrorisme['iyear'] = [str(d) for d in total_terrorisme['iyear']]</p>
<p style="margin-left: 20px">sns.lineplot(data=total_terrorisme,x=total_terrorisme['iyear'],y=total_terrorisme['eventid'])</p>
<p style="margin-left: 20px">plt.xticks(rotation=90)</p>
<p style="margin-left: 20px">plt.tight_layout()</p>
<p style="margin-left: 20px">plt.title("Trend of Terrosim 2000-2017")</p>
<p style="margin-left: 20px">plt.gca().set_facecolor('black') </p>
</div>
<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="Terror6.png" class="img-fluid" alt="">  
</p>


<p style="margin-left: 30px"> From graph above, the trend of terrorisme is increase year by year, so to know which region/country that don't have the same trend , need to check the average of growth of terrorisme case from year to year.</p>
<p style="margin-left: 30px"> The Code of average of growth of terrorisme case:</p>

<div style="margin-left: 50px;height:150px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
<p style="margin-left: 20px">data_detail= data.pivot_table(index='iyear',values='eventid',columns='country_txt',aggfunc='count')</p>
<p style="margin-left: 20px">data_detail_growth= data_detail.pct_change(periods=1)*100</p>
<p style="margin-left: 20px">data_detail_growth.mean(axis=0).reset_index().sort_values(0,ascending=True).head(9)</p>
</div>
<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="Terror7.png" class="img-fluid" alt="">  
</p>

<h4>2. The correlation number of incidents and the number of casualties </h4>
<p style="margin-left: 30px"> Code: </p>
<div style="margin-left: 50px;height:150px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>
<p style="margin-left: 20px">data_correlation = data.groupby(['iyear','imonth']).agg({'eventid': 'count', 'nkill': 'sum'}).reset_index()</p>
<p style="margin-left: 20px">data_correlation['year-month']= data_correlation['iyear'].astype(str) +"-"+ data_correlation["imonth"].astype(str)</p>
<p style="margin-left: 20px">data_correlation['nkill'] = [round(d) for d in data_correlation['nkill']]</p>
<p style="margin-left: 20px">plt.figure(figsize=(10, 8),)</p>
<p style="margin-left: 20px">sns.scatterplot(data=data_correlation,x='eventid',y='nkill')</p>
<p style="margin-left: 20px">plt.title('Correlation Between Number of Case and Number of Victims')</p>
<p style="margin-left: 20px">plt.xlabel('Number of Case')</p>
<p style="margin-left: 20px">plt.ylabel('Total Victims')</p>
<p style="margin-left: 20px">plt.gca().set_facecolor('black')</p>
</div>


<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="Terror8.png" class="img-fluid" alt="">  
</p>


<h4>4. The most common methods of attacks?</h4>
<p style="margin-left: 30px"> Code: </p>
<div style="margin-left: 50px;height:80px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>

</div>

<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="no-3.png" class="img-fluid" alt="">  
</p>

<h4>4. Plot the locations of attacks on a map to visualize their regional spread</h4>
<p style="margin-left: 30px"> Code: </p>
<div style="margin-left: 50px;height:80px;width:1000px;border:1px solid #ccc;font:14px/6px Georgia, Garamond, Serif;overflow:auto;">
	<p> </p>

</div>

<p style="margin-left: 30px"> Output: </p>
<p align="center"> 
<img src="no-4.png" class="img-fluid" alt="">  
</p>

<h3>6. Insight and Recomendation</h3>
<h4 style="margin-left: 20px">6.1 Insight</h4>
<p style="margin-left: 40px"> • Based on data, time around lunch and dinner is the time with the most oder of pizzas</p>
<p style="margin-left: 40px"> • More than 75% income  is the from pizza with the M and S size  </p>
<p style="margin-left: 40px"> • Pizzas with the chicken meat is the most sold pizzas  </p>
<p style="margin-left: 40px"> • The business is stabil in 2015 based on income with the avarge of 5% growth or loss   </p>
<h4 style="margin-left: 20px"> 6.2 Reccmendation</h4>
<p style="margin-left: 40px;align=justify"> •Pizzas in sizes XL and XXL contribute very little to revenue, so to further maximize revenue 1-2 hours before closing, pizzas in XXL or XL can be scaled down to sizes S or L to increase the likelihood of being sold  <p>
<p style="margin-left: 40px;align=justify"> •	Make sure the stock of chicken meat is always available because pizza with chicken meat sells very well compared to other flavors/toppings  <p>

