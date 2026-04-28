#
# https://medium.com/data-science/quantum-physics-visualization-with-python-35df8b365ff
#
from vpython import sqrt, exp, random, pi, arange, vec

# Probability of 1s
def prob_1s(x, y, z):
    r = sqrt(x * x + y * y + z * z)
    # Remember: probability is psi squared!
    return (exp(-r) / sqrt(pi)) * (exp(-r) / sqrt(pi))


def np_linspace(start, stop, num):
    return [x for x in arange(start, stop, (stop - start) / (num - 1))] + [stop]

#Random coordinates
x = np_linspace(0,1,30)
y = np_linspace(0,1,30)
z = np_linspace(0,1,30)

scatter_points_amount = 10000
elements = []
probability = []

probability_sum = 0
for ix in x:
    for iy in y:
        for iz in z:
            #Serialize into 1D object
            elements.append(vec(ix, iy, iz))
            prob = prob_1s(ix, iy, iz)
            probability.append(prob)
            probability_sum += prob

#Ensure sum of probability is 1
#probability = probability/sum(probability) #Getting electron coordinates based on probabiliy
for i in range(len(probability)):
    probability[i] /= probability_sum
    probability[i] *= scatter_points_amount

coord = np.random.choice(elements, size=100000, replace=True, p=probability)
elem_mat = [i.split(',') for i in coord]
elem_mat = np.matrix(elem_mat)
x_coords = [float(i.item()[1:]) for i in elem_mat[:,0]]
y_coords = [float(i.item()) for i in elem_mat[:,1]]
z_coords = [float(i.item()[0:-1]) for i in elem_mat[:,2]]#Plotting

dots = []
for _ in range(10000):

    dots.append(simple_sphere(radius=0.01, pos=))
for _

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_coords, y_coords, z_coords, alpha=0.05, s=2)
ax.set_title("Hydrogen 1s density")
plt.show()