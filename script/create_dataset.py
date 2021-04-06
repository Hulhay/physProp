#!/usr/bin/env python3

import multiprocessing as mp
import physical_properties as pp
import csv
import sys
import os

def write_csv_dataset(output_file, source_path, properties):

	images = os.listdir(source_path)
	fullname_images = []
	for image in images:
		fullname_images.append(source_path+'/'+image)

	if properties == 'p':
		to_compute = pp.absolute_porosity
	elif properties == 'ssa':
		to_compute = pp.surface_area
	elif properties == 't':
		to_compute == pp.tortuosity

	with mp.Pool() as pool:
		val_property = pool.map(to_compute, fullname_images)

	for i in range(len(images)):
		print('{},{:.2f}'.format(images[i], val_property[i]))

	with open(output_file, 'w') as f:
		for i in range(len(images)):
			f.write('{},{:.2f}\n'.format(images[i], val_property[i]))

write_csv_dataset(sys.argv[1], sys.argv[2], sys.argv[3])