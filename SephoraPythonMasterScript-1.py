'''Python script to generate graphs from inventory ticketing system data'''
'''Authors - @Julia Liu, @Zihan Wen, @Rimika Banerjee, @Alisha Mirapuri, @Sara Deck,
			 @Abhinav Jaddu, @Hana Sheikh, @Varun Jadia (DiversaTech)
'''

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime



class MCSAnalyzer:
	def __init__(self, csv):
		self.csv_path = csv

	def avg_duration_esc(self):
		'''Plots the average ticket duration for each escalation type'''
		'''Output: escalation_average.png'''
		df_agg = pd.read_csv(self.csv_path)

		df_agg['Opened timestamp'] = pd.to_datetime(df_agg['Opened'])
		df_agg['Closed timestamp'] = pd.to_datetime(df_agg['Closed'])
		df_agg['Updated timestamp'] = pd.to_datetime(df_agg['Updated'])
		df_agg['SLA timestamp'] = pd.to_datetime(df_agg['SLA due'])
		df_agg['duration'] = df_agg['Closed timestamp'] - df_agg['Opened timestamp']
		df_agg['duration'] = df_agg['duration'].apply(lambda x: x.days)

		cleanup_escalation = {"Escalation" : {"High": 10, "Moderate": 6, "Normal": 3, "Overdue": 12}}
		df_agg.replace(cleanup_escalation, inplace=True)

		df_agg["duration"] = pd.to_numeric(df_agg["duration"])
		df_agg["Escalation"] = pd.to_numeric(df_agg["Escalation"])


		hm1 = df_agg[['duration', 'Escalation']]

		# computes average escalation based on duration
		hm2 = hm1.groupby(by=['duration'], as_index=False).mean().rename(columns={"Assigned To": "count"})

		## The graph shows the average priority for certain tasks based on how many days between being opened & closed.
		my_plot = hm2.plot.scatter('duration', 'Escalation', s = 100, color = 'indianred')
		fig = my_plot.get_figure()
		fig.savefig("avg_duration_esc.png", bbox_inches='tight', dpi=600)




	def avg_duration_pri(self):
		'''Plots the average ticket duration for each priority type'''
		'''Output: priority_average.png'''
		df_agg = pd.read_csv(self.csv_path)
		df_agg['Opened timestamp'] = pd.to_datetime(df_agg['Opened'])
		df_agg['Closed timestamp'] = pd.to_datetime(df_agg['Closed'])
		df_agg['Updated timestamp'] = pd.to_datetime(df_agg['Updated'])
		df_agg['SLA timestamp'] = pd.to_datetime(df_agg['SLA due'])
		df_agg['duration'] = df_agg['Closed timestamp'] - df_agg['Opened timestamp']
		df_agg['duration'] = df_agg['duration'].apply(lambda x: x.days)

		cleanup_priority = {"Priority" : {"P3 - Normal (1-3 Days)": 4, "P4 - Low (3-5 Days)": 2, "P1 - Critical (0-4 Hrs.)": 10, "P2 - Major (4-12 Hrs.)": 8}}
		df_agg.replace(cleanup_priority, inplace=True)

		df_agg["duration"] = pd.to_numeric(df_agg["duration"])
		df_agg["Priority"] = pd.to_numeric(df_agg["Priority"])

		hm1_p = df_agg[['duration', 'Priority']]

		# computes average priorities based on duration
		hm2_p = hm1_p.groupby(by=['duration'], as_index=False).mean().rename(columns={"Assigned To": "count"})

		## The graph shows the average escalation for certain tasks based on how many days between being opened & closed.
		ax = hm2_p.plot.scatter('duration', 'Priority', s = 100, color = "indianred")
		my_plot = ax
		fig = my_plot.get_figure()
		fig.savefig("avg_duration_pri.png", bbox_inches='tight', dpi=600)



	def pie_chart(self):
		'''Plots a pie chart showing the ratio of escalation types
		for all the tickets in that year'''
		df_agg = pd.read_csv(self.csv_path)

		# Pie chart for priority based on combined 2018/19 dataset
		labels = [4, 2, 1, 10]
		sizes = [30, 40, 10, 20]
		#add colors
		colors = ['grey','maroon','pink','white']
		fig1, ax1 = plt.subplots()
		ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
				shadow=True, startangle=90)
		# Equal aspect ratio ensures that pie is drawn as a circle
		ax1.axis('equal')
		plt.tight_layout()
		plt.show()


		# Pie chart for escalation based on combined 2018/19 dataset
		labels = [3, 6, 10, 12]
		sizes = [48, 11, 7, 34]
		#add colors
		colors = ['grey','maroon','crimson','pink']
		fig1, ax1 = plt.subplots()
		ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
				shadow=True, startangle=90)
		# Equal aspect ratio ensures that pie is drawn as a circle
		ax1.axis('equal')
		plt.tight_layout()
		plt.show()




	def heat_map_days(self):
		'''Plots heatmaps showing ticket density variation during the day for all days in the week'''
		'''Output: hm_days.png'''
		df_agg = pd.read_csv(self.csv_path)

		# ## Heat map for days of the week vs hours of the day

		df_agg['Opened timestamp'] = pd.to_datetime(df_agg['Opened'])
		df_agg['Closed timestamp'] = pd.to_datetime(df_agg['Closed'])

		df_agg['Opened Day'] = df_agg['Opened timestamp'].dt.dayofweek
		df_agg['Opened Hour'] = df_agg['Opened timestamp'].dt.hour
		df_agg['Closed Day'] = df_agg['Closed timestamp'].dt.dayofweek

		hm1 = df_agg[["Opened Day", "Opened Hour", 'Assigned To']]

		#group data by opened day and opened hour, then take count
		hm2 = hm1.groupby(by=['Opened Day','Opened Hour'], as_index=False).count().rename(columns={"Assigned To": "count"})

		#pivot data and drop NA values
		hm3 = hm2.pivot(index='Opened Hour', columns='Opened Day', values='count')

		plt.subplots(figsize=(15,10))

		x_axis_labels = ["Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] # labels for x-axis

		ax = sns.heatmap(hm3, cmap='Reds', xticklabels=x_axis_labels, cbar_kws={"orientation": "horizontal",'label': 'Number of Tickets'}) #cmap for changing color
		ax.set(title="Ticket Density based on Day of the Week and Hour of the Day")
		my_plot = ax

		fig = my_plot.get_figure()
		fig.savefig("heat_map_days.png", bbox_inches='tight', dpi=600)





	def heat_map_months(self):
		'''Plots heatmaps showing ticket density variation during the month for all months in the year'''
		'''Output: hm_months.png'''
		## Heat map for month of the year vs day of the month

		data1 = pd.read_csv(self.csv_path)

		#use date time objects to extract day and month from "Opened" Column


		data1['Opened timestamp'] = pd.to_datetime(data1['Opened'])
		data1['Closed timestamp'] = pd.to_datetime(data1['Closed'])

		data1['Day of Month'] = data1['Opened timestamp'].dt.day
		data1['Month'] = data1['Opened timestamp'].dt.month


		data2 = data1.groupby(by=['Day of Month','Month'], as_index=False).count().rename(columns={"Opened": "count"})

		data3 = data2.pivot(index='Day of Month', columns='Month', values='count')

		plt.subplots(figsize=(15,10))

		x_axis = ["January","February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] # labels for x-axis

		bx = sns.heatmap(data3, cmap='Reds', xticklabels=x_axis, cbar_kws={"orientation": "horizontal",'label': 'Number of Tickets'}) #cmap for changing color
		bx.set(title="Ticket Density based on Month and Day of the Month")

		my_plot = bx
		fig = my_plot.get_figure()
		fig.savefig("heat_map_months.png", bbox_inches='tight', dpi=600)




	def time_series_pri(self):
		'''See the average number of tickets for each priority category over the year'''
		'''Output: fig_time_series_pri.png'''
		df_agg = pd.read_csv(self.csv_path)

		df_agg['Opened'] = pd.to_datetime(df_agg['Opened'])

		cleanup_priority = {"Priority" : {"P3 - Normal (1-3 Days)": 4, "P4 - Low (3-5 Days)": 2, "P1 - Critical (0-4 Hrs.)": 10, "P2 - Major (4-12 Hrs.": 8}}
		df_agg.replace(cleanup_priority, inplace=True)

		pri = df_agg[['Opened','Priority']]
		pri['op'] = [a.date() for a in pri['Opened']]

		pri = pri[["op", "Priority"]]


		#seperating each type of priority into different tables

		two = pri[pri['Priority']==2].groupby(by="op").count().rename(columns={"Priority": "2"})
		four = pri[pri['Priority']==4].groupby(by="op").count().rename(columns={"Priority": "4"})
		eight = pri[pri['Priority']==8].groupby(by="op").count().rename(columns={"Priority": "8"})
		ten = pri[pri['Priority']==10].groupby(by="op").count().rename(columns={"Priority": "10"})



		#combining tables with priority 2 and 4
		all2 = pd.concat([two, four], axis=1)


		# .rolling(window=7) creates the 7 day moving average

		all3 = pd.concat([two["2"].rolling(window=7).mean(), four["4"].rolling(window=7).mean()], axis=1)
		all3= all3.rename(columns={"2":"P4 Tickets", "4":"P3 Tickets"})
		ax= all3.plot(figsize=[10,5], title="7 Day Moving Average of Tickets Based on Priority", color = ['crimson', 'darkblue'])
		ax.set_xlabel("Date")
		ax.set_ylabel("Number of Tickets")
		#plt.show()
		my_plot = ax
		fig = my_plot.get_figure()
		fig.savefig("time_series_pri.png", bbox_inches='tight', dpi=600)




	def time_series_esc(self):
		'''Plots the average number of tickets for each escalation category over the year'''
		'''Output: fig_time_series_esc.png'''
		df_agg = pd.read_csv(self.csv_path)
		df_agg['Opened'] = pd.to_datetime(df_agg['Opened'])

		cleanup_escalation = {"Escalation" : {"High": 10, "Moderate": 6, "Normal": 3, "Overdue": 12}}
		df_agg.replace(cleanup_escalation, inplace=True)


		esc = df_agg[['Opened','Escalation']]

		esc['op'] = [a.date() for a in esc['Opened']]

		esc = esc[["op", "Escalation"]]

		th = esc[esc["Escalation"]==3].groupby(by="op").count().rename(columns={"Escalation": "3"})
		six = esc[esc["Escalation"]==6].groupby(by="op").count().rename(columns={"Escalation": "6"})
		te = esc[esc["Escalation"]==10].groupby(by="op").count().rename(columns={"Escalation": "10"})
		tw = esc[esc["Escalation"]==12].groupby(by="op").count().rename(columns={"Escalation": "12"})


		esc4 = pd.concat([th, six, te, tw], axis=1, sort=True)

		# .rolling(window=7) creates the 7 day moving average
		# Graph with all types of ticket escalation (this is NOT what was used in midpoint deliverable)
		# This is just for reference, as the POCs said they wanted to see all types of tickets in one graph.

		all4 = pd.concat([th["3"].rolling(window=7).mean(), six["6"].rolling(window=7).mean(), te["10"].rolling(window=7).mean(), tw["12"].rolling(window=7).mean()], axis=1, sort=True)
		all4= all4.rename(columns={"3":"Tickets with Escalation Normal", "6":"Tickets with Escalation Moderate", "10":"Tickets with Escalation High", "12":"Tickets with Escalation Overdue"})
		ax= all4.plot(figsize=[10,5], title="7 Day Moving Average of Tickets Based on Escalation")
		ax.set_xlabel("Date")
		ax.set_ylabel("Number of Tickets")


		all5 = pd.concat([th["3"].rolling(window=7).mean(), tw["12"].rolling(window=7).mean()], axis=1, sort=True)
		all5= all5.rename(columns={"3":"Normal Escalation", "12":"Overdue Escalation"})
		ax2= all5.plot(figsize=[10,5], title="7 Day Moving Average of Tickets Based on Escalation" ,color = ['salmon', 'navy'])
		ax2.set_xlabel("Date")
		ax2.set_ylabel("Number of Tickets")

		plt.show()
		my_plot = ax2
		fig = my_plot.get_figure()
		fig.savefig("time_series_esc_overdue.png", bbox_inches='tight', dpi=600)

		plt.show()
		my_plot = ax
		fig = my_plot.get_figure()
		fig.savefig("time_series_esc_all.png", bbox_inches='tight', dpi=600)





	def duration_box_plot(self):
		'''Plots the interquartile range of ticket duration for each escalation type'''
		'''Output: duration_box_plot.png'''
		df_agg = pd.read_csv(self.csv_path)

		## initial cleaning
		df_agg['Opened timestamp'] = pd.to_datetime(df_agg['Opened'])
		df_agg['Closed timestamp'] = pd.to_datetime(df_agg['Closed'])
		df_agg['Updated timestamp'] = pd.to_datetime(df_agg['Updated'])
		df_agg['SLA timestamp'] = pd.to_datetime(df_agg['SLA due'])
		df_agg['duration'] = df_agg['Closed timestamp'] - df_agg['Opened timestamp']

		## table of only escalation and duration
		esc_dur = df_agg[['Escalation', 'duration']]
		esc_dur['days'] = esc_dur['duration'].apply(lambda x: x.days)
		esc_dur[['Escalation', 'days']].groupby('Escalation').count()

		ax = sns.boxplot(x="Escalation", y="days", whis=1.5, data=esc_dur)
		my_plot = ax
		fig = my_plot.get_figure()
		fig.savefig("duration_box_plot.png", bbox_inches='tight', dpi=600)


	def escalation_by_day(self):
		'''Plots the breakdown for each day of the week based on escalation'''
		'''Output: escalation_by_day.png'''
		df_agg = pd.read_csv(self.csv_path)
		df_agg['Opened timestamp'] = pd.to_datetime(df_agg['Opened'])
		df_agg['Closed timestamp'] = pd.to_datetime(df_agg['Closed'])
		df_agg['Updated timestamp'] = pd.to_datetime(df_agg['Updated'])
		df_agg['SLA timestamp'] = pd.to_datetime(df_agg['SLA due'])
		df_agg['duration'] = df_agg['Closed timestamp'] - df_agg['Opened timestamp']
		df_agg['duration'] = df_agg['duration'].apply(lambda x: x.days)
		df_agg['Opened Day'] = df_agg['Opened timestamp'].dt.dayofweek
		#df_agg.replace('Overdue', 0, inplace=True)
		#df_agg["Escalation"] = pd.to_numeric(df_agg["Escalation"])
		#grouped_by_escalation = df_agg.groupby(["Escalation"]).mean()
		#for_bar = grouped_by_escalation[['duration']]
		#for_bar.plot.bar(y = 'duration')

		#cleanup_priority = {"Priority" : {4: "P3", 8: "P2", 2: "P4", 10: "P1"}}
		#df_agg.replace(cleanup_priority, inplace=True)
		cleanup_openedday = {"Opened Day" : {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}}
		df_agg.replace(cleanup_openedday, inplace=True)
		#cleanup_escalation = {"Escalation" : {10: "High", 6: "Moderate", 3: "Low", 0: "Overdue"}}
		#df_agg.replace(cleanup_escalation, inplace=True)


		colors = ["#080808", "#faebd7","#db5a6b", "#001440"]


		pivot_df = df_agg.pivot_table(index='Opened Day', columns='Escalation', values='Assigned To', aggfunc='count')
		pivot_df


		for i in np.arange(0, 7):
			sum_row_i = sum(pivot_df.iloc[i])
			pivot_df.iloc[i] = pivot_df.iloc[i].apply(lambda x: x/(sum_row_i)) * 100


		pivot_df = pivot_df.reindex(["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"])


		ax = pivot_df.loc[:,['High','Normal', 'Moderate', 'Overdue']].plot.bar(stacked=True, color=colors, figsize=(10,7))
		my_plot = ax
		fig = my_plot.get_figure()
		fig.savefig("escalation_by_day.png", bbox_inches='tight', dpi=600)


'''Main Method': takes in specified file path and runs analysis'''
if __name__ == "__main__":
	file_path = input("Paste full file path to csv file: ")
	#mcs = MCSAnalyzer('/Users/rimikabanerjee/Downloads/MCS_2018.csv') MCSAnalysis/2019/
	mcs = MCSAnalyzer(file_path)
	print('made mcs analyzer')
	mcs.avg_duration_esc()
	print('avg_duration_esc done')
	mcs.heat_map_days()
	print('heat_map_days done')
	mcs.heat_map_months()
	print('heat_map_months done')
	mcs.escalation_by_day()
	print('escalation_by_day done')
	mcs.duration_box_plot()
	print('duration_box done')
	mcs.avg_duration_pri()
	print('avg_duration_pri done')
	mcs.time_series_esc()
	print('time_series_esc done')
	mcs.time_series_pri()
	print('time_series_pri done')
	print('master script -- DONE')
