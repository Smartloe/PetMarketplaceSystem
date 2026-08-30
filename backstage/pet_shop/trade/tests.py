"""
Trade app tests: cross-user access isolation, and checkout stock/atomicity.
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.test import APITestCase

from commodity.models import CommodityCategories, CommodityInfos
from customer_operation.models import UserAddress, UserComment
from trade.models import OrderGoods, OrderInfos, ShoppingCart


class CrossUserAccessTests(APITestCase):
    """Alice must not be able to read Bob's private records."""

    def setUp(self):
        self.alice = User.objects.create_user("alice", "a@example.com", "pw-alice-123")
        self.bob = User.objects.create_user("bob", "b@example.com", "pw-bob-123")

        self.alice_address = UserAddress.objects.create(
            user=self.alice, province="P", city="C", county="D",
            address="ALICE SECRET ST 1", signer_name="Alice",
            signer_mobile="13900000001",
        )
        self.bob_address = UserAddress.objects.create(
            user=self.bob, province="P", city="C", county="D",
            address="BOB SECRET ST 2", signer_name="Bob",
            signer_mobile="13900000002",
        )

        self.bob_order = OrderInfos.objects.create(
            user=self.bob, order_sn="BOBSECRETORDER01",
            address=self.bob_address,
            total_price=Decimal("999.00"), payable_price=Decimal("999.00"),
            pay_method=1, order_status=1,
            leave_comment="BOB PRIVATE ORDER NOTE",
            created_by="bob",
        )
        ShoppingCart.objects.create(user=self.bob, commodity=None, quantity=3)

    def _as_alice(self):
        self.client.force_authenticate(user=self.alice)

    def _results(self, response):
        """Unwrap paginated or bare list payloads."""
        data = response.data
        return data["results"] if isinstance(data, dict) and "results" in data else data

    def test_alice_cannot_list_bobs_addresses(self):
        self._as_alice()
        response = self.client.get("/api/operation/addresses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = str(self._results(response))
        self.assertNotIn("BOB SECRET ST 2", body)
        self.assertNotIn("13900000002", body)

    def test_alice_cannot_list_bobs_orders(self):
        self._as_alice()
        response = self.client.get("/api/trade/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = str(self._results(response))
        self.assertNotIn("BOBSECRETORDER01", body)
        self.assertNotIn("BOB PRIVATE ORDER NOTE", body)

    def test_alice_cannot_list_bobs_cart(self):
        self._as_alice()
        response = self.client.get("/api/trade/shopping-carts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for row in self._results(response):
            self.assertNotEqual(row.get("user"), self.bob.id)

    def test_alice_cannot_retrieve_bobs_order_detail(self):
        self._as_alice()
        response = self.client.get(f"/api/trade/orders/{self.bob_order.id}/")
        self.assertIn(
            response.status_code,
            (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND),
        )

    def test_alice_cannot_delete_bobs_order(self):
        self._as_alice()
        response = self.client.delete(f"/api/trade/orders/{self.bob_order.id}/")
        self.assertIn(
            response.status_code,
            (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND),
        )
        self.assertTrue(OrderInfos.objects.filter(id=self.bob_order.id).exists())


class CheckoutTests(APITestCase):
    """Checkout must move stock, stay atomic, and not collide on order_sn."""

    def setUp(self):
        self.user = User.objects.create_user("frank", "f@example.com", "pw-frank-123")
        self.client.force_authenticate(user=self.user)

        self.address = UserAddress.objects.create(
            user=self.user, province="P", city="C", county="D",
            address="ST 1", signer_name="Frank", signer_mobile="13900000003",
        )
        self.category = CommodityCategories.objects.create(title="猫粮")
        self.product = CommodityInfos.objects.create(
            sku_title="测试猫粮", main_image="product_photos/x.png",
            detail_images="product_photos_details/x.png",
            cost_price=Decimal("10.00"), price=Decimal("25.00"),
            types=self.category, stock_quantity=10, sold=0,
        )

    def _cart(self, quantity):
        return ShoppingCart.objects.create(
            user=self.user, commodity=self.product, quantity=quantity
        )

    def _checkout(self, cart_ids, **extra):
        body = {"cart_ids": cart_ids, "address_id": self.address.id, "pay_method": 1}
        body.update(extra)
        return self.client.post("/api/trade/checkout/", body, format="json")

    def test_successful_checkout_decrements_stock_and_increments_sold(self):
        cart = self._cart(3)
        response = self._checkout([cart.id])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 7)
        self.assertEqual(self.product.sold, 3)

    def test_checkout_clears_the_processed_cart_rows(self):
        cart = self._cart(2)
        self._checkout([cart.id])
        self.assertFalse(ShoppingCart.objects.filter(id=cart.id).exists())

    def test_checkout_beyond_stock_is_refused(self):
        cart = self._cart(11)  # only 10 in stock
        response = self._checkout([cart.id])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("库存不足", str(response.data))

    def test_refused_checkout_leaves_no_partial_state(self):
        """The whole thing rolls back: no order, no stock change, cart intact."""
        cart = self._cart(11)
        orders_before = OrderInfos.objects.count()

        self._checkout([cart.id])

        self.assertEqual(OrderInfos.objects.count(), orders_before)
        self.assertEqual(OrderGoods.objects.count(), 0)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 10)
        self.assertEqual(self.product.sold, 0)
        self.assertTrue(ShoppingCart.objects.filter(id=cart.id).exists())

    def test_two_checkouts_in_the_same_second_get_distinct_order_sns(self):
        """
        order_sn used to be timestamp+user_id at second granularity, so a
        second order within the same second violated the unique constraint.
        """
        first = self._checkout([self._cart(1).id])
        second = self._checkout([self._cart(1).id])

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(first.data["order_sn"], second.data["order_sn"])

    def test_repeated_product_across_cart_rows_is_summed_against_stock(self):
        """Two cart rows for the same product must not each get full stock."""
        a, b = self._cart(6), self._cart(6)  # 12 total, only 10 in stock
        response = self._checkout([a.id, b.id])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 10)

    def test_invalid_pay_method_is_a_400_not_a_500(self):
        cart = self._cart(1)
        for bad in ("abc", 99, None):
            with self.subTest(pay_method=bad):
                response = self._checkout([cart.id], pay_method=bad)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_address_belonging_to_another_user_is_refused(self):
        other = User.objects.create_user("grace", "g@example.com", "pw-grace-123")
        foreign = UserAddress.objects.create(
            user=other, province="P", city="C", county="D",
            address="OTHER ST", signer_name="Grace", signer_mobile="13900000004",
        )
        cart = self._cart(1)
        response = self.client.post("/api/trade/checkout/", {
            "cart_ids": [cart.id], "address_id": foreign.id, "pay_method": 1,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderCommentRatingTests(APITestCase):
    """Rating must be constrained to 1-5 so it can't poison the dashboard."""

    def setUp(self):
        self.user = User.objects.create_user("henry", "h@example.com", "pw-henry-123")
        self.client.force_authenticate(user=self.user)

        address = UserAddress.objects.create(
            user=self.user, province="P", city="C", county="D",
            address="ST", signer_name="Henry", signer_mobile="13900000005",
        )
        category = CommodityCategories.objects.create(title="玩具")
        product = CommodityInfos.objects.create(
            sku_title="逗猫棒", main_image="product_photos/y.png",
            detail_images="product_photos_details/y.png",
            cost_price=Decimal("5.00"), price=Decimal("15.00"),
            types=category, stock_quantity=5, sold=0,
        )
        # order_status=3 (已签收) is the precondition for commenting
        self.order = OrderInfos.objects.create(
            user=self.user, order_sn="ORDERFORCOMMENT1", address=address,
            total_price=Decimal("15.00"), payable_price=Decimal("15.00"),
            pay_method=1, order_status=3, created_by="henry",
        )
        self.order_goods = OrderGoods.objects.create(
            order=self.order, goods=product, goods_num=1
        )

    def _comment(self, rating):
        return self.client.post(
            f"/api/trade/orders/{self.order.id}/goods/{self.order_goods.id}/comment/",
            {"content": "还不错", "rating": rating},
            format="json",
        )

    def test_out_of_range_rating_is_refused(self):
        for bad in (0, 6, 999, -5):
            with self.subTest(rating=bad):
                response = self._comment(bad)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserComment.objects.count(), 0)

    def test_non_numeric_rating_is_a_400_not_a_500(self):
        response = self._comment("five")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_rating_is_accepted(self):
        response = self._comment(4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserComment.objects.get().rating, 4)


class OrderStateTransitionSecurityTests(APITestCase):
    """
    订单金额与状态只能走专用端点流转。此前通用 PUT /trade/orders/
    全字段可写，客户端可以篡改应付金额、伪造“已签收/已退货”。
    """

    def setUp(self):
        self.user = User.objects.create_user("ivy", "i@example.com", "pw-ivy-12345")
        self.client.force_authenticate(user=self.user)

        self.address = UserAddress.objects.create(
            user=self.user, province="P", city="C", county="D",
            address="ST", signer_name="Ivy", signer_mobile="13900000006",
        )
        self.category = CommodityCategories.objects.create(title="零食")
        self.product = CommodityInfos.objects.create(
            sku_title="冻干", main_image="product_photos/z.png",
            detail_images="product_photos_details/z.png",
            cost_price=Decimal("8.00"), price=Decimal("30.00"),
            types=self.category, stock_quantity=10, sold=0,
        )

    def _order(self, order_status, refund_status=0):
        return OrderInfos.objects.create(
            user=self.user, order_sn=f"IVYORDER{order_status}{refund_status}0001",
            address=self.address,
            total_price=Decimal("30.00"), payable_price=Decimal("30.00"),
            pay_method=1, order_status=order_status, refund_status=refund_status,
            created_by="ivy",
        )

    def test_order_amount_and_status_cannot_be_patched(self):
        order = self._order(0)
        response = self.client.patch(
            f"/api/trade/orders/{order.id}/",
            {"total_price": "0.01", "payable_price": "0.01", "order_status": 5},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        order.refresh_from_db()
        self.assertEqual(order.total_price, Decimal("30.00"))
        self.assertEqual(order.order_status, 0)

    def test_order_goods_cannot_be_created_directly(self):
        order = self._order(2)
        response = self.client.post(
            "/api/trade/order-goods/",
            {"order": order.id, "goods": self.product.id, "goods_num": 99},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(OrderGoods.objects.count(), 0)

    def test_only_unpaid_orders_can_be_cancelled(self):
        unpaid = self._order(0)
        paid = self._order(1)

        paid_delete = self.client.delete(f"/api/trade/orders/{paid.id}/")
        self.assertEqual(paid_delete.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(OrderInfos.objects.filter(id=paid.id).exists())

        unpaid_delete = self.client.delete(f"/api/trade/orders/{unpaid.id}/")
        self.assertEqual(unpaid_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderInfos.objects.filter(id=unpaid.id).exists())

    def test_pay_endpoint_moves_unpaid_order_to_paid(self):
        order = self._order(0)
        response = self.client.post(
            f"/api/trade/orders/{order.id}/pay/", {"pay_method": 2}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.order_status, 1)
        self.assertEqual(order.pay_method, 2)

    def test_pay_endpoint_rejects_non_pending_orders(self):
        order = self._order(2)  # 发货中，不是待支付
        response = self.client.post(
            f"/api/trade/orders/{order.id}/pay/", {"pay_method": 2}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()
        self.assertEqual(order.order_status, 2)

    def test_pay_endpoint_rejects_bad_pay_methods(self):
        order = self._order(0)
        for bad in ("abc", 99):
            with self.subTest(pay_method=bad):
                response = self.client.post(
                    f"/api/trade/orders/{order.id}/pay/", {"pay_method": bad}, format="json"
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()
        self.assertEqual(order.order_status, 0)

    def test_pending_refund_can_be_cancelled_back_to_shipping(self):
        order = self._order(2, refund_status=1)
        response = self.client.post(f"/api/trade/orders/{order.id}/refund/cancel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.refund_status, 0)
        self.assertEqual(order.order_status, 2)

    def test_cancel_refund_requires_pending_review(self):
        order = self._order(2)  # refund_status 默认 0，没有待审核申请
        response = self.client.post(f"/api/trade/orders/{order.id}/refund/cancel/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        order.refresh_from_db()
        self.assertEqual(order.refund_status, 0)
        self.assertEqual(order.order_status, 2)


class ShoppingCartQuantityValidationTests(APITestCase):
    """购物车数量必须是正整数，非数字不能变成 500。"""

    def setUp(self):
        self.user = User.objects.create_user("mary", "m@example.com", "pw-mary-12345")
        self.client.force_authenticate(user=self.user)
        self.category = CommodityCategories.objects.create(title="玩具")
        self.product = CommodityInfos.objects.create(
            sku_title="猫爬架", main_image="product_photos/w.png",
            detail_images="product_photos_details/w.png",
            cost_price=Decimal("40.00"), price=Decimal("88.00"),
            types=self.category, stock_quantity=10,
        )

    def test_non_numeric_quantity_is_a_400_not_a_500(self):
        response = self.client.post(
            "/api/trade/shopping-carts/",
            {"commodity": self.product.id, "quantity": "abc"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShoppingCart.objects.count(), 0)

    def test_zero_and_negative_quantity_are_refused(self):
        for bad in (0, -3):
            with self.subTest(quantity=bad):
                response = self.client.post(
                    "/api/trade/shopping-carts/",
                    {"commodity": self.product.id, "quantity": bad}, format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShoppingCart.objects.count(), 0)


class CartCommodityIntegrityTests(APITestCase):
    """购物车行只能指向真实存在的商品（FK 约束已恢复）。"""

    def setUp(self):
        self.user = User.objects.create_user("nina", "n@example.com", "pw-nina-12345")
        self.client.force_authenticate(user=self.user)

    def test_nonexistent_commodity_is_refused(self):
        response = self.client.post(
            "/api/trade/shopping-carts/",
            {"commodity": 999999, "quantity": 1}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShoppingCart.objects.count(), 0)


class OrderGoodsProtectTests(APITestCase):
    """有订单明细引用的商品不允许被删除，历史订单必须保真。"""

    def setUp(self):
        self.user = User.objects.create_user("oscar", "o@example.com", "pw-oscar-1234")
        self.address = UserAddress.objects.create(
            user=self.user, province="P", city="C", county="D",
            address="ST", signer_name="Oscar", signer_mobile="13900000007",
        )
        self.category = CommodityCategories.objects.create(title="保健")
        self.product = CommodityInfos.objects.create(
            sku_title="鱼油", main_image="product_photos/f.png",
            detail_images="product_photos_details/f.png",
            cost_price=Decimal("12.00"), price=Decimal("36.00"),
            types=self.category, stock_quantity=8,
        )
        order = OrderInfos.objects.create(
            user=self.user, order_sn="OSCARORDER00000001", address=self.address,
            total_price=Decimal("36.00"), payable_price=Decimal("36.00"),
            pay_method=1, order_status=3, created_by="oscar",
        )
        OrderGoods.objects.create(order=order, goods=self.product, goods_num=1)

    def test_commodity_with_order_lines_cannot_be_deleted(self):
        with self.assertRaises(ProtectedError):
            self.product.delete()
        self.assertTrue(CommodityInfos.objects.filter(id=self.product.id).exists())
