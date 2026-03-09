import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
    
# Draw dots
# "Vegetationsaufnahmen 91_94.pdf"
# 1: Melampyrum pratense F 2, R 2
# 2: Rhty lore -> nicht gefunden
# 3: pleu schr -> nicht gefunden
# 4: hypn cupr -> nicht gefunden
# 5: dicr scop -> nicht gefunden
# 6: vaccinium myrtillus F 3, R 1
# 7: poly form -> nicht gefunden
# 8: hylo sple -> nicht gefunden
# 9: dryopteris dilitata aggr. F 3.5, R 2
# 10: thui tama -> nicht gefunden
# x_points = [2-offset, 1-offset, 2-offset]
# y_points = [2-offset, 3-offset, 3.5-offset]


# "1021.pdf"
# 1: Athyrium filix-femina F 3, R 2
# 2: Dryopteris filix-mas F 3.5, R 3
# 3: Oxalis acetosella F 3, R 2
# 4: Viol silv nicht gefunden -> Viola sylvestris F 3, R x
# 5: Polygonatum multiflorum F 3, R 4
# 6: Galium odoratum F 3, R 3
# 7: Anemone nemorosa F 3, R x
# 8: Lamium montanum F 3, R 3.5
# 9: Paris quadrifolia F 3.5, R 4
# 10: Primula elatior F 3.5, R 3 (aggr.) oder R 4
# 11: Milium effusum F 3, R 2
# 12: Carex sylvatica F 3.5, R 3
# 13: Galeopsis tetrahit F 3 , R 3
# 14: Pulmonaria obscura F 3.5, R 4
# 15: Arum maculatum F 3, R 3 (aggr.) oder R 4
# 16: Allium ursinum F 4, R 4
# 17: Mniu undu -> nicht gefunden
# 18: Circaea lutetiana F 3.5, R 4
# 19: Adoxa moschatellina F 3.5, R 4
# 20: Moehringia trinervia F 3, R 3 (aggr.) oder R 2
# 21: Mercurialis perennis F 3 (aggr.) oder F 3.5, R 4
# 22: Brachypodium sylvaticum F 3.5, R 3
# Zwei weitere Pflanzen nicht entzifferbar

# Die aggr. varianten wurden ignoriert
plants = [
    {"name": "Athyrium filix-femina", "f": 3, "r": 2},    
    {"name": "Dryopteris filix-mas", "f": 3.5, "r": 3},
    {"name": "Oxalis acetosella", "f": 3, "r": 2},
#     {"name": "Viola sylvestris", "f": 3, "r": 0},
    {"name": "Polygonatum multiflorum", "f": 3, "r": 4},
    {"name": "Galium odoratum", "f": 3, "r": 3},
#     {"name": "Anemone nemorosa ", "f": 3, "r": 0},
    {"name": "Lamium montanum", "f": 3, "r": 3.5},
    {"name": "Paris quadrifolia", "f": 3.5, "r": 4},
    {"name": "Primula elatior", "f": 3.5, "r": 4},
    {"name": "Milium effusum", "f": 3, "r": 2},
    {"name": "Carex sylvatica", "f": 3.5, "r": 3},
    {"name": "Galeopsis tetrahit", "f": 3, "r": 3},
    {"name": "Pulmonaria obscura", "f": 3.5, "r": 4},
    {"name": "Arum maculatum", "f": 3, "r": 3},
    {"name": "Allium ursinum", "f": 4, "r": 4},
    {"name": "Circaea lutetiana ", "f": 3.5, "r": 4},
    {"name": "Adoxa moschatellina", "f": 3.5, "r": 4},
    {"name": "Moehringia trinervia", "f": 3, "r": 2},
    {"name": "Mercurialis perennis", "f": 3.5, "r": 4},
    {"name": "Brachypodium sylvaticum", "f": 3.5, "r": 3}    
]

################## TESTING GROUND - Values incorrect
# plants = [{"name": "Athyrium filix-femina", "f": 3, "r": 3}]




# define the coordinate lists
x_points = []
y_points = []

# Validate input values
for plant in plants:
    if not (1 <= plant["r"] <= 5) or not (1 <= plant["f"] <= 5):
        raise ValueError(f"Invalid values for {plant['name']}: r={plant['r']}, f={plant['f']}")
# for each plant in the dictionary, add the x and y values to the coordinate list
# the 6 - plant[...] part is for inversion of the values, so i don't have
# to invert the y-aaxis
for plant in plants:
    r_val = plant["r"] - offset
    f_val = 6 - plant["f"] - offset
    x_points.append(r_val)
    y_points.append(f_val)


# plot the actual points
ax.plot(x_points, y_points, 'ko', markersize=6)  # 'ko' sets the color

# calculate the mean
x_points_mean = sum(x_points) / len(x_points)
y_points_mean = sum(y_points) / len(y_points)
ax.plot(x_points_mean, y_points_mean, 'ro', markersize=8)

# draw the area 
# triangle_coords = [[x_points[0], y_points[0]],
#                    [x_points[1], y_points[1]], 
#                    [x_points[2], y_points[2]]]
# area = Polygon(triangle_coords, closed=True, 
#                facecolor='#ffffff', alpha=0.5, edgecolor='black')
# ax.add_patch(area)

# Create legend entries
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Melampyrum pratense'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Vaccinium myrtillus'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Dryopteris dilatata'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Zentrum')
]

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

# show the plot
plt.show()