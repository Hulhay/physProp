#!/usr/bin/env python3

from PIL import Image
import sys
import mahotas as mh
from pylab import imshow, show
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def absolute_porosity(filename):
	CITRA = Image.open(filename).convert('L')
	PIXEL = CITRA.load()

	horizontal, vertical = CITRA.size

	porous = 0
	for x in range(horizontal):
		for y in range(vertical):
			if PIXEL[x,y] == 255:
				porous += 1

	total_size = horizontal * vertical
	porosity = porous / total_size
	porosity *= 100

	return porosity

def surface_area(filename, resolution=1):
	CITRA = mh.imread(filename)
	perimCITRA = mh.bwperim(CITRA)

	horizontal, vertical = len(perimCITRA), len(perimCITRA[0])

	perimeter, grain_area = 0, 0
	for x in range(horizontal):
		for y in range(vertical):
			if perimCITRA[x, y] == True:
				perimeter += 1
			if CITRA[x, y] == 0:
				grain_area += 1

	ssa = perimeter/resolution/grain_area
	ssa *= 1000

	return ssa

def tortuosity(filename):
	CITRA = Image.open(filename).convert('L')
	PIXEL = CITRA.load()

	horizontal, vertical = CITRA.size

	maze = []
	for x in range(horizontal):
		col = []
		for y in range(vertical):
			if PIXEL[y,x] == 255:
				col.append(1)
			else:
				col.append(0)
		maze.append(col)

	left_side_list = []
	right_side_list = []

	i = 0
	while i < len(maze):
		if maze[i][0] == 1:
			left_side_list.append(i)
		if maze[i][len(maze[0])-1] == 1:
			right_side_list.append(i)
		i += 1

	if len(left_side_list) == 0 or len(right_side_list) == 0:
		return 0

	dist_list = []
	for i in left_side_list:
		for j in right_side_list:
			grid = Grid(matrix=maze)
			start = grid.node(0, i)
			end = grid.node(len(maze[0])-1, j)
			finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
			path = finder.find_path(start, end, grid)
			path = list(path)
			dist_list.append(len(path[0]))

	dist_list = [i for i in dist_list if i != 0]

	if len(dist_list) == 0:
		return 0

	avg_x = sum(dist_list) / len(dist_list)
	tor_x = avg_x / len(maze)

	return tor_x

def avg_pore_size(filename):

	# Using Octave
	# Open file aps.m and
	# create_aps_datasets.m

	pass