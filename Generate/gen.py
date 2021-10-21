  
import tensorflow as tf
import numpy as np
import json
import time
from rdkit import Chem
import os
#text encoded and padded

class Generate:

	def __init__(self, tem):
		self.model=tf.keras.models.load_model("Generate/model_gen.h5")
		self.tem=tem
		

		with open("Generate/voc_gen.json", "r") as f:
			self.voc=json.load(f)

		self.cov={}
		for k, v in self.voc.items():
			self.cov[v]=k
	def one_hot(self, x):
		x3d=np.zeros((x.shape[0], x.shape[1], len(self.voc)+1))
		for i in range(x.shape[0]):
			for j in range(x.shape[1]):
				x3d[i][j][x[i][j]]=1
		
		return x3d

	def sample(self, a, temperature=1.0):
		  # helper function to sample an index from a probability array
		a = np.log(a) / temperature
		a = np.exp(a) / np.sum(np.exp(a))
		a/=a[0].sum()
		try:
			return np.argmax(np.random.multinomial(1, a[0], 1))
		except:
			return np.argmax(a)

	def predict(self, st):
		init=st
		#init="O)n[C@H]2CCN(c3ccccc3)CC2)CC1EE"
		init=list(init)

		for i in range(30):
			init[i]=self.voc[init[i]]
		init=np.array(init)
		init=np.expand_dims(init, axis=0)
		#x=tf.keras.preprocessing.sequence.pad_sequences([init], maxlen=60)
		x=self.one_hot(init)
		p=self.model.predict(x)
		pred=self.sample(p, self.tem)
		return self.cov[pred]




	
	def generate(self):
		string="cccccccccccccccccccccEEccc1O=S"
		n=200
		s=time.time()
		for i in range(n):
			temp=string[-30:]
			c=self.predict(temp)
			string+=c
			if i%1000==0:
				print(i)
		mols=string.split("EEEEEEEESSSSSSSS")
		mols=mols[1:-1]
		e=time.time()
		print("time taken = "+str(e-s))
		print("Total mols = "+str(len(mols)))
		print(mols)
		valid=[]
		inv=0
		for mol in mols:
			try:
				m=Chem.MolFromSmiles(mol)	
				if m is not None:
					valid.append(mol)
			except:
				inv+=1
		print(len(valid), len(mols))
		valids="\n".join(valid)
		with open("Generate/output/generated.txt", "w") as f:
			f.write(valids)
		
#gen=Generate()
#gen.generate()

