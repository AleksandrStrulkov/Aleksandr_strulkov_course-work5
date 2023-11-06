import requests
from pprint import pprint
import json


class HeadhunterVacancy:
	"""Получение вакансий с платформы HeadHunter API"""
	HH_URL = "https://api.hh.ru/vacancies"
	HH_COMPANY = "https://api.hh.ru/employers"
	HH_AREAS = "https://api.hh.ru/suggests/areas"
	company_id = 'company_id_hh.json'

	def __init__(self, city_name):
		self.city_name = city_name

	def __repr__(self):
		return f"Указанный город: {self.city_name}"

	@property
	def get_city_id(self):
		"""Получение id города для получения в нем вакансий"""
		params = {
				"text": self.city_name
		}
		hh_areas_url = self.HH_AREAS
		response = requests.get(hh_areas_url, params=params)

		for city in response.json()["items"]:
			if city["text"] == self.city_name:
				return city["id"]

	@property
	def get_json(self):
		"""
		Функция получения id работодателя на платформе headhunter
		:return: list
		"""
		company_id_list = []
		with open(self.company_id, 'r', encoding='utf-8') as file:
			company_json = json.load(file)
			for item in company_json:
				company_id_list.append(item['id'])
		return company_id_list

	def company_information(self):
		"""
		Функция получения всех данных о работодателях
		:return: list
		"""
		company_info = []
		for item in self.get_json:
			hh_areas_url = self.HH_COMPANY + "{item}"
			response = requests.get(hh_areas_url)
			info_company = response.json()
			company_info.append(info_company['name'])
		return company_info

	def get_vacancies(self):
		"""Получение всех вакансий работодателей"""
		vacancies_list = []
		hh_vac_url = self.HH_URL
		employee_list = self.get_json
		for num in range(len(employee_list)):
			params = {
					"employer_id": employee_list[num],
					"per_page": 100,
					"only_with_salary": True,
					"area": self.get_city_id
			}
			response = requests.get(hh_vac_url, params=params)
			if response.status_code == 200:
				vacancies = response.json()
				for item in vacancies["items"]:
					if item["salary"]["from"]:
						vacancies_list.append(item)

		return vacancies_list


company_id_add = HeadhunterVacancy("Россия")
# print(len(company_id.get_vacancies()))
# pprint(company_id_add.get_vacancies(), indent=2)
# company = company_id_add.get_vacancies()
# pprint(company.get_all_vacancies(2000762), indent=2)
# print(len(company_id_add.company_information()))
print(len(company_id_add.get_vacancies()))
pprint(company_id_add.get_vacancies(), indent=2)
