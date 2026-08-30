"""
commodity API 回归：公开商品接口不得泄漏进价等内部字段。
"""
from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from .models import CommodityCategories, CommodityInfos


class PublicCommodityOutputTests(APITestCase):
	"""匿名可访问的商品列表/详情/搜索不得包含 cost_price 等内部字段。"""

	def setUp(self):
		self.category = CommodityCategories.objects.create(title="主食")
		self.product = CommodityInfos.objects.create(
			sku_title="牛肉罐头", main_image="product_photos/m.png",
			detail_images="product_photos_details/m.png",
			# 9.37 不会出现在其他任何字段里，方便对序列化结果做子串断言
			cost_price=Decimal("9.37"), price=Decimal("39.90"),
			types=self.category, stock_quantity=20, sold=3,
			created_by="merch01", updated_by="merch01",
		)

	def _assert_no_internal_fields(self, payload):
		body = str(payload)
		self.assertNotIn("cost_price", body)
		self.assertNotIn("9.37", body)
		self.assertNotIn("created_by", body)
		self.assertNotIn("merch01", body)

	def test_list_does_not_leak_cost_price(self):
		response = self.client.get("/api/commodity/list/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self._assert_no_internal_fields(response.data)

	def test_detail_does_not_leak_cost_price(self):
		response = self.client.get(f"/api/commodity/detail/{self.product.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self._assert_no_internal_fields(response.data)

	def test_search_does_not_leak_cost_price(self):
		response = self.client.get("/api/commodity/search/", {"query": "牛肉"})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self._assert_no_internal_fields(response.data)
