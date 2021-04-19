import os
import numpy as np
from shutil import copyfile

from ase.io import read

from ase.data import atomic_numbers, chemical_symbols
from asap3.analysis.rdf import RadialDistributionFunction
import matplotlib.pyplot as plt

from ase.neighborlist import NeighborList

class GeoProps_Program:
	def __init__(self, rdf_max_dist, no_of_bins, colours, r_cut, xlim_RDF=None, xlim_CN=None):
		self.rdf_max_dist = rdf_max_dist
		self.no_of_bins = no_of_bins
		self.colours = colours
		self.format_colour_scheme()
		self.r_cut = r_cut
		if xlim_RDF == None:
			self.xlim_RDF = (0,self.rdf_max_dist)
		else:
			self.xlim_RDF = xlim_RDF
		self.xlim_CN = xlim_CN
		self.run()

	def run(self):
		print('====================================================')
		for root, dirs, files in os.walk("."):
			if len(root.split('/')) <= 2:
				continue
			for file in files:
				if file.endswith('.xyz') or file.endswith('.traj'):
					root_modified = root.split('/')
					root_modified[1] += '_GeoProps'
					root_modified = os.getcwd()+'/'+'/'.join(root_modified)
					self.run_upon_single_cluster(file, root, root_modified)
		print('====================================================')

	def run_upon_single_cluster(self, file, root, save_to):
		print('====================================================')
		path_to_xyz_file = root+'/'+file
		print('Saving cluster properties for '+path_to_xyz_file)
		cluster = read(path_to_xyz_file)
		cluster.set_cell([50,50,50])
		cluster.set_pbc(False)
		if file.endswith('.xyz'):
			filename = file.replace('.xyz','')
		elif file.endswith('.traj'):
			filename = file.replace('.traj','')
		else:
			exit('Weird')
		save_to += '/'+filename
		self.make_folder(save_to)
		self.get_RDF(cluster, filename, save_to)
		self.get_nearest_neighbours(cluster, filename, save_to)
		copyfile(root+'/'+file,save_to+'/'+file)
		print('====================================================')

	def make_folder(self, save_to):
		if not os.path.exists(save_to):
			os.makedirs(save_to)

	def format_colour_scheme(self):
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

		nl = NeighborList([self.r_cut]*len(cluster))
		nl.update(cluster)
		all_number_of_neighbours = {}
		for index in range(len(cluster)):
			indices, offsets = nl.get_neighbors(index)
			number_of_neighbours = len(indices)
			if number_of_neighbours in all_number_of_neighbours.keys():
				all_number_of_neighbours[number_of_neighbours] += 1
			else:
				all_number_of_neighbours[number_of_neighbours] = 1

		if self.xlim_CN == None:
			max_CN_to_plot = max(all_number_of_neighbours.keys())
		else:
			max_CN_to_plot = self.xlim_CN
		all_number_of_neighbours_list = []
		for number_of_neighbours in range(max_CN_to_plot):
			value = all_number_of_neighbours.get(number_of_neighbours,0)
			all_number_of_neighbours_list.append(value)
		plt.bar(range(max_CN_to_plot),all_number_of_neighbours_list, width=0.8, bottom=None, align='center')

		plt.ylim(0,max(all_number_of_neighbours_list)*1.05)
		yint = []
		locs, labels = plt.yticks()
		for each in locs:
			each = round(each,8)
			if each%1.0:
				yint.append(int(each))
		plt.yticks(yint)

		plt.xlabel('Number of neighbours')
		plt.ylabel('Number of atoms')
		plt.tight_layout()
		file_path_name = save_to+'/'+filename+"_No_of_Neighbours"
		plt.savefig(file_path_name+".png")
		plt.savefig(file_path_name+".eps")
		plt.savefig(file_path_name+".svg")
		plt.cla(); plt.clf()