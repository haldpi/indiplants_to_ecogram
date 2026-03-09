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
title = "BE_2004"
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
value_to_coordinate = {0:0, 1: 0, 1.5: 0.25, 2: 0.5, 2.5: 1.5, 3: 2.5, 
                       3.5: 3.5, 4: 4.5, 4.5: 4.75, 5: 5}

# define the coordinate lists
x_points = []
y_points = []
# for each plant in the dictionary, add the x and y values to the coordinate list
# the 6 - plant[...] part is for inversion of the values, so i don't have
# to invert the y-axis
fxplants = [] # a list containing all plants where f = x (0 here)
rxplants = [] # a list containing all plants where r = x (0 here)
specialplants = []
for plant in plants:
    # checks for the indicator values. a "0" represents an x in landolt
    if plant["r"] == 0 and plant["f"] == 0: specialplants.append(plant)
    elif plant["r"] < 1 or plant["f"] < 1:
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
    
# initiate the plantcounter to set the fillalpha properly
# fillalpha = 0.9 / len(plants)
fillalpha = 1 - (1 - 0.9)**(1/len(plants))
print(fillalpha)
rectfillcolor = (0,1,0,fillalpha)
rectedgecolor = (0,0,0,1)

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

# plot rectangles
def plotRects():
    valid_plants = [p for p in plants if p["r"] >= 1 and p["f"] >= 1]
    for (x, y), plant in zip(zip(x_points, y_points), valid_plants):
        print(x,y) 
        if plant["w"] == 2: height = 1
        elif plant["w"] == 3: height = 1.5
        else: height = 0.5
        if plant["rv"] == 2: width = 1.5
        else: width = 1
        # define the boundaries
        x1 = x-width
        y1 = y-height
        x2 = x+width
        y2 = y-height
        x3 = x+width
        y3 = y+height
        x4 = x-width
        y4 = y+height
        # restrict the rectangles to the graph
        if x1 < 0: x1 = 0
        if x2 > 5: x2 = 5
        if x3 > 5: x3 = 5
        if x4 < 0: x4 = 0
        if y1 < 0: y1 = 0
        if y2 < 0: y2 = 0
        if y3 > 5: y3 = 5
        if y4 > 5: y4 = 5
        rect_coords = [(x1, y1), (x2, y2), 
                       (x3, y3), (x4, y4)]
        rect = Polygon(rect_coords, facecolor=rectfillcolor, edgecolor=rectedgecolor)
        ax.add_patch(rect)
        # better visual for testing
        # ax.plot(x, y, marker='o', color='black', markersize=8, alpha=0.8)
        
    for plant in rxplants:  # Directly iterate plants, not coordinates
        # Get F coordinate (y position)
        y = value_to_coordinate[6 - plant["f"]]
        
        # Height scales with w
        if plant["w"] == 2: height = 1
        elif plant["w"] == 3: height = 1.5
        else: height = 0.5
        
        # Clamp to graph boundaries
        y1 = max(0, y - height)
        y2 = min(5, y + height)
        
        # Full width bar from x=0 to x=5
        rect_coords = [(0, y1), (5, y1), (5, y2), (0, y2)]
        rect = Polygon(rect_coords, facecolor=rectfillcolor, edgecolor=rectedgecolor)
        ax.add_patch(rect)

        # plot special f cases (x/0)
    for plant in fxplants:  # Directly iterate plants
        # Get R coordinate (x position)
        x = value_to_coordinate[plant["r"]]
        
        # Width scales with rv
        if plant["rv"] == 2: width = 1.5
        else: width = 1
        
        # Clamp to graph boundaries
        x1 = max(0, x - width)
        x2 = min(5, x + width)
        
        # Full height bar from y=0 to y=5
        rect_coords = [(x1, 0), (x2, 0), (x2, 5), (x1, 5)]
        rect = Polygon(rect_coords, facecolor=rectfillcolor, edgecolor=rectedgecolor)
        ax.add_patch(rect)
        
plotRects()

# plot the special plants (both r=0 and f=0)
for plant in specialplants:
    # These plants cover entire graph
    rect = Polygon([(0,0), (5,0), (5,5), (0,5)], 
                   facecolor=rectfillcolor, edgecolor=rectedgecolor)
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

# scaling
fig = plt.gcf()  # Get current figure
fig.set_size_inches(8, 8)  # Width, height in inches?? really??

# show the plot
plt.show()
# some basic debugging
print("RXPLANTS: ", rxplants)
print("FXPLANTS: ", fxplants)
print("PLANTS WITH BOTH F AND R = 0: ",len(specialplants))




IMPLEMENT ABUNDANCE, SEE DEEPSEEKS PROPOSAL!!!