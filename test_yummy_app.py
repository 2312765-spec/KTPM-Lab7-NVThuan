import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service
# ================================================================
# CAP DO 1: Bo test co ban cho san ( Moi chi dat ~35% Coverage )
# ================================================================
class TestEasyLevel(unittest.TestCase):
	"""Kiem thu chuc nang co ban tinh tien don hang."""

	def setUp(self):
		self.app = YummyApp()

	def test_calculate_total_for_single_item(self):
		cart = {"pho": 2}
		self.assertEqual(self.app.calculate_order_total(cart), 100000)

	def test_calculate_total_for_multiple_items(self):
		cart = {"pho": 1, "bun": 1}
		self.assertEqual(self.app.calculate_order_total(cart), 95000)

	def test_calculate_total_for_empty_cart(self):
		self.assertEqual(self.app.calculate_order_total({}), 0.0)

	def test_calculate_total_with_zero_quantity(self):
		cart = {"pho": 0}
		self.assertEqual(self.app.calculate_order_total(cart), 0.0)
# ================================================================
# CAP DO 2 ( TIET 3) : SINH VIEN TU TAY LAP TRINH TEST CASE DUOI DAY
# ( Sau khi da hoan thanh Ban thiet ke test case viet tay tren giay )
# ================================================================
class TestMediumLevel(unittest.TestCase):
	"""Kiem thu ap dung ma khuyen mai (apply_promo_code)."""

	def test_online_valid_code(self):
		app = YummyApp(network_status="online")
		self.assertAlmostEqual(app.apply_promo_code(100000, "GIAM10"), 90000)

	def test_offline_raises_connection_error(self):
		app = YummyApp(network_status="offline")
		with self.assertRaises(ConnectionError):
			app.apply_promo_code(100000, "GIAM10")

	def test_special_code_on_os15(self):
		app = YummyApp(os_version=15)
		self.assertAlmostEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

	def test_special_code_on_os14_raises_value_error(self):
		app = YummyApp(os_version=14)
		with self.assertRaises(ValueError):
			app.apply_promo_code(100000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
	"""Kiem thu goi y nha hang, dong the (mock) dich vu GPS."""

	def setUp(self):
		self.app = YummyApp()

	@patch('yummy_app.gps_service.get_current_location')
	def test_gps_in_service_area(self, mock_location):
		mock_location.return_value = (10.0, 105.0)
		self.assertEqual(
			self.app.get_nearby_restaurants(),
			["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
		)
		mock_location.assert_called_once()

	@patch('yummy_app.gps_service.get_current_location')
	def test_gps_out_of_service_area(self, mock_location):
		mock_location.return_value = (20.0, 110.0)
		self.assertEqual(self.app.get_nearby_restaurants(), [])

	@patch('yummy_app.gps_service.get_current_location')
	def test_gps_signal_lost(self, mock_location):
		mock_location.side_effect = gps_service.GPSSignalLostError
		self.assertEqual(
			self.app.get_nearby_restaurants(), "Khong the xac dinh vi tri."
		)


if __name__ == "__main__":
	unittest.main()
