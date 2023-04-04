import unittest
import pandas as pd
from main import siphon


class SiphonTests(unittest.TestCase):

    def setUp(self):
        # Create a small test DataFrame
        self.test_data = pd.DataFrame({
            'Server': ['IslandView1', 'IslandView2', 'IslandView3'],
            'Serial Number': ['123456', '789012', '345678'],
            'Model Number': ['2.0C-H4A-D1-B', 'ENC-4P-H264', '2.0C-H4A-D1-B'],
            'IP Address': ['192.168.1.1', '10.0.0.1', '172.16.0.1'],
            'Logical ID': ['Logical ID:1', 'Logical ID:2', 'Logical ID:3']
        })

    def test_siphon(self):
        # Test that siphon() correctly filters the DataFrame for a given model number
        result = siphon('2.0C-H4A-D1-B')
        expected = {
            'ids': [1, 3],
            'ips': ['192.168.1.1', '172.16.0.1']
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
