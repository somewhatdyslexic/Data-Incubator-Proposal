# Work with oil data to generate some plots
import csv, numpy, operator
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

# Define paths to data
WTI_path = "C:/Users/Paul/Google Drive/Data Incubator/3/DCOILWTICO.csv"
LFS_path = "C:/Users/Paul/Google Drive/Data Incubator/3/Labor Force Survey AB.csv"
EI_path = "C:/Users/Paul/Google Drive/Data Incubator/3/EI data.csv"
House_path = "C:/Users/Paul/Google Drive/Data Incubator/3/House Stats.csv"

# Import data
WTI = pd.read_csv(WTI_path)
LFS = pd.read_csv(LFS_path)
EI = pd.read_csv(EI_path)
House = pd.read_csv(House_path)

# Clean up data
# WTI
WTI = WTI.dropna()
WTI['Year'], WTI['Month'], WTI['Day'] = zip(*WTI['DATE'].map(lambda x: x.split('-')))
del WTI['DATE']

# Labor Force Survey
#LFS = LFS.dropna()
#print LFS
#WTI['Year'], WTI['Month'], WTI['Day'] = zip(*WTI['DATE'].map(lambda x: x.split('-')))
#del WTI['DATE']

# Employment Insurance Data
EI = EI.dropna()
EI=EI[EI>0]
EI['Year'], EI['Month'] = zip(*EI['Ref_Date'].map(lambda x: x.split('/')))
del EI['Ref_Date'], EI['Vector'], EI['Coordinate']
EI[['Value']]=EI[['Value']].apply(pd.to_numeric,errors='raise')
EI['Oil Related'] = numpy.where(EI['OCC'].isin(['Occupations unique to forestry operations, mining, oil and gas extraction and fishing, excluding labourers', 'Supervisors, mining, oil and gas','Underground miners, oil and gas drillers and related workers','Mine service workers and operators in oil and gas drilling']),'yes','no') 

newEI = EI.groupby(['Year','Oil Related'],as_index=False)
muEI = newEI[['Value']].mean()

newEI2 = EI.groupby(['Year'],as_index=False)
muEI2 = newEI2[['Value']].mean()


# Housing Data
House = House.dropna()
House[['Sales','New_Listings','AverageDOM','Median_Price','Average_Price']] = House[['Sales','New_Listings','AverageDOM','Median_Price','Average_Price']].apply(pd.to_numeric,errors='coerce')
HouseGroup = House.groupby(['Type','Year'],as_index=False)
muHouseGroup = HouseGroup[['Sales','New_Listings','AverageDOM','Median_Price','Average_Price']].mean()


WTIbyMY= WTI.groupby(['Year','Month'],as_index=False).mean()

WTIbyY = WTIbyMY.groupby(['Year'],as_index=False).mean()

#'''
# Oil prices
WTIsub = WTIbyY[19:30]
fig1=plt.figure()
ax = fig1.add_subplot(111)
ax.set_ylim(25, 110)
p1 = plt.plot(WTIsub['Year'],WTIsub['VALUE'], color='red',linestyle='solid',label='West Texas Intermediate')
plt.ylabel('Cost per Barrel (USD)',color='red')
plt.xlabel('Year')
plt.legend(loc='lower right',prop={'size':10})
plt.show

# house days on market, number of sales
HouseSub = muHouseGroup[10:21]
fig2=plt.figure()
host = host_subplot(111, axes_class=AA.Axes)

plt.subplots_adjust(right=0.75)
par1 = host.twinx()
par2 = host.twinx()

offset = 60
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right",
                                    axes=par2,
                                    offset=(offset, 0))

par2.axis["right"].toggle(all=True)

host.set_xlim(2004, 2016)
host.set_ylim(25, 110)

host.set_xlabel("Year")
host.set_ylabel("West Texas Intermediate Price")
par1.set_ylabel("Average Days on Market")
par2.set_ylabel("Average New Listings per Month")

p1, = host.plot(WTIsub['Year'],WTIsub['VALUE'], label="West Texas Intermediate Price")
p2, = par1.plot(HouseSub['Year'],HouseSub['AverageDOM'], label="Average Days on Market")
p3, = par2.plot(HouseSub['Year'],HouseSub['New_Listings'], label="Average New Listings per Month")

par1.set_ylim(0, 70)
par2.set_ylim(600, 6400)

host.legend(loc='lower center',prop={'size':10})
host.figtext(.02, .02, "The relation between the per barrel price of West Texas Intermediate, the average number of days a home stays on the market before it is sold, and the average number of new house listings in the local housing market for the city of Calgary from 2005 - 2015")
host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())
par2.axis["right"].label.set_color(p3.get_color())


# EI Data 
nonOilEI = muEI[muEI['Oil Related']== 'no']
OilEI = muEI[muEI['Oil Related'] == 'yes']
fig3=plt.figure()
host = host_subplot(111, axes_class=AA.Axes)

plt.subplots_adjust(right=0.75)

host.set_xlim(2004, 2016)
host.set_ylim(120, 1350)

host.set_xlabel("Year")
host.set_ylabel("Employment Insurance Recipients")

p1, = host.plot(OilEI['Year'],OilEI['Value'], label="Oil-Related Occupations")
p2, = host.plot(nonOilEI['Year'],nonOilEI['Value'], label="Other Occupations")


host.legend(loc='top right',prop={'size':10})

host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())

#plt.draw()
#plt.show()

# house prices
fig4=plt.figure()
host = host_subplot(111, axes_class=AA.Axes)

plt.subplots_adjust(right=0.75)
par1 = host.twinx()
par2 = host.twinx()

offset = 60
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right",
                                    axes=par2,
                                    offset=(offset, 0))

par2.axis["right"].toggle(all=True)

host.set_xlim(2004, 2016)
host.set_ylim(245000, 570000)

host.set_xlabel("Year")
host.set_ylabel("Average Price (CAD)")
par1.set_ylabel("Price Per Barrel (USD)")
par2.set_ylabel("Number of Employment Insurance Recipients")

p1, = host.plot(HouseSub['Year'],HouseSub['Average_Price'], label="Home Sale Price")
p2, = par1.plot(WTIsub['Year'],WTIsub['VALUE'], label="West Texas Intermediate")
p3, = par2.plot(muEI2['Year'],muEI2['Value'], label="EI Recipients")
host.figtext(.02, .02, "The relation between the per barrel price of West Texas Intermediate, the unemployment rate, and the average sale price of homes in the city of Calgary from 2005 - 2015")
par1.set_ylim(25, 110)
par2.set_ylim(120, 1350)

host.legend(loc='lower center',prop={'size':10})

host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())
par2.axis["right"].label.set_color(p3.get_color())

plt.draw()
plt.show()
#'''