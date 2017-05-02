"""png_image_test.py"""

import unittest
import sys
import os
sys.path.insert(0,
  os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.path.join('..', '..', '..')
  )
)

import fpdf
import test
from test.utilities import relative_path_to, \
                           set_doc_date_0, \
                           calculate_hash_of_file

from PIL import Image
import io

not_supported = [
  "e59ec0cfb8ab64558099543dc19f8378.png",  # Interlacing not supported:
  "6c853ed9dacd5716bc54eb59cec30889.png",  # 16-bit depth not supported:
  "ac6343a98f8edabfcc6e536dd75aacb0.png",  # Interlacing not supported:
  "93e6127b9c4e7a99459c558b81d31bc5.png",  # Interlacing not supported:
  "18f9baf3834980f4b80a3e82ad45be48.png",  # Interlacing not supported:
  "51a4d21670dc8dfa8ffc9e54afd62f5f.png",  # Interlacing not supported:
]
images_in_memory = {}
images = [relative_path_to(f) for f
          in os.listdir(relative_path_to('.'))
          if f.endswith(".png")
            and os.path.basename(f) not in not_supported]

# Load images before entering test
for image in images:
  images_in_memory[image] = Image.open(image)

class InsertPNGSuiteMemory(unittest.TestCase):
  def test_insert_png_memory(self):
    pdf = fpdf.FPDF(unit = 'pt')
    pdf.compress = False

    images = [relative_path_to(f) for f
              in os.listdir(relative_path_to('.'))
              if f.endswith(".png")]

    for image in images:
      pdf.add_page()
      # i = Image.open(image)
      i = images_in_memory.get(image, None)
      if i is None: continue
      # print image#, i.size

      temp_i_storage = io.BytesIO()
      i.save(temp_i_storage, format = 'png')
      pdf.image('arbitrary_name_of_' + image, x = 0, y = 0,
                w = i.size[0], h = i.size[1],
                type = '', link = None, file = temp_i_storage)

    set_doc_date_0(pdf)
    outfile = relative_path_to('insert_images_png_test_memory.pdf')
    pdf.output(outfile, 'F')
    # print(calculate_hash_of_file(outfile))

    test_hash = calculate_hash_of_file(outfile)
    self.assertEqual(test_hash, "652c74f2fa6b12f0c80eebd75b2a2b18")  # skip
    # self.assertEqual(test_hash, "5d11f7a3235d154c3a7001d3b8551d6e")
    os.unlink(outfile)
 
class InsertPNGSuiteFiles(unittest.TestCase):
  def test_insert_png_files(self):
    pdf = fpdf.FPDF(unit = 'pt')
    pdf.compress = False

    images = [relative_path_to(f) for f
              in os.listdir(relative_path_to('.'))
              if f.endswith(".png")]

    not_supported = [
      "e59ec0cfb8ab64558099543dc19f8378.png",  # Interlacing not supported:
      "6c853ed9dacd5716bc54eb59cec30889.png",  # 16-bit depth not supported:
      "ac6343a98f8edabfcc6e536dd75aacb0.png",  # Interlacing not supported:
      "93e6127b9c4e7a99459c558b81d31bc5.png",  # Interlacing not supported:
      "18f9baf3834980f4b80a3e82ad45be48.png",  # Interlacing not supported:
      "51a4d21670dc8dfa8ffc9e54afd62f5f.png",  # Interlacing not supported:
    ]

    for image in images:
      if os.path.basename(image) in not_supported:
        self.assertRaises(Exception, pdf.image, x = 0, y = 0, w = 0, h = 0,
                          type = '', link = None)
      else:
        pdf.add_page()
        pdf.image(image, x = 0, y = 0, w = 0, h = 0,
                  type = '', link = None)

    set_doc_date_0(pdf)
    outfile = relative_path_to('insert_images_png_test_files.pdf')
    pdf.output(outfile, 'F')
    # print(calculate_hash_of_file(outfile))

    test_hash = calculate_hash_of_file(outfile)
    self.assertEqual(test_hash, "4f65582566414202a12ed86134de10a7")
    os.unlink(outfile)

if __name__ == '__main__':
  # http://stackoverflow.com/questions/9502516/how-to-know-time-spent-on-each-
  # test-when-using-unittest
  import time
  @classmethod
  def setUpClass(cls):
      cls.start_ = time.time()

  @classmethod
  def tearDownClass(cls):
      t = time.time()
      print("\n%s.%s: %.3f" % (cls.__module__, cls.__name__, t - cls.start_))

  unittest.TestCase.setUpClass = setUpClass
  unittest.TestCase.tearDownClass = tearDownClass

  unittest.main()

## Code used to create test: Test created in place
