"""
Version 4.3:
    features:
        - Plotskala nach Vorschlag Valentin
        - Individuelle Transparenz
            -> Hilft beim finden des Standortes
            -> Transparenz abhängig von der Grösse der Pflanzenliste
            -> Transparenz auch abhängig von der Abundanz
        - R, F, Rv, Fv, a (abundanz) werden miteinbezogen
        - Fokus auf die Standortbestimmung
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Polygon
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
    if not (0 <= plant["r"] <= 5) or not (0 <= plant["f"] <= 5):
        raise ValueError(f"Invalid values for {plant['name']}: r={plant['r']}, f={plant['f']}")

# Übersetzung der Koordinaten - old -> delete after testing
# value_to_coordinate = {0:0, 1: 0, 1.5: 0.25, 2: 0.5, 2.5: 1.5, 3: 2.5, 
#                        3.5: 3.5, 4: 4.5, 4.5: 4.75, 5: 5}

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
basealpha = 1 - (1 - 0.9)**(1/len(plants))
maxabundance = 7

# Weighted mean
point_counter = Counter(zip(x_points, y_points))

# Exponential weighting: duplicate points weight much more
# power = 2 # what number is reasonable?
# x_weighted = sum(x * (count**power) for (x, y), count in point_counter.items())
# y_weighted = sum(y * (count**power) for (x, y), count in point_counter.items())
# total_weight = sum(count**power for count in point_counter.values())

# x_weighted /= total_weight
# y_weighted /= total_weight

# ax.plot(x_weighted, y_weighted, 'ro', markersize=8)

# edgecolor of the Rectangles (currently disabled, increase alpha to enable)
edgecolor = (0,0,0,0)
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
            
        # implement abundance-depending alpha
        abundance = plant["a"]
        fillalpha = basealpha * (abundance / maxabundance)
        rectfillcolor = ("#aaff00",fillalpha)
        rectedgecolor = edgecolor
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

        
        # implement abundance-depending alpha
        abundance = plant["a"]
        fillalpha = basealpha * (abundance / maxabundance)
        rectfillcolor = ("#aaff00",fillalpha)
        rectedgecolor = edgecolor
        print("fillalpha: ", fillalpha)
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

        # implement abundance-depending alpha
        abundance = plant["a"]
        fillalpha = basealpha * (abundance / maxabundance)
        rectfillcolor = ("#aaff00",fillalpha)
        rectedgecolor = edgecolor
        
        # Full height bar from y=0 to y=5
        rect_coords = [(left, 0), (right, 0), (right, 5), (left, 5)]
        rect = Polygon(rect_coords, facecolor=rectfillcolor, edgecolor=rectedgecolor)
        ax.add_patch(rect)
        
plotRectangles()

# plot the special plants (both r=0 and f=0)
for plant in specialplants:
    abundance = plant["a"]
    fillalpha = basealpha * (abundance / maxabundance)
    rectfillcolor = ("#aaff00",fillalpha)
    rectedgecolor = (0,0,0,0)
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
