import tensorflow as tf
import json
import numpy as np
import shutil

with open("vocab_913_clintox.json", "r") as f:
  voc=json.load(f)

model=tf.keras.models.load_model("model_clintox-0.9130_us.h5")

shutil.copy("../Generate/output/generated.txt", "input/gen.txt")
def encode(row):
  r2=row
  for i in range(len(row)):
    r2[i]=voc[row[i]]
  return r2
def one_hot(x):
  x3d=np.zeros((x.shape[0], x.shape[1], len(voc)+1))
  for i in range(x.shape[0]):
    for j in range(x.shape[1]):
      x3d[i][j][x[i][j]]=1
  
  return x3d
def predict(d):
  l=list(d)
  e=encode(l)
  e=np.expand_dims(e, axis=0)
  p=x_train=tf.keras.preprocessing.sequence.pad_sequences(e, 210)
  oh=one_hot(p)
  pred=model.predict(oh)
  p=1 if pred[0][1]>=0.6 else 0
  return p

with open("input/gen.txt", "r") as f:
	mol=f.read()

mols=mol.split("\n")
op=[]
for mol in mols:
	t=predict(mol)
	print(mol+" : "+str(t))
	if t==1:
		op.append(mol)

with open("output/output.txt", "w") as f:
	f.write("\n".join(op))
