import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Polygon
import yaml
from collections import Counter

# load the Background image
img = mpimg.imread("/home/p/Documents/SemB/python/img/background.png")

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

# Pflanzen mit x-werten momentan auskommentiert -> wie lösen?
# BE_1021 -> Standort 11
# BE_1049 -> Standort 7aB
# BE_1053 -> Standort 7g
# BE_1057 -> Standort 14?
# BE_1059 -> Standort 9a
# BE_2004 -> Standort 7as
title = "BE_1057"
with open (f"/home/p/Documents/SemB/python/lists/{title}.yaml", 'r') as f:
    plants = yaml.safe_load(f)

################## TESTING GROUND - Values incorrect
# plants = [{"name": "F2 | R1", "f": 2, "r": 1},
#           {"name": "F2 | R1.5", "f": 2, "r": 1.5},
#           {"name": "F2 | R2", "f": 2, "r": 2},
#           {"name": "F2 | R2.5", "f": 2, "r": 2.5},
#           {"name": "F2 | R3", "f": 2, "r": 3},
#           {"name": "F2 | R3.5", "f": 2, "r": 3.5},
#           {"name": "F2 | R4", "f": 2, "r": 4},
#           {"name": "F2 | R4.5", "f": 2, "r": 4.5},
#           {"name": "F2 | R5", "f": 2, "r": 5},
          
#           {"name": "F1 | R2", "f": 1, "r": 2},
#           {"name": "F1.5 | R2", "f": 1.5, "r": 2},
#           {"name": "F2 | R2", "f": 2, "r": 2},
#           {"name": "F2.5 | R2", "f": 2.5, "r": 2},
#           {"name": "F3 | R2", "f": 3, "r": 2},
#           {"name": "F3.5 | R2", "f": 3.5, "r": 2},
#           {"name": "F4 | R2", "f": 4, "r": 2},
#           {"name": "F4.5 | R2", "f": 4.5, "r": 2},
#           {"name": "F5 | R2", "f": 5, "r": 2}
# ]
################### END OF TESTING GROUND

# check the values
for plant in plants:
    if not (0 <= plant["r"] <= 5) or not (0 <= plant["f"] <= 5):
        raise ValueError(f"Invalid values for {plant['name']}: r={plant['r']}, f={plant['f']}")

# Übersetzung der Koordinaten
value_to_coordinate = {1: 0, 1.5: 0.25, 2: 0.5, 2.5: 1.5, 3: 2.5, 
                       3.5: 3.5, 4: 4.5, 4.5: 4.75, 5: 5}

# define the coordinate lists
x_points = []
y_points = []
# for each plant in the dictionary, add the x and y values to the coordinate list
# the 6 - plant[...] part is for inversion of the values, so i don't have
# to invert the y-axis
fxplants_x = []
fxplants_y = []
fxplants = [] # a list containing all plants where f = x (0 here)
rxplants = [] # a list containing all plants where r = x (0 here)
rxplants_x = []
rxplants_y = []
for plant in plants:
    # checks for the indicator values. a "0" represents an x in landolt
    if plant["r"] < 1 or plant["f"] < 1:
        if plant["f"] == 0:
            # adds all "x" plants to a separate list which should later be 
            # plotted separately
            fxplants.append(plant)
            # same for the x-values for R
        elif plant["r"] == 0:
            rxplants.append(plant)
        else:
            continue 
    else:
        r_val = value_to_coordinate[plant["r"]]
        f_val = value_to_coordinate[6 - plant["f"]]
        x_points.append(r_val)
        y_points.append(f_val)
################################# SOMETHING LIKE ABOVE FOR W AND RV!!!!!!!!!!
# special cases
for plant in rxplants:
    if plant["r"] == 0:
        # for R = "x" (or here 0): set the coordinate to 3 and plot the rect
        # over the whole graph
        r_val = 3
    else:
        r_val = value_to_coordinate[plant["r"]]
        f_val = value_to_coordinate[6 - plant["f"]]
    rxplants_x.append(r_val)
    rxplants_y.append(f_val)

# same thing for fxplants
for plant in fxplants:
    if plant["f"] == 0:
        # for R = "x" (or here 0): set the coordinate to 3 and plot the rect
        # over the whole graph
        f_val = 3
    else:
        r_val = value_to_coordinate[plant["r"]]
        f_val = value_to_coordinate[6 - plant["f"]]
    fxplants_x.append(r_val)
    fxplants_y.append(f_val)    


# Weighted mean
point_counter = Counter(zip(x_points, y_points))

# Exponential weighting: duplicate points weight much more
power = 2 # what number is reasonable?
x_weighted = sum(x * (count**power) for (x, y), count in point_counter.items())
y_weighted = sum(y * (count**power) for (x, y), count in point_counter.items())
total_weight = sum(count**power for count in point_counter.values())

x_weighted /= total_weight
y_weighted /= total_weight

ax.plot(x_weighted, y_weighted, 'ro', markersize=8)

# plot special r cases (x/0)
for x, y in zip(rxplants_x, rxplants_y):
    # plotes plants with R x (or 0 here) as a 'bar' over the whole x-axis
    rect_coords = [(0, y-0.5), (5, y-0.5),
                   (5, y+0.5), (0, y+0.5)]
    rect = Polygon(rect_coords, facecolor='#00ff00', alpha=0.1, edgecolor='black')
    ax.add_patch(rect)
    
# plot special f cases (x/0)
for x, y in zip(fxplants_x, fxplants_y):
    # plotes plants with R x (or 0 here) as a 'bar' over the whole x-axis
    rect_coords = [(x-0.5, 0), (x+0.5, 0),
                   (x+0.5, 5), (x-0.5, 5)]
    rect = Polygon(rect_coords, facecolor='#00ff00', alpha=0.1, edgecolor='black')
    ax.add_patch(rect)
    
# plot rectangles
for x, y in zip(x_points, y_points):
    rect_coords = [(x-0.5, y-0.5), (x+0.5, y-0.5), 
                   (x+0.5, y+0.5), (x-0.5, y+0.5)]
    rect = Polygon(rect_coords, facecolor='#00ff00', alpha=0.1, edgecolor='black')
    ax.add_patch(rect)

# Create legend entries (automatically from plants)
legend_elements = []
for plant in plants:
    legend_elements.append(
        plt.Line2D([0], [0], marker='o', color='w', 
                   markerfacecolor='black', markersize=8, 
                   label=plant['name'])
    )
# add "Zentrum" to the legend
legend_elements.append(
    plt.Line2D([0], [0], marker='o', color='w',
               markerfacecolor='red', markersize=10,
               label='Zentrum (Mehrfache Punkte\nam selben Ort zählen ^2')
    )

# set Axis labels
plt.ylabel("Feuchtigkeit")
plt.xlabel("")

# Place legend outside to the right
ax.legend(handles=legend_elements, 
          loc='upper left', 
          bbox_to_anchor=(1, 1),  # Move right of plot
          frameon=True)  # Keep frame

# Adjust figure to make room for legend
plt.subplots_adjust(right=0.75)  # Leave 25% space on right

# Set the plot title
plt.title(title)

# show the plot
plt.show()
print("RXPLANTS: ", rxplants)
print("RXPLANTS_X:\n", rxplants_x)
print("RXPLANTS_Y:\n", rxplants_y)
print("FXPLANTS: ", fxplants)