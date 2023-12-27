import sys
sys.path.append("../")
from libraries.libraries import *

base_url = ["https://www.pcb.com.pk/players.php?pg=1&ipp=100&&new_page_limit=100"]
page_url = ["https://www.pcb.com.pk/players.php?pg={}&ipp=100&&new_page_limit=100"]

original_directory = os.getcwd()
os.chdir("..")
file_path = os.getcwd() + "/temp/" + "playertable.csv"

os.chdir(original_directory)


player_ids = []
player_names = []
player_links = []
# player_total_records = []

class gettingData():
	def __init__(self):
		pass
	def dataFetch(url):
		raw_data = requests.get(url)
		raw_html = raw_data.text

		page_format = r'page_limit=100">(.*?)</a>'
		page_range = re.findall(page_format, raw_html)
		page_range = page_range[:-1]
		page_range = list(map(int, page_range))
		
		last_page = max(page_range)

		total_pages = list(range(1, last_page+1))

		for page in total_pages:
			page_link = page_url[0].format(page)
			print(page_link)
			raw_data = requests.get(page_link)
			raw_html = raw_data.text

			soup = BeautifulSoup(raw_html, "html.parser")

			for a_tag in soup.find_all("a", {"class": "profileLink"}):
				player_id = a_tag["href"].split('player_id=')[1].split('¬e=')[0]
				player_ids.append(player_id)
				player_name = a_tag.text
				player_names.append(player_name)
				player_link = a_tag["href"]
				player_links.append(player_link)

				# raw_data = requests.get(player_link)
				# raw_html = raw_data.text

				# soup = BeautifulSoup(raw_html, "html.parser")

				# for a_tag in soup.find_all("a", string="Matches Detail"):
				# 	match_details = a_tag["href"]

				# 	raw_data = requests.get(match_details)
				# 	raw_html = raw_data.text

				# 	soup = BeautifulSoup(raw_html, "html.parser")

				# 	match_types = ["TEST matches", "First-class matches", "ODI matches", "List A matches", "T20I matches", "T20 matches", "Four Day matches", "Three Day matches", "Two Day matches", "One Day matches"]
				# 	total_records = []

				# 	for match_type in match_types:
				# 		for a_tag in soup.find_all("a", string=match_type):
				# 			format_link = a_tag["href"]

				# 			raw_data = requests.get(format_link)
				# 			raw_html = raw_data.text

				# 			match_type_soup = BeautifulSoup(raw_html, "html.parser")
							


				# 			for total_record in match_type_soup.find_all("div", {"class": "totalno"}):
				# 				total_records.append(int(total_record.text[-1]))

				# 	print(sum(total_records))
				# 	player_total_records.append(sum(total_records))



class generatingCsv():
	def __init__(self):
		pass
	def checkCsv(filePath):
		if os.path.isfile(filePath):
			os.remove(filePath)
			data = list(zip(player_ids, player_names, player_links))
			with open(filePath, "w") as tempData:
				t_data = csv.writer(tempData)
				t_data.writerow(["player_id", "player_name", "player_link"])
				t_data.writerows(data)
		else:
			data = list(zip(player_ids, player_names, player_links))
			with open(filePath, "w") as tempData:
				t_data = csv.writer(tempData)
				t_data.writerow(["player_id", "player_name", "player_link"])
				t_data.writerows(data)


gettingData.dataFetch(base_url[0])
generatingCsv.checkCsv(file_path)