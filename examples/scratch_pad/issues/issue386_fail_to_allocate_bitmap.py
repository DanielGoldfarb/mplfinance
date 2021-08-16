import numpy
import matplotlib
from matplotlib import pyplot

#matplotlib.use("Agg")  # This does indeed fix the problem but it would be better to fix the problem properly
image = numpy.zeros((256,256,3))
print('backend=',matplotlib.get_backend())
print('matplotlib.__version__ =',matplotlib.__version__)
print('numpy.__version__ =',numpy.__version__)
for i in range(500):
	print(i)
	pyplot.subplot(1, 1, 1) # rows, cols, itemno
	pyplot.axis('off')
	pyplot.imshow(image)
	pyplot.savefig('plot_%d.png' % (i), dpi=250)
	pyplot.close()
