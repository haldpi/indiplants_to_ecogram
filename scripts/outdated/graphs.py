import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Plot the foundation of the Graph
# The y-axis
ax = plt.gca()
# Note the offset, needs consideration in further calculations??
ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.0, 5.5])
ax.set_yticklabels(['Sehr\nTrocken', 'Trocken', 'Frisch', 'Feucht', 'Nass', '', ''])
ax.invert_yaxis()

# The x-axis
# Because of offset calculate -1 to each x-axis!!
ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.0, 5.5])
ax.set_xticklabels(['Sauer', '', '', '', 'basisch', '', ''])
offset = 0.5

# dictionary with all polygons
polygons = [
    {"coords": [[0,5], [1.3,5], [1.1,4.1], [0,3.8]], "color": "#e3b8da"},
    {"coords": [[5,5], [1.3,5], [1.1,4.1], [1.1,3.9], [5,3.9]], "color": "#2ec2f0"},
    {"coords": [[1.1,3.9], [5,3.9], [5,3.5], [1.3,3.5], [1.1,3.8]], "color": "#8ce1f9"},
    {"coords": [[4.5,3.5], [5,3.5], [5,2.9], [4.5,2.9]], "color": "#9ad590"},
    {"coords": [[4.5, 3.5], [1.3, 3.5], [1.1, 3.8], [0.7, 3.5], [0.7, 2.9], [4.5, 2.9]], "color": "#93dac3"},
    {"coords": [[4.5,2.9], [5,2.9], [5,2.3], [4.5,2.3]], "color": "#e0e682"},
    {"coords": [[0,3.8], [1.1,4.1], [1.1,3.8], [0.7,3.4], [0.7,2.8], [0,2.5]], "color": "#ffc9d3"},
    {"coords": [[0.7,2.9], [4.5,2.9], [4.5,2.3], [3.4,2.3], [1.6,1.8], [0.9,2.1], [0.7,2.3]], "color": "#aee4d6"},
    {"coords": [[0,2.5], [0.7,2.8], [0.7,2.3], [0.9,2.1], [0.9,1], [0,1.1]], "color": "#ffa19d"},
    {"coords": [[1.6,1.8], [3.4,2.3], [5,2.3], [5,1.6], [2.3,1.6]], "color": "#fffbe2"},
    {"coords": [[2.3,1.6], [5,1.6], [5,0.9], [2.3,0.9]], "color": "#fff5a8"},
    {"coords": [[0.9,2.1], [1.6,1.8], [2.3,1.6], [2.3,0.9], [1.5,0.9], [0.9,1]], "color": "#ffdf7a"},
    {"coords": [[1.5,0.9], [5,0.9], [5,0], [2,0]], "color": "#fff078"},
    {"coords": [[0,1.1], [0.9,1], [1.5,0.9], [2,0], [0,0]], "color": "#ff776e"},
    {"coords": [[0,5], [5,5], [5,4.5], [0,4.5]], "color": "#0055ff"},
    {"coords": [[0,0.5], [5,0.5], [5,0], [0,0]], "color": "#ff3131"}
]

# add all polygons to the graph
for p in polygons:
    poly = Polygon(p["coords"], closed=True, facecolor=p["color"])
    ax.add_patch(poly)
    
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
x_points = [2-offset, 1-offset, 2-offset]
y_points = [2-offset, 3-offset, 3.5-offset]
ax.plot(x_points, y_points, 'ko', markersize=6)  # 'ko' sets the color

# calculate the mean
x_points_mean = sum(x_points) / len(x_points)
y_points_mean = sum(y_points) / len(y_points)
ax.plot(x_points_mean, y_points_mean, 'ro', markersize=8)

# draw the area 
triangle_coords = [[x_points[0], y_points[0]],
                   [x_points[1], y_points[1]], 
                   [x_points[2], y_points[2]]]
area = Polygon(triangle_coords, closed=True, 
               facecolor='#ffffff', alpha=0.5, edgecolor='black')
ax.add_patch(area)

# Create legend entries
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Melampyrum pratense'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Vaccinium myrtillus'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Dryopteris dilatata'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Zentrum')
]

ax.legend(handles=legend_elements, loc='upper right')


# testpont: Bei F und R wert = 1, je 0.5 abziehen! (offset=0.5)
# ax.plot([1-offset], [1-offset], 'ro', markersize=10)

# set Axis labels
plt.ylabel("Feuchtigkeit")
plt.xlabel("")

# show the plot
plt.show()