import pandas as pd
import geopandas as gpd 
import matplotlib.pyplot as plt 

# data = pd.read_html('http://citypopulation.de/php/guinea-admin.php') 

# for population_data in data:
#   print(population_data) 

# population_data.to_excel(r'C:\Users\Boubacar Diallo\Documents\NOVA COURS\GPSoPaA\Data Guinea\Website\Excel1 pop.xlsx')
  
population_data = pd.read_excel(r'C:\Users\Boubacar Diallo\Documents\NOVA COURS\GPSoPaA\Data Guinea\Website\Excel1 pop.xlsx')  

population_data = population_data[['Prefecture','Status','PopulationCensus2014-03-01']] 
population_data.rename(columns = {'PopulationCensus2014-03-01': 'Population_2014'}, inplace = True)  
population_data = population_data.loc[population_data['Status'] == 'Prefecture'] 

# Reading data from the shapefile 
gin_prefectures = gpd.read_file(r'C:\Users\Boubacar Diallo\Documents\NOVA COURS\GPSoPaA\Data Guinea\GIN_adm2.shp')
gin_prefectures = gin_prefectures[['NAME_2', 'geometry']]   
gin_prefectures.rename(columns = {'NAME_2' : 'Prefecture'}, inplace = True) 

# Reprojecting to projected coordinate system 
gin_prefectures.to_crs(epsg=31528, inplace = True) 

# Create a new gin_prefecturecolumn and calculate the areas of the districts 
gin_prefectures['area'] = gin_prefectures.area/1000000 

#Do an attributes join 
gin_prefectures = gin_prefectures.merge(population_data, on = 'Prefecture') 
# # Create a population density column
gin_prefectures['density_2014'] = gin_prefectures['Population_2014']/gin_prefectures['area'] 
# # # # # Plotting density
gin_prefectures.plot(column = 'density_2014', cmap = 'gist_rainbow', legend = True) 

# Create a new figure and axis
fig, ax = plt.subplots(figsize=(10,10))

# Plot the density choropleth
gin_prefectures.plot(column='Population_2014', legend= True, cmap='tab20_r', ax=ax)

# Add prefecture name labels
gin_prefectures.apply(lambda x: ax.annotate(s=x.Prefecture, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)

# Set the title and axis labels
ax.set_title('Population by Prefecture in Guinea (2014)')  
ax.set_xlabel('Longitude') 
ax.set_ylabel('Latitude')

# Show the plot
plt.show()

# Send to SQL
from sqlalchemy import create_engine
engine = create_engine("postgresql://postgres:Diallo10@localhost:5432/pop_guinea")  
gin_prefectures.to_postgis("gin_adm2", engine, if_exists='append') 
# End of real code with plotting
# End of code  


# import urllib3

# # create an instance of the PoolManager
# http = urllib3.PoolManager()

# # make a GET request to the URL
# # url = "https://www.example.com"
# url = "http://citypopulation.de/php/guinea-admin.php"
# response = http.request('GET', url)
# # print the response
# print(response.data.decode('utf-8'))   
# import contextily as ctx

# # Add a basemap from OpenStreetMap
# ctx.add_basemap(ax)

# # Show the map
# plt.show()



# from sqlalchemy import create_engine
# engine = create_engine("postgresql://postgres:Diallo10@localhost:5432/pop_guinea")  

# # Append data to existing table
# gin_prefectures.to_postgis("GIN_adm2", engine, if_exists='append')

# # Replace existing table with new data
# gin_prefectures.to_postgis("GIN_adm2", engine, if_exists='replace')

# # ploting
# gin_prefectures.plot(column='Population 2014', cmap='tab20c_r', legend=True)  
#   # Plotting prefecture
# gin_prefectures.plot("Population 2014", legend = True, cmap = 'tab10')  
#    # # # # Plotting density
# gin_prefectures.plot(column = 'density 2014', cmap = 'jet', legend = True)    