# This script was developed to allow better storage of images:
# 1) Set Created and Modified Date to match the Date Taken [With a little help from: https://gist.github.com/ikoblik/7089165]
# 2) Based on the CreatedDate, add an ordered prefix to the picture name to allow cross-system sorting# 
#
# Usage: 
# # 1a) Update the Created and Modified DateTimes when there is a DateTaken provided (DateTimeOriginal) - in current folder
# python MediaFilePrefixer.py setTimeStamps
# # 1b) Update the Created and Modified DateTimes for images stored in a different folder (script converts proper directory indication)
# python MediaFilePrefixer.py setTimeStamps 'D:/Pictures/Event'
#
# # Update file names based on the created date
# # 2a) Add prefix to file names (including movies) based on Created Date - in current folder
# python MediaFilePrefixer.py prefixFiles
# # 2b) Add prefix to file names (including movies) based on Created Date - in specified folder
# python MediaFilePrefixer.py prefixFiles 'D:/Pictures/Event'
#
# @Author 	Reinier van den Assum
# @Created	August 2019

import os, stat, time, re, glob, sys 
from stat import *
from exif import Image

from datetime import datetime, timedelta

__dir__ = '.'
__dateFormat__ = '%Y-%m-%d %H:%M:%S'

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
		print( newFN )
		os.rename( __dir__ + '/' + fileName, __dir__ + '/' + newFN )
		i += 1
		
######
# EXIF METHODS 
######
def getExifCreationDate( path ):
	"""Gets the earliest date from the file's EXIF header, returns time tuple"""
	timeStamp = None
	try:
		with open( path, 'rb' ) as image_file:
			my_image = Image( image_file )
		originalTime = my_image.datetime_original
		if( originalTime ):
			timeStamp = datetime.strptime( originalTime, __dateFormat__ )
	except Exception as e :
		print( 'Failed to retrieve datetime_original via Exif for '+ path.replace( __dir__, '' ) )
		print( '>> '+ str( e ) )
		return timeStamp
  
	# sometimes exif lib failes to retrieve data
	if( not timeStamp ):
		response = os.popen( 'exif' + ' -x "%s"' % path, 'r' )
		lines = response.read()
		matches = re.findall('<Date_and_Time.+?>(.*?)</Date_and_Time.+?>', lines)
		if( len( matches ) ) :
			timeStamp = min( * [datetime.strptime( x, __dateFormat__ ) for x in matches ] )
	return timeStamp

def getFileDates(path):
	"""Returns a dictionary of file creation (ctime), modification (mtime), exif (exif) dates"""
	dates = {}
	dates['exif'] = getExifCreationDate(path)
	dates['mtime'] = datetime.fromtimestamp( os.path.getmtime( path ) )
	dates['ctime'] = datetime.fromtimestamp( os.path.getctime( path ) )
	
	if not dates['exif']:
		dates['exif'] = min( dates['mtime'], dates['ctime'] )
	return dates
  
def setFileDates( path, dates ):
	"""Sets file modification and creation dates to the specified value"""
	newTime = time.mktime( dates['exif'].timetuple() )
	# update modified and accessed time
	os.utime( path, ( newTime, newTime ) )
	try:
		# update created time
		from win32_setctime import setctime	
		setctime( path, newTime )
		return 'CMA'
	except:
		return 'MA !Created'

#####
# MAIN METHODS
#####
# python MediaFilePrefixer.py rename
def rename():
	print( '== Start adding prefixes to images and video files ==' )
	print( '== Folder '+ __dir__ )
	# Get Images (files and correct extension)
	imageList = filter( fileFilter, os.listdir( __dir__ ) )
	# Sort Images by Created Date and Rename files
	renameFiles( sorted( imageList, key=lambda p: os.stat( __dir__ + '/' + p ).st_ctime ) )
	
def setTimeStamps():
	print( '== Start running setTimestamps ==' )
	print( '== Folder '+ __dir__ )
	# Get Images (files and correct extension)
	imageList = filter( fileFilter, os.listdir( __dir__ ) )
	
	for fileName in imageList:
		result = ''
		fullPath =  __dir__ + '/' + fileName
		dates = getFileDates( fullPath )
		if( dates[ 'exif' ] ):
			# calculate difference between created and modify date
			cmp_time = lambda x, y: abs( x - y ) > timedelta(minutes=10)
			diff = [ cmp_time( dates[x], dates['exif'] ) for x in ('mtime', 'ctime') ]
			if( sum( diff ) ):
				result += dates['exif'].strftime( __dateFormat__ ) + ' vs. '+ dates['mtime'].strftime( __dateFormat__ ) + ' vs. '+ dates['mtime'].strftime( __dateFormat__ )
				result += ' '+ setFileDates( fullPath, dates )
			else:
				result = 'Less than 10 minutes difference between dates'
		else:
			result += 'No EXIF found'
			
		print( fileName + ' - ' + result )

## EXECUTION
try:
	args = sys.argv
	methodName = args[1]
	if len( args ) == 3:
		__dir__ = args[2].replace( '\\', '/' ) # Replace Windows to Unix file references

	if methodName == 'prefixFiles' :
		rename();
	elif methodName == 'setTimeStamps':
		setTimeStamps();
	else:
		print('No method selected')
except Exception as e:
	print( e )
