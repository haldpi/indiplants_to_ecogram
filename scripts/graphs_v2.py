"""
Version 4.5:
    features:
        - Keine individuelle Transparenz
            -> Ermöglicht den Vergleich zwischen verschiedenen Aufnahmen
            -> Feste Transparenz
        - <Pflanzendichte> in der Legende angegeben
        - R, F, Rv, Fv, a (abundanz) werden miteinbezogen
        - Fokus auf die Vergleichbarkeit
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Polygon
import yaml
from collections import Counter
import matplotlib.patches as mpatches
import numpy as np

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

# BE_1021 -> Standort 11
# BE_1049 -> Standort 7aB
# BE_1053 -> Standort 7g
# BE_1057 -> Standort 14?
# BE_1059 -> Standort 9a
# BE_2004 -> Standort 7as
title = "BE_2004"
# title = "test"
with open (f"/home/p/Documents/SemB/python/lists/{title}.yaml", 'r') as f:
    plants = yaml.safe_load(f)

# check the values
for plant in plants:
    if not (0 <= plant["r"] <= 5) or not (0 <= plant["f"] <= 5 or not (0 <= plant["a"] <= 7) or not (0 <= plant["rv"] <= 2) or not (0 <= plant["fv"] <= 2)):
        raise ValueError(f"Invalid values for {plant['name']}: r={plant['r']},f={plant['f']}, fv={plant['fv']}, rv={plant['rv']}, a={plant['a']}")

# Übersetzung der Koordinaten - überarbeitet
value_to_coordinate_f = {0:0, 1: 5, 1.5: 5, 2: 4.5, 2.5: 3.5, 3: 2.5, 3.5: 1.5,
                         4: 0.9, 4.5: 0.4, 5: 0}

value_to_coordinate_r = {0:0, 1: 0.5, 2: 1.5, 3: 2.5, 4: 4.5, 5: 4.5}

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
        r_val = value_to_coordinate_r[plant["r"]]
        f_val = value_to_coordinate_f[plant["f"]]
        x_points.append(r_val)
        y_points.append(f_val)  
    
# initiate the plantcounter to set the fillalpha properly
# fillalpha = 0.9 / len(plants)
basealpha = 0.05

# implement fixed alpha
fillalpha = basealpha 
rectfillcolor = ("#aaff00",fillalpha)

# Weighted mean
point_counter = Counter(zip(x_points, y_points))

# Exponential weighting: duplicate points weight much more
# power = 2 # what number is reasonable?
# x_weighted = sum(x * (count**power) for (x, y), count in point_counter.items())
# y_weighted = sum(y * (count**power) for (x, y), count in point_counter.items())
# total_weight = sum(count**power for count in point_counter.values())

# x_weighted /= total_weight
# y_weighted /= total_weight

# use the black rectangle instead
# ax.plot(x_weighted, y_weighted, 'ro', markersize=8)

# edgecolor of the Rectangles (currently disabled, increase alpha to enable)
edgecolor = (0,0,0,0)
rectedgecolor = edgecolor
# plot rectangles
def plotRectangles():
    valid_plants = [p for p in plants if p["r"] >= 1 and p["f"] >= 1]
    for (x, y), plant in zip(zip(x_points, y_points), valid_plants):
        # following is the code which determines the border locations of the
        # recangles
        if plant["fv"] == 1: 
            if plant["f"] == 1 or plant["f"] == 1.5: bottom = 4.5; top = 5
            elif plant["f"] == 2: bottom = 2.5; top = 5
            elif plant["f"] == 2.5: bottom = 1.5; top = 5
            elif plant["f"] == 3: bottom = 0.9; top = 4.5
            elif plant["f"] == 3.5: bottom = 0.4; top = 3.5
            elif plant["f"] == 4: bottom = 0; top = 2.5
            elif plant["f"] == 4.5: bottom = 0; top = 1.5
            elif plant["f"] == 5: bottom = 0; top = 0.9
            else: print("Error with input values"); return
        else: # covers fv values of 2, with +-1.5 variance instead of +-1
            # -1.5 instead of -1.6 -> easier to implement
            if plant["f"] == 1 or plant["f"] == 1.5: bottom = 4; top = 5
            elif plant["f"] == 2: bottom = 1.5; top = 5
            elif plant["f"] == 2.5: bottom = 0.9; top = 5
            elif plant["f"] == 3: bottom = 0.4; top = 5
            elif plant["f"] == 3.5: bottom = 0; top = 4.5
            elif plant["f"] == 4: bottom = 0; top = 3.5
            elif plant["f"] == 4.5: bottom = 0; top = 2.5
            elif plant["f"] == 5: bottom = 0; top = 1.5
            else: print("Error with input values"); return
        # note that there are no fractions of r-values
        if plant["rv"] == 1:
            if plant["r"] == 1: right = 1.5; left = 0
            elif plant["r"] == 2: right = 2.5; left = 0.5
            elif plant["r"] == 3: right = 4.5; left = 1.5
            elif plant["r"] == 4: right = 5; left = 2.5
            elif plant["r"] == 5: right = 5; left = 4.5
            else: print("Error with input values"); return
        else: # covers rv = 2 values
            if plant["r"] == 1: right = 2; left = 0
            # right = 3.5 -> is this the correct value?
            elif plant["r"] == 2: right = 3.5; left = 0
            elif plant["r"] == 3: right = 5; left = 1
            elif plant["r"] == 4: right = 5; left = 2
            elif plant["r"] == 5: right = 5; left = 3.5
            else: print("Error with input values"); return
            
        rect_coords = [(left, bottom), (right, bottom), 
                       (right, top), (left, top)]
        rect = Polygon(rect_coords, facecolor=rectfillcolor, edgecolor=rectedgecolor)
        ax.add_patch(rect)
        
    # plot the special x cases r = 0/x
    for plant in rxplants:  # Directly iterate plants added previously to the list
    # same code as above for the scaling
        if plant["fv"] == 1: 
            if plant["f"] == 1 or plant["f"] == 1.5: bottom = 4.5; top = 5
            elif plant["f"] == 2: bottom = 2.5; top = 5
            elif plant["f"] == 2.5: bottom = 1.5; top = 5
            elif plant["f"] == 3: bottom = 0.9; top = 4.5
            elif plant["f"] == 3.5: bottom = 0.4; top = 3.5
            elif plant["f"] == 4: bottom = 0; top = 2.5
            elif plant["f"] == 4.5: bottom = 0; top = 1.5
            elif plant["f"] == 5: bottom = 0; top = 0.9
            else: print("Error with input values"); return
        else: # covers fv values of 2, with +-1.5 variance instead of +-1
            # -1.5 instead of -1.6 -> easier to implement
            if plant["f"] == 1 or plant["f"] == 1.5: bottom = 4; top = 5
            elif plant["f"] == 2: bottom = 1.5; top = 5
            elif plant["f"] == 2.5: bottom = 0.9; top = 5
            elif plant["f"] == 3: bottom = 0.4; top = 5
            elif plant["f"] == 3.5: bottom = 0; top = 4.5
            elif plant["f"] == 4: bottom = 0; top = 3.5
            elif plant["f"] == 4.5: bottom = 0; top = 2.5
            elif plant["f"] == 5: bottom = 0; top = 1.5
            else: print("Error with input values"); return

        # Full width bar from x=0 to x=5
        rect_coords = [(0, bottom), (5, bottom), 
                       (5, top), (0, top)]
        rect = Polygon(rect_coords, facecolor=rectfillcolor, edgecolor=rectedgecolor)
        ax.add_patch(rect)
        
        # plot special f cases (f = x/0)
    for plant in fxplants:  # Directly iterate plants
        # note that there are no fractions of r-values
        # same code as above
        if plant["rv"] == 1:
            if plant["r"] == 1: right = 1.5; left = 0
            elif plant["r"] == 2: right = 2.5; left = 0.5
            elif plant["r"] == 3: right = 4.5; left = 1.5
            elif plant["r"] == 4: right = 5; left = 2.5
            elif plant["r"] == 5: right = 5; left = 4.5
            else: print("Error with input values"); return
        else: # covers rv = 2 values
            if plant["r"] == 1: right = 2; left = 0
            # right = 3.5 -> is this the correct value?
            elif plant["r"] == 2: right = 3.5; left = 0
            elif plant["r"] == 3: right = 5; left = 1
            elif plant["r"] == 4: right = 5; left = 2
            elif plant["r"] == 5: right = 5; left = 3.5
            else: print("Error with input values"); return
        
        # Full height bar from y=0 to y=5
        rect_coords = [(left, 0), (right, 0), (right, 5), (left, 5)]
        rect = Polygon(rect_coords, facecolor=rectfillcolor, edgecolor=rectedgecolor)
        ax.add_patch(rect)
                
plotRectangles()

# to calculate rect-overlay for legend
grid_size = 100
grid = np.zeros((grid_size, grid_size))

# Get all valid plants (same ones used in plotRectangles)
valid_plants = [p for p in plants if p["r"] >= 1 and p["f"] >= 1]

# For each plant, calculate its rectangle boundaries (same logic as in plotRectangles)
for (x, y), plant in zip(zip(x_points, y_points), valid_plants):
    # Copy-pasta the boundary calculation from plotRectangles:
    if plant["fv"] == 1: 
        if plant["f"] == 1 or plant["f"] == 1.5: bottom = 4.5; top = 5
        elif plant["f"] == 2: bottom = 2.5; top = 5
        elif plant["f"] == 2.5: bottom = 1.5; top = 5
        elif plant["f"] == 3: bottom = 0.9; top = 4.5
        elif plant["f"] == 3.5: bottom = 0.4; top = 3.5
        elif plant["f"] == 4: bottom = 0; top = 2.5
        elif plant["f"] == 4.5: bottom = 0; top = 1.5
        elif plant["f"] == 5: bottom = 0; top = 0.9
    else:
        if plant["f"] == 1 or plant["f"] == 1.5: bottom = 4; top = 5
        elif plant["f"] == 2: bottom = 1.5; top = 5
        elif plant["f"] == 2.5: bottom = 0.9; top = 5
        elif plant["f"] == 3: bottom = 0.4; top = 5
        elif plant["f"] == 3.5: bottom = 0; top = 4.5
        elif plant["f"] == 4: bottom = 0; top = 3.5
        elif plant["f"] == 4.5: bottom = 0; top = 2.5
        elif plant["f"] == 5: bottom = 0; top = 1.5
    
    if plant["rv"] == 1:
        if plant["r"] == 1: right = 1.5; left = 0
        elif plant["r"] == 2: right = 2.5; left = 0.5
        elif plant["r"] == 3: right = 4.5; left = 1.5
        elif plant["r"] == 4: right = 5; left = 2.5
        elif plant["r"] == 5: right = 5; left = 4.5
    else:
        if plant["r"] == 1: right = 2; left = 0
        elif plant["r"] == 2: right = 3.5; left = 0
        elif plant["r"] == 3: right = 5; left = 1
        elif plant["r"] == 4: right = 5; left = 2
        elif plant["r"] == 5: right = 5; left = 3.5
    
    # Convert to grid indices (0 to grid_size-1)
    left_idx = max(0, int(left / 5 * grid_size))
    right_idx = min(grid_size, int(right / 5 * grid_size))
    bottom_idx = max(0, int(bottom / 5 * grid_size))
    top_idx = min(grid_size, int(top / 5 * grid_size))
    
    # Add this rectangle to grid
    grid[bottom_idx:top_idx, left_idx:right_idx] += 1

# Get maximum overlap anywhere in the graph
max_overlap = int(np.max(grid))
print(f"Maximum rectangles overlapping: {max_overlap}")
 
# plot the special plants (both r=0 and f=0)
for plant in specialplants:
    rectedgecolor = (0,0,0,0)
    # These plants cover entire graph
    rect = Polygon([(0,0), (5,0), (5,5), (0,5)], 
                   facecolor=rectfillcolor, edgecolor=rectedgecolor)
    ax.add_patch(rect)
    
# legend section
legend_elements = []
patchlist = []
disableover20 = False
above15 = False
between0and5 = False
between6and10 = False
between11and15 = False
ifcounter: int = 0
# for the overlap legend entries
for count in range(1, max_overlap + 1):
    sample_alpha = 1 - (1 - fillalpha) ** count
    
    if count > 15 and count < 20 and above15 == False:
        # catch entries between 15 and 20
        patch = mpatches.Patch(color=("#aaff00", sample_alpha),
                               label='n=16-20')
        legend_elements.append(patch)
        above15 = True
    if count > 0 and count < 5 and between0and5 == False:
        # catch entries between 0 and 5
        patch = mpatches.Patch(color=("#aaff00", sample_alpha),
                               label='n=1-5')
        legend_elements.append(patch)
        between0and5 = True
    if count > 6 and count < 10 and between6and10 == False:
        # catch entries between 6 and 10
        patch = mpatches.Patch(color=("#aaff00", sample_alpha),
                               label='n=6-10')
        legend_elements.append(patch)
        between6and10 = True
    if count > 11 and count < 15 and between11and15 == False:
        # catch entries between 11 and 15
        patch = mpatches.Patch(color=("#aaff00", sample_alpha),
                               label='n=11-15')
        legend_elements.append(patch)
        between11and15 = True
    if count == 20 and max_overlap > 20:
        # Last entry
        patch = mpatches.Patch(color=("#aaff00", sample_alpha), 
                              label=f'n>{count}')
        legend_elements.append(patch)

for patch in patchlist:
    legend_elements.append(patch)

# add plant entries to the same list
for plant in plants:
    legend_elements.append(
        plt.Line2D([0], [0], marker='o', color='w', 
                   markerfacecolor='black', markersize=8, 
                   label=plant['name'])
    )

# add "Zentrum" to the legend
# legend_elements.append(
#     plt.Line2D([0], [0], marker='o', color='w',
#                markerfacecolor='red', markersize=10,
#                label='Zentrum (Mehrfache Punkte\nam selben Ort zählen ^2')
#     )
    
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
print("RXPLANTS: ", len(rxplants))
print("FXPLANTS: ", len(fxplants))
print("PLANTS WITH BOTH F AND R = 0: ",len(specialplants))
print("PLANTS: ", len(plants))