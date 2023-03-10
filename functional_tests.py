import unittest
from selenium import webdriver


class HomePageTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        # Edith hears about a cool to-do list site. She visits it
        self.browser.get('http://localhost:8000')

        # She sees the title and the header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do', header.text)


if __name__ == '__main__':
    unittest.main()



