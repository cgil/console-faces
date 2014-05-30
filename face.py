import argparse


class Feature(object):
	def __init__(self, size):
		self.size = size
		self.mid = self.size/2

	#	Mirror the left half of the face on the right side
	def mirror(self, side):
		flip = []
		for s in side:
			flip.append(s[::-1])
		return flip

	def combine(self,lSide, rSide):
		mouth = []
		for i in xrange(len(lSide)):
			temp = lSide[i]
			temp.extend(rSide[i])
			mouth.append(temp)
		return mouth

	def form(self, expression):
		return getattr(self, expression)()

	def addSpace(self, feature):
		feature.append(["*"]*self.mid)

class Hair(Feature):
	def __init__(self, size):
		super(Hair, self).__init__(size)

	def addHair(self, hair, hairType):
		hair.append([hairType]*self.mid)

	def curly(self):
		hair = []
		self.addHair(hair, "@")
		self.addHair(hair, "@")
		self.addHair(hair, "@")
		self.combine(hair, self.mirror(hair))
		return hair

class Mouth(Feature):
	def __init__(self, size):
		super(Mouth, self).__init__(size)

	def addDimple(self, mouth):
		mouth.append(["*"]*self.mid)
		mouth[-1][1] = " "

	def addLip(self, mouth):
		mouth.append(["*"]*self.mid)
		for i in xrange(1, self.mid):
			mouth[-1][i] = " "

	def happy(self):
		mouth = []
		self.addDimple(mouth)
		self.addLip(mouth)
		self.addSpace(mouth)
		self.addSpace(mouth)
		self.addSpace(mouth)
		self.combine(mouth, self.mirror(mouth))
		return mouth

	def mad(self):
		mouth = []
		mouth.append(["*"]*self.mid)
		mouth.append(["*"]*self.mid)
		for i in xrange(self.mid):
			if i % 2 == 0:
				mouth[-2][i] = " "
			if (i+1) % 2 == 0:
				mouth[-1][i] = " "

		self.addSpace(mouth)
		self.addSpace(mouth)
		self.combine(mouth, self.mirror(mouth))
		return mouth

	def smirk(self):
		lSide = []
		rSide = []
		self.addSpace(lSide)
		self.addSpace(lSide)
		self.addLip(lSide)
		self.addSpace(lSide)

		self.addDimple(rSide)
		self.addDimple(rSide)
		self.addLip(rSide)
		self.addSpace(rSide)
		self.addSpace(rSide)

		mouth = self.combine(lSide, self.mirror(rSide))
		return mouth

	def sad(self):
		mouth = []
		self.addSpace(mouth)
		self.addLip(mouth)
		self.addDimple(mouth)
		self.addSpace(mouth)
		self.combine(mouth, self.mirror(mouth))
		return mouth
		

class Nose(Feature):
	def __init__(self, size):
		super(Nose, self).__init__(size)

	def normal(self):
		nose = []
		nose.append(["*"]*self.mid)
		nose.append(["*"]*self.mid)
		nose[-1][self.mid-1] = " "
		nose.append(["*"]*self.mid)
		self.combine(nose,self.mirror(nose))
		return nose

class Eyes(Feature):
	def __init__(self, size):
		super(Eyes, self).__init__(size)

	def addEye(self, eyes, size=1, pupil=None):
		pos = self.mid/2
		eyes.append(["*"]*self.mid)
		for i in xrange(size):
			eyes[-1][pos-size/2+i] = " "
		if pupil is not None and pupil >= 0 and pupil <= size:
			eyes[-1][pos-size/2+pupil] = "@"

	def normal(self):
		eyes = []
		self.addSpace(eyes)
		self.addSpace(eyes)
		self.addEye(eyes, 5)
		self.addEye(eyes, 5, 2)
		self.addEye(eyes, 5)
		self.addSpace(eyes)
		self.combine(eyes, self.mirror(eyes))
		return eyes
		
class Face(object):
	expressions = ['happy', 'sad', 'smirk', 'mad']
	def __init__(self, expression=None, eyesE=None, noseE=None, mouthE=None):
		self.size = 20
		self.form(expression, eyesE, noseE, mouthE)

	def form(self, expression=None, eyesE=None, noseE=None, mouthE=None, hairE=None):
		if expression and expression in Face.expressions:
			eyes, nose, mouth, hair = self.__create(expression)
		if eyesE:
			eyes = Eyes(self.size).form(eyesE)
		if noseE:
			nose = Nose(self.size).form(noseE)
		if mouthE:
			mouth = Mouth(self.size).form(mouthE)
		if hairE:
			hair = Hair(self.size).form(hairE)
		self.face = []
		self.face.extend(hair)
		self.face.extend(eyes)
		self.face.extend(nose)
		self.face.extend(mouth)
		self.__addCheeks(5)
		self.__curve()

	def __addCheeks(self, size):
		for row in self.face:
			row[:0] = "*"*size
			row.extend("*"*size)

	def __create(self, expression):
		if expression == "happy":
			return Eyes(self.size).form("normal"), Nose(self.size).form("normal"), \
				Mouth(self.size).form("happy"), Hair(self.size).form("curly")
		elif expression == "sad":
			return Eyes(self.size).form("normal"), Nose(self.size).form("normal"), \
				Mouth(self.size).form("sad"), Hair(self.size).form("curly")
		elif expression == "smirk":
			return Eyes(self.size).form("normal"), Nose(self.size).form("normal"), \
				Mouth(self.size).form("smirk"), Hair(self.size).form("curly")
		elif expression == "mad":
			return Eyes(self.size).form("normal"), Nose(self.size).form("normal"), \
				Mouth(self.size).form("mad"), Hair(self.size).form("curly")

	def __curve(self):
		self.face = self.face[::-1]
		for y in xrange(len(self.face)):
			for x in xrange(len(self.face[0])):
				if y < self.__func(x):
					self.face[y][x] = " "
		self.face = self.face[::-1]

	def __scale(self, val, src, dst):
	    """
	    Scale the given value from the scale of src to the scale of dst.
	    scale(0, (0.0, 99.0), (-1.0, +1.0))
	    """
	    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

	def __func(self, x):
		faceHeight = len(self.face) - 1
		faceWidth = len(self.face[0]) - 1
		func = lambda x: (x-(faceWidth/2))**4
		y = func(x)

		y = self.__scale(y, (0.0, func(faceWidth)), (0, faceHeight))
		return y

	def show(self):
		for row in self.face:
			for col in row:
				print col,
			print "\n",


parser = argparse.ArgumentParser(description='Makes faces.')
parser.add_argument("expression", help="Facial expression to make {happy, sad, smirk, mad}")
args = parser.parse_args()

face = Face(args.expression).show()



