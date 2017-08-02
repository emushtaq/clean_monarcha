# coding=utf-8
import csv
import sqlite3
import os
import re
import errno
from datetime import datetime
import re

path_dataset = "/home/mushtaq/monarcha/MonarchaData/"
 
def make_list_of_persons(path):                                     
	output = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path, dI))]
	return output

def gather_files(type_of_data, person):
	print("%%%%%%%%%%%  Gathering files for " + person + "    %%%%%%%%%%%%%%%%%%%")
	retrieved_files = []
	for root, dirs, files in os.walk(path_dataset + person):
		for name in files:
			if name.find(type_of_data) != -1:
				retrieved_files.append(root + "/" + name)
	create_file(retrieved_files, person, type_of_data)

def create_file(files, person, type_of_data):
	print("%%%%%%%%%%%  Creating a file for " + person + " data:" + type_of_data  + "    %%%%%%%%%%%%%%%%%%%")
	if not os.path.exists("organized_data/" + person):
		os.makedirs("organized_data/" + person)

	output = open("organized_data/" + person + "/" + type_of_data  + ".txt", "a+")
	for filename in files:
		with open(filename) as file:
			for line in file:
				if not line.startswith("%"):
					line = re.split("\s+", line)
					line = ",".join(line)
					line = line[:-1]
					line = line + "\n"
					output.write(line) 	

def start():
	persons = make_list_of_persons(path_dataset)
	data_points = ["META", "MAG", "ACC", "WIFI", "LOC", "BAT", "BLTH"]
	for person in persons:
		for data_point in data_points:
			gather_files(data_point, person)

start()
print("Completed.")
