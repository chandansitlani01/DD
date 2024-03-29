import threading
from Generate.gen import Generate 
from Tox.tox_pred import Tox 
from DTI.dti_pred import DTI

import streamlit as st
import time
import shutil
import datetime

from rdkit.Chem import MolFromSmiles
from rdkit.Chem.Draw import MolsToGridImage
import os





st.set_page_config(page_title="Drug Discovery", layout="wide", page_icon="logo.png")
col1, col2, col3 = st.columns([12, 3, 7])

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
	footer {visibility: hidden;}

        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

open("DTI/output/out.txt", "w").close()
with col3:
	st.title("Draw Molecule")
	smi=st.text_input("Enter Smiles String of Molecule", value="C1(=O)CCCCC1")
	mol=MolFromSmiles(smi)
	if mol is None:
		st.text("Invalid Molecule")
	else:
		img=MolsToGridImage([mol])
		st.image(img)
with col1:
	st.title("Drug Discovery")
	n_iterations=st.text_input("Enter no. of Iterations", value=7, help="No of iterations to check")
	n_iterations=int(n_iterations)
	n_iterations+=2
	t=st.text_input("Enter Target Sequence")

	tem=0.7
	gen=Generate(tem)
	tox=Tox()
	dti=DTI()
	st.warning("Dont make any action on the page after run until the program is complete else progress may get discarded.")
	if st.button("Run"):
		
		for i in range(n_iterations):
			
			
			s=time.time()
			st.text("Started Iteration "+str(i))
			st.text("-------------------")
			if i==0:
				gen.generate()
				
			elif i==1:
				t1=threading.Thread(target=gen.generate)
				t2=threading.Thread(target=tox.calculate)
				
				t1.start()
				t2.start()
				
				t1.join()
				t2.join()
				
			elif i==n_iterations-2:
				t1=threading.Thread(target=tox.calculate)
				t2=threading.Thread(target=dti.calculate, args=(t,))
				
				t1.start()
				t2.start()
				
				t1.join()
				t2.join()
			elif i==n_iterations-1:
				dti.calculate(t)
			
			else:
				t1=threading.Thread(target=gen.generate)
				t2=threading.Thread(target=tox.calculate)
				t3=threading.Thread(target=dti.calculate, args=(t,))
				
				t1.start()
				t2.start()
				t3.start()
				
				t1.join()
				t2.join()
				t3.join()
			
			
			with open("Generate/output/generated.txt", "r") as f:
				geno=f.read()
				geno=geno.split("\n")
				
			
			with open("Tox/output/output.txt", "r") as f:
				toxo=f.read()
				toxo=toxo.split("\n")
				
				
			dtio=""
			with open("DTI/output/out.txt", "r") as f:
				dtio=f.read()
				dtio=dtio.split("\n")
				
				
			e=time.time()
			m=len(dtio) if len(dtio[0])>0 else 0
			m=max(m-1, 0)
			st.text("Generated Molecules : "+str(len(geno)))
			if i>0:
				st.text("Non Toxic Molecules : "+str(len(toxo)))
			if i>1:
				st.text("Final Molecules : "+str(m))
			st.text("Time Taken : "+str(round(e-s, 2)))
			st.text(" ")
			st.text(" ")
			print()
			print()
			
		
		
		
		

		with open("DTI/output/out.txt", "r") as f:
			st.download_button("Download Outputs", f, file_name="output.txt")
			
		
		print(dti.outs)
		
		
		st.warning("Please Download the file using the Download Button else it can be deleted as soon as any other action is taken on the page")
			
			

