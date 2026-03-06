"""
Red WiFi Test Suite
Import verification and basic functionality tests.
"""

import sys
import unittest


class TestImports(unittest.TestCase):
    """Test that all modules import successfully."""
    
    def test_import_branding(self):
        """Test branding module import."""
        from red_wifi import branding
        self.assertTrue(hasattr(branding, 'print_banner'))
        self.assertTrue(hasattr(branding, 'print_logo_large'))
    
    def test_import_wifi_pentest(self):
        """Test wifi_pentest module import."""
        from red_wifi import WiFiPentestFramework, Logger, Colors, WiFiNetwork
        self.assertIsNotNone(WiFiPentestFramework)
        self.assertIsNotNone(Logger)
        self.assertIsNotNone(Colors)
        self.assertIsNotNone(WiFiNetwork)
    
    def test_import_wifite_integration(self):
        """Test wifite_integration module import."""
        from red_wifi import (
            AutomatedAttacker,
            AttackMode,
            AttackStrategy,
            WPAAttacks,
            WPSAttacks
        )
        self.assertIsNotNone(AutomatedAttacker)
        self.assertIsNotNone(AttackMode)
        self.assertIsNotNone(AttackStrategy)
        self.assertIsNotNone(WPAAttacks)
        self.assertIsNotNone(WPSAttacks)
    
    def test_import_advanced_attacks(self):
        """Test advanced_attacks module import."""
        from red_wifi import (
            EncryptionAnalyzer,
            EncryptionType,
            AdvancedWPAAttacks,
            AdvancedWPSAttacks
        )
        self.assertIsNotNone(EncryptionAnalyzer)
        self.assertIsNotNone(EncryptionType)
        self.assertIsNotNone(AdvancedWPAAttacks)
        self.assertIsNotNone(AdvancedWPSAttacks)
    
    def test_version_info(self):
        """Test version information."""
        import red_wifi
        self.assertEqual(red_wifi.__version__, "2.0.0")
        self.assertIsNotNone(red_wifi.__author__)
        self.assertEqual(red_wifi.__license__, "MIT")
    
    def test_package_all(self):
        """Test __all__ exports."""
        import red_wifi
        all_exports = red_wifi.__all__
        self.assertIn('WiFiPentestFramework', all_exports)
        self.assertIn('AutomatedAttacker', all_exports)
        self.assertIn('AttackMode', all_exports)
        self.assertIn('EncryptionAnalyzer', all_exports)
        self.assertIn('main', all_exports)


class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality of core classes."""
    
    def test_logger_creation(self):
        """Test Logger instantiation."""
        from red_wifi import Logger
        logger = Logger("TestLogger")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "TestLogger")
    
    def test_colors_class(self):
        """Test Colors class."""
        from red_wifi import Colors
        colors = Colors()
        self.assertIsNotNone(colors.RED)
        self.assertIsNotNone(colors.GREEN)
        self.assertIsNotNone(colors.YELLOW)
        self.assertIsNotNone(colors.RESET)
    
    def test_wifi_network_creation(self):
        """Test WiFiNetwork dataclass."""
        from red_wifi import WiFiNetwork
        network = WiFiNetwork(
            bssid="00:11:22:33:44:55",
            ssid="TestNetwork",
            channel=6,
            rssi=-50,
            encryption="WPA2",
            band="2.4GHz"
        )
        self.assertEqual(network.ssid, "TestNetwork")
        self.assertEqual(network.bssid, "00:11:22:33:44:55")
        self.assertEqual(network.channel, 6)
        self.assertEqual(network.encryption, "WPA2")
    
    def test_encryption_analyzer(self):
        """Test EncryptionAnalyzer."""
        from red_wifi import EncryptionAnalyzer, Logger, EncryptionType
        logger = Logger("TestAnalyzer")
        analyzer = EncryptionAnalyzer(logger)
        
        # Test classification
        self.assertEqual(
            analyzer.classify_encryption("WPA2"),
            EncryptionType.WPA2
        )
        self.assertEqual(
            analyzer.classify_encryption("WPA3"),
            EncryptionType.WPA3
        )
        self.assertEqual(
            analyzer.classify_encryption("Open"),
            EncryptionType.OPEN
        )


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestImports))
    suite.addTests(loader.loadTestsFromTestCase(TestBasicFunctionality))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
