import json
from functools import lru_cache
from pathlib import Path


def _load_regions():
	data_path = Path(__file__).resolve().parent.parent / 'data' / 'china-regions.json'
	with data_path.open(encoding='utf-8') as fp:
		return json.load(fp)


@lru_cache(maxsize=1)
def get_region_helper():
	raw = _load_regions()
	provinces_by_code = raw.get("00", {})
	province_city_map = {}
	for code, name in provinces_by_code.items():
		cities = raw.get(code, {})
		province_city_map[name] = list(cities.values())
	return RegionHelper(provinces_by_code, province_city_map)


class RegionHelper:
	def __init__(self, provinces_by_code, province_city_map):
		self.provinces_by_code = provinces_by_code
		self.province_city_map = province_city_map
		self.cascader_options = self._build_cascader_options()

	def _build_cascader_options(self):
		options = []
		for code, province_name in self.provinces_by_code.items():
			children = [{'value': city, 'label': city} for city in self.province_city_map.get(province_name, [])]
			options.append({
				'value': province_name,
				'label': province_name,
				'children': children
			})
		return options

	def validate(self, province, city, county=None):
		if not province or province not in self.province_city_map:
			raise ValueError('请选择有效的省份')
		if not city or city not in self.province_city_map.get(province, []):
			raise ValueError('请选择有效的城市')
		if not county:
			raise ValueError('区/县不能为空')

	def get_cascader(self):
		return self.cascader_options
