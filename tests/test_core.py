import unittest,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
class Core(unittest.TestCase):
 def test_unratified(self):
  r=pathlib.Path(__file__).resolve().parents[1]
  m=json.loads((r/"manifest.json").read_text())
  self.assertEqual(m["corporate_domicile"],"UNDECIDED")
  self.assertFalse(m["is_issued_token"])
 def test_release_block(self):
  r=pathlib.Path(__file__).resolve().parents[1]
  g=json.loads((r/"70_DELIVERY/release-gates.json").read_text())
  self.assertTrue(all(x["status"]!="pass" for x in g["gates"]))
if __name__=="__main__":unittest.main()
