import tensorflow as tf
import json
import numpy as np
import shutil
import time

class Tox:
	def __init__(self):
		with open("Tox/vocab_913_clintox.json", "r") as f:
			self.voc=json.load(f)

		self.model=tf.keras.models.load_model("Tox/model_clintox-0.9130_us.h5")

	
	def encode(self, row):
		r2=row
		for i in range(len(row)):
		  r2[i]=self.voc[row[i]]
		return r2
	def one_hot(self, x):
		x3d=np.zeros((x.shape[0], x.shape[1], len(self.voc)+1))
		for i in range(x.shape[0]):
		  for j in range(x.shape[1]):
		    x3d[i][j][x[i][j]]=1
		
		return x3d
	def predict(self, d):
		l=list(d)
		e=self.encode(l)
		e=np.expand_dims(e, axis=0)
		p=x_train=tf.keras.preprocessing.sequence.pad_sequences(e, 210)
		oh=self.one_hot(p)
		pred=self.model.predict(oh)
		p=1 if pred[0][1]>=0.6 else 0
		return p

	def calculate(self):
		time.sleep(2)
		shutil.copy("Generate/output/generated.txt", "Tox/input/gen.txt")
		with open("Tox/input/gen.txt", "r") as f:
			mol=f.read()

		mols=mol.split("\n")
		op=[]
		for mol in mols:
			if len(mol)>0:
				t=self.predict(mol)
				print(mol+" : "+str(t))
				if t==1:
					op.append(mol)
			
			else:
				print("Invalid Mol")

		with open("Tox/output/output.txt", "w") as f:
			f.write("\n".join(op))
			
#tox=Tox()
#tox.calculate()
