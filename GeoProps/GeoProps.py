import os
import numpy as np
#from shutil import copyfile

from ase.io import read, write

from ase.data import atomic_numbers, chemical_symbols
from asap3.analysis.rdf import RadialDistributionFunction
import matplotlib.pyplot as plt

#from ase.neighborlist import NeighborList
from GeoProps.No_Of_Neighbours import No_Of_Neighbours

class GeoProps_Program:
	def __init__(self, rdf_max_dist, no_of_bins, colours, r_cut, xlim_RDF=None, xlim_CN=None, suffix_name=''):
		self.rdf_max_dist = rdf_max_dist
		self.no_of_bins = no_of_bins
		self.colours = colours
		self.format_colour_scheme()
		self.r_cut = r_cut
		if xlim_RDF is None:
			self.xlim_RDF = (0,self.rdf_max_dist)
		else:
			self.xlim_RDF = xlim_RDF
		self.xlim_CN = xlim_CN

		self.modified_name_suffix = '_GeoProps'
		self.suffix_name = suffix_name
		self.run()

	def format_colour_scheme(self):

		self.colours_bar_plots = {element_pair: colour for element_pair, colour in self.colours.items() if isinstance(element_pair,str)}

		for element_pair, colour in list(self.colours.items()):
			if isinstance(element_pair,str):
				del self.colours[element_pair]
				element_pair = (element_pair,element_pair)
				self.colours[element_pair] = colour
		for (element1, element2), colour in list(self.colours.items()):
			del self.colours[(element1, element2)]
			element1 = atomic_numbers[element1]
			element2 = atomic_numbers[element2]
			self.colours[(element1, element2)] = colour

	def run(self):
		print('====================================================')
		for root, dirs, files in os.walk("."):
			if len(root.split('/')) <= 2:
				continue
			if self.modified_name_suffix in root:
				continue
			files.sort()
			for file in files:
				if file.endswith('.xyz') or file.endswith('.traj'):
					root_modified = root.split('/')
					root_modified[1] += self.modified_name_suffix+'_'+self.suffix_name
					root_modified = os.getcwd()+'/'+'/'.join(root_modified)
					root_modified = os.path.abspath(root_modified)
					self.run_upon_single_cluster(file, root, root_modified)
		print('====================================================')

	def run_upon_single_cluster(self, file, root, save_to):
		print('====================================================')
		path_to_xyz_file = root+'/'+file
		print('Saving cluster properties for '+path_to_xyz_file+' to '+save_to)
		cluster = self.read_in_chemical_system(path_to_xyz_file)
		if file.endswith('.xyz'):
			filename = file.replace('.xyz','')
		elif file.endswith('.traj'):
			filename = file.replace('.traj','')
		else:
			exit('Weird')
		save_to += '/'+filename
		self.make_folder(save_to)
		#copyfile(root+'/'+file,save_to+'/'+file)
		self.save_xyz_file(cluster, save_to+'/'+file)
		self.get_RDF(cluster, filename, save_to)
		self.get_nearest_neighbours(cluster, filename, save_to)
		self.bond_counting(cluster, filename, save_to)
		print('====================================================')

	def read_in_chemical_system(self, path_to_xyz_file):
		cluster = read(path_to_xyz_file)
		cluster.set_cell([50,50,50])
		cluster.set_pbc(False)
		return cluster

	def make_folder(self, save_to):
		if not os.path.exists(save_to):
			os.makedirs(save_to)

	def save_xyz_file(self, cluster, saving_path):
		for index in range(len(cluster)):
			cluster[index].tag = index
		write(saving_path,cluster)

	def get_RDF(self, cluster, filename, save_to):
		elements = list(set(cluster.get_chemical_symbols()))
		for index in range(len(elements)):
			elements[index] = atomic_numbers[elements[index]]
		element_pairs = []
		for element1 in elements:
			for element2 in elements:
				element_pairs.append((element1,element2))

		RDF_results = {}
		RDFobj = RadialDistributionFunction(cluster, self.rdf_max_dist, self.no_of_bins, verbose=True)
		for element_pair in element_pairs:
			rdf_pair = RDFobj.get_rdf(elements=element_pair)
			element_pair = tuple(sorted(element_pair))
			if not (element_pair in list(RDF_results.keys())):
				RDF_results[element_pair]  = rdf_pair
			else:
				RDF_results[element_pair] += rdf_pair

		#plotting
		x_axis = self.rdf_max_dist * np.linspace(0,1,self.no_of_bins,endpoint=True)
		for element_pair, rdf_pair in sorted(RDF_results.items()):
			element_pair_name = ', '.join(tuple(chemical_symbols[element] for element in element_pair))
			#rdf_pair = list(rdf_pair)
			print(self.colours[element_pair])
			plt.plot(x_axis, rdf_pair, self.colours[element_pair], label=element_pair_name)
			
		plt.xlim(self.xlim_RDF)
		plt.legend()
		plt.xlabel('Interatomic distance '+r'$(\AA)$')
		plt.ylabel('Radial distribution function')
		plt.tight_layout()
		file_path_name = save_to+'/'+filename+"_RDF"
		plt.savefig(file_path_name+".png")
		plt.savefig(file_path_name+".eps")
		plt.savefig(file_path_name+".svg")
		plt.cla(); plt.clf()

	def get_nearest_neighbours(self, cluster, filename, save_to):

		#nl = NeighborList([self.r_cut/2.0 + 0.00000001]*len(cluster))
		nl = No_Of_Neighbours([self.r_cut/2.0]*len(cluster))
		nl.update(cluster)
		all_number_of_neighbours = {}
		for index in range(len(cluster)):
			indices, offsets = nl.get_neighbors(index)
			number_of_neighbours = len(indices)
			all_number_of_neighbours.setdefault(number_of_neighbours,[]).append(index)

		#full_list = [j for sub in all_number_of_neighbours.values() for j in sub]
		#full_list.sort()
		#print(full_list)

		no_of_all_atoms_analysed = sum([len(xx) for xx in all_number_of_neighbours.values()])
		if not len(cluster) == no_of_all_atoms_analysed:
			print('Error')
			import pdb; pdb.set_trace()
			exit()

		if self.xlim_CN is None:
			max_CN_to_plot = max(all_number_of_neighbours.keys())
		else:
			max_CN_to_plot = self.xlim_CN

		elements = sorted(list(set(cluster.get_chemical_symbols())))
		all_elements_number_of_neighbours_list = {element: [] for element in elements}
		x_axis = list(range(max_CN_to_plot+1))
		for number_of_neighbours in x_axis:
			number_of_neighbours_list_element = {element: 0 for element in elements}
			if number_of_neighbours in all_number_of_neighbours:
				atom_indices_to_inspect = all_number_of_neighbours[number_of_neighbours]
				for atom_index in atom_indices_to_inspect:
					atom_index_symbol = cluster[atom_index].symbol
					number_of_neighbours_list_element[atom_index_symbol] += 1
			for key, value in number_of_neighbours_list_element.items():
				all_elements_number_of_neighbours_list[key].append(value)
		
		no_of_all_atoms_analysed = sum([sum(xx) for xx in all_elements_number_of_neighbours_list.values()])
		if not len(cluster) == no_of_all_atoms_analysed:
			print('Error')
			import pdb; pdb.set_trace()
			exit()

		all_y_axis = [0 for _ in range(len(x_axis))]
		no_of_elements = len(elements)
		for index in range(no_of_elements):
			element = elements[index]
			y_axis = all_elements_number_of_neighbours_list[element]
			all_y_axis = [y1+y2 for y1,y2 in zip(all_y_axis,y_axis)]
			plt.bar(x_axis, all_y_axis, width=0.8, bottom=None, align='center', color=self.colours_bar_plots[element], label=element, zorder=(no_of_elements-index))
		plt.ylim(0,max(all_y_axis)*1.05)
		'''
		yint = []
		locs, labels = plt.yticks()
		for each in locs:
			each = round(each,8)
			if each%1.0:
				yint.append(int(each))
		plt.yticks(yint)
		'''
		plt.xlabel('Number of neighbours')
		plt.ylabel('Number of atoms')
		plt.legend()
		plt.tight_layout()
		file_path_name = save_to+'/'+filename+"_No_of_Neighbours"
		plt.savefig(file_path_name+".png")
		plt.savefig(file_path_name+".eps")
		plt.savefig(file_path_name+".svg")
		plt.cla(); plt.clf()

		all_number_of_neighbours = sorted(all_number_of_neighbours.items())
		self.no_of_neighbours_filename = 'no_of_neighbours.txt'
		with open(file_path_name+'_'+self.no_of_neighbours_filename,'w') as no_of_neighboursTXT:
			no_of_neighboursTXT.write('The following file contains information about the number of neighbours that each atom contains in the cluster, as well as the atom indices of atoms in the cluster with those number of neighbours.\n')
			no_of_neighboursTXT.write('\n')
			no_of_neighboursTXT.write('To see each atom in your cluster, open the xyz file of your nanocluster/chemical system, and in View -> Colors, change the colouring of your cluster to "By tag".\n')
			no_of_neighboursTXT.write('\n')
			no_of_neighboursTXT.write('The colours represent the index for each atom, which corresponce to the atom indices in this document.\n')
			no_of_neighboursTXT.write('\n')
			no_of_neighboursTXT.write('No of neighbours\t|\tAtom Indices in Cluster/Chemical System\n')
			no_of_neighboursTXT.write('---------------------------------------------------------------\n')
			for no_of_neighbours, atom_indices in all_number_of_neighbours:
				#import pdb; pdb.set_trace()
				atom_indices = [str(atom_index)+' ('+str(cluster[atom_index].symbol)+')' for atom_index in atom_indices]
				no_of_neighboursTXT.write('\t\t'+str(no_of_neighbours)+'\t\t\t|\t\t'+str(', '.join(atom_indices))+'\n')
			no_of_neighboursTXT.write('\n')
			no_of_neighboursTXT.write('This is the same list as above, but without elements given for each atom\n')
			no_of_neighboursTXT.write('\n')
			no_of_neighboursTXT.write('No of neighbours\t|\tAtom Indices in Cluster/Chemical System\n')
			no_of_neighboursTXT.write('---------------------------------------------------------------\n')
			for no_of_neighbours, atom_indices in all_number_of_neighbours:
				atom_indices = [str(xx) for xx in atom_indices]
				no_of_neighboursTXT.write('\t\t'+str(no_of_neighbours)+'\t\t\t|\t\t\t'+str(', '.join(atom_indices))+'\n')

	def bond_counting(self, cluster, filename, save_to): 
		all_bonds = {}
		no_of_atoms = len(cluster)
		for index1 in range(no_of_atoms):
			for index2 in range(index1+1,no_of_atoms):
				atom1 = cluster[index1]
				atom2 = cluster[index2]
				length = cluster.get_distance(index1,index2)
				if length <= self.r_cut:
					symbol1 = atom1.symbol
					symbol2 = atom2.symbol
					symbol_pair = tuple(sorted([symbol1,symbol2]))
					all_bonds.setdefault(symbol_pair,[]).append(length)
		total_bonds = sum([len(a) for a in all_bonds.values()])
		print('Total Number of Bonds = '+str(total_bonds))
		all_bonds = list(all_bonds.items())
		all_bonds.sort(key=lambda x:x[0])
		
		with open(save_to+'/'+filename+'_Bond_Counting.txt','w') as OUTPUT:
			OUTPUT.write('This text file contains all the information about the number of bonds in this cluster/chemical system.\n')
			OUTPUT.write('\n')
			OUTPUT.write('Total Number of Bonds = '+str(total_bonds)+'\n')
			OUTPUT.write('\n')
			for key,value in all_bonds:
				OUTPUT.write('Number of '+str(key)+' Bonds = '+str(len(value))+'\n')
			OUTPUT.write('\n')
			OUTPUT.write('Bond lengths\n')
			OUTPUT.write('\n')
			for key, value in all_bonds:
				OUTPUT.write(str(key)+': '+str(sorted(value))+'\n')





