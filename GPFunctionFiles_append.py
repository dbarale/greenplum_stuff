########################## TEST DATA ##############################
'''
Normal File Path
C:\\Users\\dbarale\\Documents\\Dev Work\\GPDump.txt

File Folder
C:\\Users\\dbarale\\Documents\\Dev\\Desktop\\GPDumpFiles

Test Missing End
C:\\Users\\dbarale\\Documents\\Dev Work\\GPDumpAlterFnRemove.txt

Test Missing Begin
C:\\Users\\dbarale\\Documents\\Dev Work\\GPDumpTypeFnRemove.txt
'''
###################################################################

from datetime import datetime
import os

##Asks User for file path for the dump file and opens to read
def get_file():
    dump_file = input('Dump Filename: ')
    fr = open(dump_file, 'r')
    read_file = fr.readline()
    return dump_file

def file_health_check(dump_file):
    ##Variables for Summary Stats and Error Checks
    fn_begin_cnt = 0
    fn_create_cnt = 0
    fn_end_cnt = 0

    ##Gets Dump file path and opens to read
    health_file_path = dump_file
    hfr = open(health_file_path, 'r')
    read_health_file = hfr.readline()
	
    ##Creates string values to stop and start reading on
    health_fn_begin = 'Type: FUNCTION;'
    health_fn_creation_found = 'CREATE FUNCTION'
    health_fn_end = 'ALTER FUNCTION'

    for line in hfr:
        if health_fn_begin in line:
			fn_begin_cnt += 1
        if health_fn_creation_found in line:
            fn_create_cnt += 1
        if health_fn_end in line:
            fn_end_cnt += 1
    if fn_begin_cnt == fn_create_cnt:
        if fn_begin_cnt == fn_end_cnt:
            print('Health check completed. No Errors.')
        else:
            print('Error.')
    return
    

##Asks User for the file path that they want the new files to be created in, creates the file and returns the str of file path
def get_new_file_location():
    new_file_location = input('New File Location: ')
    now_datetime = datetime.now()
    time_folder = datetime.strftime(now_datetime,'%Y''%m''%d ''%H''%M''%S')
    str_new_file_loc = str(new_file_location) + '\\' + time_folder
    new_file_location = os.makedirs(str_new_file_loc)
    return str_new_file_loc

##Counts the files created
def count_files_created(str_new_file_loc):
    sql_file_cnt = list(i for i in os.listdir(path=str_new_file_loc) if i.endswith('.sql'))
    function_created_cnt = len(sql_file_cnt)
    return function_created_cnt

def read_dump_file_write_fn(str_new_file_loc, dump_file):
	
	loop_cnt = 0
	
	##Gets Dump file path and opens to read
	file_path = dump_file
	fr = open(file_path, 'r')
	read_file = fr.readline()
	
	##Creates string values to stop and start reading on
	fn_begin = 'Type: FUNCTION;'
	fn_end = 'ALTER FUNCTION'
	
	## Flags for when to stop/start reading
	fn_read_started = False
	skip_line = False
	
	## Walks through all lines in dump file. Either skips the line, writes the lines, creates the file, or stops writing
	for line in fr:
		if skip_line: ##checks if this is the line right after the header line containing --
			skip_line = False
			continue
	
		if fn_read_started: ##writes after function begin string has been found
			fw.writelines(line)
	
		## Begin Function Found
		if fn_begin in line:
	
			##Creates New File/FilePath
			line_list = line.replace('(',' ').replace(';', ' ').split() ##replaces unwanted characters in the header file with spaces then splits on spaces
			name_start = line_list.index('Name:')
			schema_start = line_list.index('Schema:')
			file_name = '\\' + line_list[schema_start+1]+ '.' + line_list[name_start+1] + '.sql' ##Finds the item in the list after Name: and after Schema: 
			build_new_file = str_new_file_loc + file_name
	
			##Checks if file already exists
			if os.path.exists(build_new_file):
				fw = open(build_new_file, 'a+')
			else:
				fw = open(build_new_file, 'w')
	
			##Set Flags
			skip_line = True
			fn_read_started = True
			loop_cnt =+ 1
    
		## End Function Found
		if fn_end in line:
	
			fw.close()       
	
			##Set Flag
			fn_read_started = False
	
	fr.close()
	return
	
###################### Code Begin ####################################

##Gets File Locations
str_new_file_loc = get_new_file_location()

##Gets File
dump_file = get_file()

##File Health Check
file_health_check(dump_file)
##Reads Dump File and Writes Function Files
read_dump_file_write_fn(str_new_file_loc, dump_file)

##Counts Files Created
function_created_cnt = count_files_created(str_new_file_loc)

##Renames Overloaded Files
#name_overloaded_functions(str_dup_new_file_loc)

print('\n' + 'SUMMARY')
print('Total Functions Created: ' + str(function_created_cnt))
