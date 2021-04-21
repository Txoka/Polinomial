import matplotlib.pyplot as plt
from math import sqrt

class Polinomial:
	def __init__(self,arr):
		if type(arr) is Polinomial:
			self.coef=arr.coef.copy()
			self.degree=len(arr.coef)
		else:
			self.coef=arr
			self.degree=len(arr)
	def getcoef(self,i):
		if i>=self.degree:return 0
		return self.coef[i]
	def __add__(self,poli):
		if type(poli) is int:return Polinomial([self.coef[0]+poli]+self.coef[1:])
		if type(poli) is Division:return Division(poli.dividend+self*poli.divisor,poli.divisor)
		l=[]
		for i in range(max(self.degree,poli.degree)):
			l.append(self.getcoef(i)+poli.getcoef(i))
		return Polinomial(l)
	def __sub__(self,poli):
		if type(poli) is int:return Polinomial([self.coef[0]-poli]+self.coef[1:])
		if type(poli) is Division:return Division(poli.dividend+self*poli.divisor,poli.divisor)
		l=[]
		for i in range(max(self.degree,poli.degree)):
			l.append(self.getcoef(i)-poli.getcoef(i))
		return Polinomial(l)
	def upgrade(self):
		self.degree+=1
		self.coef.insert(0,0)
	def downgrade(self):
		self.degree-=1
		self.coef.pop(0)
	def __mul__(self,poli):
		if type(poli) is Division:return Division(self*poli.dividend,poli.divisor)
		if type(poli) is int or type(poli) is float:
			l=[]
			for i in self.coef:
				l.append(i*poli)
			return Polinomial(l)
		if type(poli) is Polinomial:
			a,b=self,Polinomial(poli)
			res=Polinomial([])
			for i in a.coef:
				res+=b*i
				b.upgrade()
			return res
	def __truediv__(self,b):
		if type(b) is Polinomial:return Division(self,b)
		if type(b) is Division:return Division(b.divisor*self,b.dividend)
		if type(b) is int or type(b) is float:return self*1/b
	def __call__(self,x):
		res=0
		if type(x) is Polinomial:res=Polinomial([0])
		if type(x) is Division:res=Division(Polinomial([0]),Polinomial([1]))
		for i in range(len(self.coef)-1,-1,-1):
			res*=x
			res+=self.coef[i]
		return res
	def __str__(self,rev=False):
		if self.degree==0:return ""
		res=""
		if self.coef[0]!=0:res=str(self.coef[0])
		for i,e in enumerate(self.coef[1:]):
			if e!=0:
				if e>0:res+="+"
				res+=str(e)+"x"
				if i!=0:res+="^{"+str(i+1)+"}"
		if self.coef[0]==0:return res[1:]
		return res
		
class Division:
	def __init__(self,a,b):
		self.dividend=a
		self.divisor=b
	def __mul__(self,div):
		if type(div) is Polinomial or type(div) is int or type(div) is float:return Division(self.dividend*div,self.divisor)
		if type(div) is Division:return Division(self.dividend*div.dividend,self.divisor*div.divisor)
	def __truediv__(self,div):
		if type(div) is Polinomial or type(div) is int or type(div) is float:return Division(self.dividend,self.divisor*div)
		if type(div) is Division:return Division(self.dividend*div.divisor,self.divisor*div.dividend)
	def __add__(self,poli):
		if type(poli) is Polinomial:return Division(self.dividend+poli*self.divisor,self.divisor)
		if type(poli) is Division:return Division(self.dividend*poli.divisor+self.divisor*poli.dividend,self.divisor*poli.divisor)
	def simplify(self):
		while self.dividend.coef[0]==0 and self.divisor.coef[0]==0:
			self.dividend.downgrade()
			self.divisor.downgrade()
	def __call__(self,x):
		return self.dividend(x)/self.divisor(x)
	def __str__(self):
		return "\\frac{"+str(self.dividend)+"}{"+str(self.divisor)+"}"

a=Polinomial([0,1])
x=Polinomial([0,1])

for i in range(5):
	a=(a+x/a)/2
	a.simplify()

arr1=[]
arr2=[]
for i in range(1024):
	arr1.append(sqrt(i))
	arr2.append(a(i))

plt.plot(arr1)
plt.plot(arr2)
plt.show()

a=Polinomial([0,1])
b=Polinomial([0,4,-4])

for i in range(4):
	a=b(a)

print(a)