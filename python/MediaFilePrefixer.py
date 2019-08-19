# This script was developed to allow better storage of images
# Based on the CreatedDate, an ordered prefix is added to the picture name to allow cross-system sorting
# @Author 	Reinier van den Assum
# @Created	August 2019

# @TODO: Add input parameters, dynamic directory & to allow testing (print suggested list of new names vs. directly rename files)

import os, stat, time, re
from stat import *

#####
# UTIL METHODS
#####
# Handle File Extensions
allowed_extensions = [ "jpg", "jpeg", "png", "gif" ] + [ "mov", "mp4" ]
def getExtension( filename ):
	return os.path.splitext( filename )[1][1:].strip().lower()

# Only return existing Files of allowed extensions
def fileFilter( fileName ):
	return os.path.isfile and getExtension( fileName ) in allowed_extensions
	
def printTime( t ):
	return time.asctime( time.localtime( t ) )

def origFileName( fileName, length ):
	return re.sub( r'^([0-9]{'+ str( length ) +'}\_)', '', fileName )

def populatePrefix( i, length ):
	return str( i ).zfill( length ) + '_'

def renameFiles( sortedFileList ):
	# Get the maximum length of the prefix
	lenPrefix = len( str( len( sortedFileList ) ) )
	
	i = 1;
	for fileName in sortedFileList:
		newFN = populatePrefix( i, lenPrefix ) + origFileName( fileName, lenPrefix )
		print( newFN ) #+ printTime( os.stat( fileName ).st_ctime )
		os.rename( fileName, newFN )
		i += 1

#####
# MAIN
#####
def main():
	# Get Images (files and correct extension
	imageList = filter( fileFilter, os.listdir( '.' ) )
	# Sort Images by Created Date and Rename files
	renameFiles( sorted( imageList, key=lambda p: os.stat(p).st_ctime ) )
	
main();