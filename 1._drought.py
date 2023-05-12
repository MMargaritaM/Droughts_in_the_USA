# -*- coding: utf-8 -*-
"""
@author: Margarita
"""

# Initial setup
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import geotools

# Setting the default resolution of plots to 300
plt.rcParams[ 'figure.dpi' ] = 300

# Defining the CONUS area
# Projected coordinate system for US
conus = 5070

cdf = gpd.read_file('cb_2019_us_state_500k.zip')
# Cliping the layer to select US continental area and eliminate Alaska and Hawaii
cdf = cdf.query( 'STATEFP <= "56"' )
cdf = cdf.query( 'STATEFP != "02" & STATEFP != "15"' )
cdf = cdf.to_crs(epsg=conus)

us_area = cdf.to_crs(epsg=conus).geometry.area.sum()
print(us_area)

# Setting the graph parameters
cols = [plt.get_cmap('hot_r')(0.2+i/7) for i in range(5)]
labels = ['Normal','D0 - Abnormally dry', 'D1 - Moderate drought', 'D2 - Severe drought', 'D3 - Extreme drought', 'D4 - Exceptional drought']
pp = [mpl.patches.Patch(edgecolor='k', facecolor = cols[y-1] if y else 'w', label=labels[y]) for y in range(6)]

# Defining the map plotting function
def draw_map(ax, date, filename):
    gdf = gpd.read_file(filename)
    gdf.head()
    geotools.make_valid(gdf)
    gdf = gdf.to_crs(conus)
    gdf = gdf.clip(cdf, keep_geom_type=True)

    cdf.boundary.plot(ax=ax, edgecolor='k')
    for d in range(0,5):
        x=gdf[gdf["DM"]==d]
        if len(x)>0 :
            x.plot(ax=ax,color=cols[d])
            print(filename, d, x.area)

    ax.text(0.5,0.94, date, transform = ax.transAxes, ha='center')
    ax.legend(handles=pp, loc = 'lower left', frameon=False, fontsize=6)
    ax.set_axis_off()

# Datafiles to be plotted 
info = {
    '20100427':'USDM_20100427_M.zip',
    '20150428':'USDM_20150428_M.zip',
    '20200428':'USDM_20200428_M.zip',
    '20220426':'USDM_20220426_M.zip',
    }

# Setting the position of the maps in the figure 
fig, axes = plt.subplots(2,2,figsize=(10,6))
draw_map(axes[0][0], '2010', info['20100427'])
draw_map(axes[0][1], '2015', info['20150428'])
draw_map(axes[1][0], '2020', info['20200428'])
draw_map(axes[1][1], '2022', info['20220426'])

fig.tight_layout()
# Saving the figure
fig.savefig("map2010-2022_US.png")

#%%
# Datafiles to be plotted
info = {
    '20230404':'USDM_20230404_M.zip',
    '20230411':'USDM_20230411_M.zip',
    '20230418':'USDM_20230418_M.zip',
    '20230425':'USDM_20230425_M.zip',
    }

# Setting the position of the maps in the figure
fig, axes = plt.subplots(2,2,figsize=(10,6))
draw_map(axes[0][0], '04-04-23', info['20230404'])
draw_map(axes[0][1], '04-11-23', info['20230411'])
draw_map(axes[1][0], '04-18-23', info['20230418'])
draw_map(axes[1][1], '04-25-23', info['20230425'])

# Adjusting label spacing and axis 
fig.tight_layout()
# Saving the figure
fig.savefig("map2023_US.png")

#%%

# Datafile to be plotted 
filename = 'USDM_20220426_M.zip'
print(filename)

df = gpd.read_file(filename)
# Printing the datafile
df.head()

# Setting the bar graph parameters
ratios = (df.Shape_Area / us_area).tolist()[::-1]
print(ratios)
for i in range(5):
        t = sum(ratios[:i+1]) if i<5 else sum(ratios)
        b = sum(ratios[:i])
        plt.fill_between((0,0.2),(t,t), (b,b), color=cols[::-1][i])
plt.legend(handles=pp, loc = 'lower right', frameon=False, fontsize=12);
plt.xlim(0,1)
# Title to the graph
plt.title('Proportion of US area in USDM categories in 2022')

# Adjusting label spacing and axis 
fig.tight_layout()
# Saving the figure
fig.savefig("map2022_acum_US.png")





