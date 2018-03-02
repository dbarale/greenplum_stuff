########################## TEST DATA ##############################
'''
Normal File Path
C:\\Users\\rachel.ayersman\\Documents\\Dev Work\\GPDump.txt

File Folder
C:\\Users\\rachel.ayersman\\Desktop\\GPDumpFiles

Test Missing End
C:\\Users\\rachel.ayersman\\Documents\\Dev Work\\GPDumpAlterFnRemove.txt

Test Missing Begin
C:\\Users\\rachel.ayersman\\Documents\\Dev Work\\GPDumpTypeFnRemove.txt
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
    str_dup_new_file_loc = str_new_file_loc + '\\Duplicate File Name'
    new_dup_file_loc = os.makedirs(str_dup_new_file_loc)
    return str_new_file_loc, str_dup_new_file_loc

##Counts the files created
def count_files_created(str_new_file_loc):
    sql_file_cnt = list(i for i in os.listdir(path=str_new_file_loc) if i.endswith('.sql'))
    dup_folder = str_new_file_loc + '\\Duplicate File Name'
    function_created_cnt = len(sql_file_cnt)
    if os.path.exists(dup_folder):
        dup_sql_file_cnt = list(i for i in os.listdir(path=dup_folder) if i.endswith('.sql'))
        dup_function_created_cnt = len(dup_sql_file_cnt)
    return function_created_cnt + dup_function_created_cnt, dup_function_created_cnt

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
		if skip_line == True: ##checks if this is the line right after the header line containing --
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
	
			##Checks if file already exists, moves the original into the dup folder, & creates dup in the dup folder
			if os.path.exists(build_new_file):
				file_move_path = str_new_file_loc + '\\Duplicate File Name' + file_name 
				os.rename(build_new_file, file_move_path)
				if os.path.exists(file_move_path): ## Checks if there is already a dup file
					build_new_file = file_move_path.replace('sql', str(loop_cnt)) + '.sql' ## Adds number to the end of file so that it doesn't overwrite existing files
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

def name_overloaded_functions(str_dup_new_file_loc):
	list_of_dup_files = os.listdir(str_dup_new_file_loc)
	loop_count = 0
	for file in list_of_dup_files:
		file_dup_name = list_of_dup_files[loop_count]
		dup_file_path = str_dup_new_file_loc + '\\' + file_dup_name
		frd = open(dup_file_path, 'r')
		read_dup_file = frd.readline() ##Blank Line
		read_dup_file = frd.readline() ##Create Line
		comma_count = 0
		for char in read_dup_file:
			if char == ',':
				comma_count += 1
		comma_count += 1 ##There will always be one less comma then parameter
		frd.close() ##Closes file
		split_file_path = dup_file_path.replace('.', ' ').split()
		if split_file_path[-2].isdigit(): ##Finds numbed dup
			split_file_name = file_dup_name.split('.')
			file_dup_name = split_file_name[0] + '.' + split_file_name[1] + '(' + str(comma_count) + ')' + '.sql' 
		else: ##Finds original dup
			split_file_name = file_dup_name.split('.')
			file_dup_name = split_file_name[0] + '.' + split_file_name[1] + '(' + str(comma_count) + ')' + '.sql'
		new_file_path = str_new_file_loc + '\\' + file_dup_name 
		os.rename(dup_file_path, new_file_path)
		frd.close()
		##del list_of_dup_files[loop_count]
		loop_count += 1
	
	os.removedirs(str_dup_new_file_loc)
	return


	
###################### Code Begin ####################################

##Gets File Locations
str_new_file_loc, str_dup_new_file_loc = get_new_file_location()

##Gets File
dump_file = get_file()

##File Health Check
file_health_check(dump_file)

##Reads Dump File and Writes Function Files
read_dump_file_write_fn(str_new_file_loc, dump_file)

##Counts Files Created
function_created_cnt, duplicate_function_created_cnt = count_files_created(str_new_file_loc)

##Renames Overloaded Files
##name_overloaded_functions(str_dup_new_file_loc)

print('\n' + 'SUMMARY')
print('Total Functions Created: ' + str(function_created_cnt))
print('Total Overloaded Functions Created: ' + str(duplicate_function_created_cnt))
