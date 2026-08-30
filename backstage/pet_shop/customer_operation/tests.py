"""
customer_operation API 回归：评论可见性与留言回复字段不可伪造。
"""
from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from commodity.models import CommodityCategories, CommodityInfos
from .models import UserComment, UserLeavingMessage


class CommentVisibilityTests(APITestCase):
	"""评论创建只随确认收货评价端点发生；未审核评论不对外。"""

	def setUp(self):
		self.user = User.objects.create_user("kate", "k@example.com", "pw-kate-1234")
		self.category = CommodityCategories.objects.create(title="用品")
		self.product = CommodityInfos.objects.create(
			sku_title="猫砂盆", main_image="product_photos/c.png",
			detail_images="product_photos_details/c.png",
			cost_price=Decimal("15.00"), price=Decimal("45.00"),
			types=self.category, stock_quantity=5,
		)
		self.visible = UserComment.objects.create(
			user=self.user, commodity=self.product, content="很好用", rating=5, is_show=True,
		)
		self.hidden = UserComment.objects.create(
			user=self.user, commodity=self.product, content="待审核", rating=2, is_show=False,
		)

	def test_comment_creation_through_generic_api_is_refused(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.post(
			"/api/operation/usercomments/",
			{"commodity": self.product.id, "content": "绕过购买校验", "rating": 5},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
		self.assertEqual(UserComment.objects.count(), 2)

	def test_hidden_comments_are_not_listed_for_anonymous(self):
		response = self.client.get("/api/operation/usercomments/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		ids = [row["id"] for row in response.data["results"]]
		self.assertIn(self.visible.id, ids)
		self.assertNotIn(self.hidden.id, ids)

	def test_staff_can_see_hidden_comments(self):
		staff = User.objects.create_user(
			"boss", "b@example.com", "pw-boss-1234", is_staff=True,
		)
		self.client.force_authenticate(user=staff)
		response = self.client.get("/api/operation/usercomments/")
		ids = [row["id"] for row in response.data["results"]]
		self.assertIn(self.hidden.id, ids)


class MessageReplySpoofingTests(APITestCase):
	"""留言的客服回复字段不允许客户端自带。"""

	def setUp(self):
		self.user = User.objects.create_user("liam", "l@example.com", "pw-liam-1234")
		self.client.force_authenticate(user=self.user)

	def test_client_cannot_forge_the_support_reply(self):
		response = self.client.post(
			"/api/operation/messages/",
			{
				"message_type": 1, "subject": "咨询", "message": "何时发货？",
				"is_replied": True, "reply_content": "已为您优先发货（伪造）",
			},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		message = UserLeavingMessage.objects.get()
		self.assertFalse(message.is_replied)
		self.assertFalse(message.reply_content)
