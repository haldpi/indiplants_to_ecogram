"""
Version 3.1:
    features: 
        - Plotgrösse abhängig von # Pflanzen am selben Ort
        - Plotskala nach Vorschlag Valentin
        - Aufschlüsselung der Plots in der Legende
        - R, F werden miteinbezogen
        - Fokus auf die Standortsbestimmung
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import yaml
from collections import Counter

# load the Background image
img = mpimg.imread("/home/p/Documents/SemB/python/img/background_blank.png")

# Plot the foundation of the Graph
# The y-axis
ax = plt.gca()
# Note the offset, needs consideration in further calculations??
ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.0, 5.5])
ax.set_yticklabels(['Nass', 'Feucht', 'Frisch', 'Trocken', 'Sehr\nTrocken', '', ''])

# The x-axis
# Because of offset calculate -0.5 to each x-axis!!
ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.0, 5.5])
ax.set_xticklabels(['Sauer', '', '', '', 'Basisch','', ''])
offset = 0.5

# load the image as the background
ax.imshow(img, extent=[0,5, 0,5], aspect='equal', zorder=0)
    
# Draw dots

# BE_1021 -> Standort 11
# BE_1049 -> Standort 7aB
# BE_1053 -> Standort 7g
# BE_1057 -> Standort 14?
# BE_1059 -> Standort 9a
# BE_2004 -> Standort 7as
title = "BE_2004"
with open (f"/home/p/Documents/SemB/python/lists/{title}.yaml", 'r') as f:
    plants = yaml.safe_load(f)

for plant in plants:
    if not (0 <= plant["r"] <= 5) or not (0 <= plant["f"] <= 5):
        raise ValueError(f"Invalid values for {plant['name']}: r={plant['r']}, f={plant['f']}")
        
value_to_coordinate_f = {0:0, 1: 5, 1.5: 5, 2: 4.5, 2.5: 3.5, 3: 2.5, 3.5: 1.5,
                         4: 0.9, 4.5: 0.4, 5: 0}

value_to_coordinate_r = {0:0, 1: 0.5, 2: 1.5, 3: 2.5, 4: 4.5, 5: 4.5}

# define the coordinate lists
x_points = []
y_points = []
# for each plant in the dictionary, add the x and y values to the coordinate list
# the 6 - plant[...] part is for inversion of the values, so i don't have
# to invert the y-axis
for plant in plants:
    if plant["f"] < 1 or plant["r"] < 1:
        continue
    else:
        r_val = value_to_coordinate_r[plant["r"]]
        f_val = value_to_coordinate_f[plant["f"]]
        x_points.append(r_val)
        y_points.append(f_val)
        
# count = len(x_points)
# pointsize = 8 * count

# point_counter = Counter(zip(x_points, y_points))
# for x, y in point_counter.items():
#     ax.plot(x, y, marker='o', color='gray', markersize=pointsize, alpha=0.6)

cap = 80  # maximum point size
# plot the points, increased size means more poins on the same spot
point_counter = Counter(zip(x_points, y_points))
point_ids = {}
for i, ((x, y), count) in enumerate(point_counter.items(), 1):
    point_ids[(x,y)] = i
    pointsize = min(8 * count, cap)
    # label 
    ax.plot(x, y, marker='o', color="#aaff00", markersize=pointsize, alpha=0.5)  # Size scales with count
    ax.text(x, y+0.1, str(i),  # Position slightly offset
        fontsize=16, color='red', ha='center')
    
# calculate the mean
# x_points_mean = sum(x_points) / len(x_points)
# y_points_mean = sum(y_points) / len(y_points)
# # plot the geometrical center (all points considered unique)
# # -> could see this as very low weighting
# ax.plot(x_points_mean, y_points_mean, 'ro', markersize=8)

# Group plants by their coordinates
plants_by_point = {}
valid_plants = [p for p in plants if p["f"] >= 1 and p["r"] >= 1]

for plant, x, y in zip(valid_plants, x_points, y_points):
    point_id = point_ids.get((x, y))
    if point_id not in plants_by_point:
        plants_by_point[point_id] = []
    plants_by_point[point_id].append(plant["name"])
    
# Create legend entries - first add point ID groups
legend_elements = []
for point_id, species_list in plants_by_point.items():
    # Group species in pairs with newlines
    formatted_species = []
    for i in range(0, len(species_list), 2):
        pair = species_list[i:i+2]
        formatted_species.append(', '.join(pair))
    
    label = f"Gruppe {point_id}:\n" + '\n'.join(formatted_species)
    
    legend_elements.append(
        plt.Line2D([0], [0], marker='o', color='w',
                   markerfacecolor='gray', markersize=10,
                   label=label)
    )
    
# add "Zentrum" to the legend
# legend_elements.append(
#     plt.Line2D([0], [0], marker='o', color='w',
#                markerfacecolor='red', markersize= 10,
#                label='Zentrum (ohne gewichtung)')
#     )

# set Axis labels
plt.ylabel("Feuchtigkeit")
plt.xlabel("")

# Place the legend outside the graph to the right
ax.legend(handles=legend_elements, 
          loc='upper left', 
          bbox_to_anchor=(1, 1),  # Move to the right of plot
          frameon=True,  # Frame around the Legend
          fontsize=14)

# Adjust the figure to make room for the legend
plt.subplots_adjust(right=0.75)

# scaling
fig = plt.gcf()  # Get current figure
fig.set_size_inches(8, 8)  # Width, height in inches?? really??

# set the plot title
plt.title(title)

# show the plot
plt.show()

