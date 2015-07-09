import dvrhelper
import unittest

class TestDVRHelperMethods(unittest.TestCase):
  def test_DVRFile_init(self):
    examples = {
      # format of result:
      # [x.path["filename"], x.path["ext"], x.show_name["raw"], x.season["num"]["int"], x.season["num"]["disp"], x.episode["num"]["int"], x.episode["num"]["disp"]
      "12.Monkeys.S01E04.HDTV.x264-KILLERS.mp4":
        ["12.Monkeys.S01E04.HDTV.x264-KILLERS.mp4", ".mp4", "12.Monkeys.", 1, "01", 4, "04"],
      "/volume2/Downloads/Archer.2009.S05E07.HDTV.x264-2HD.mp4":
        ["Archer.2009.S05E07.HDTV.x264-2HD.mp4", ".mp4", "Archer.2009.", 5, "05", 7, "07"],
      "/volume1/Dropbox/Media/DVR/Bobs.Burgers.S04E20.PROPER.HDTV.x264-W4F.mp4":
        ["Bobs.Burgers.S04E20.PROPER.HDTV.x264-W4F.mp4", ".mp4", "Bobs.Burgers.", 4, "04", 20, "20"],
      "../Community.S06E04.Queer.Studies.and.Advanced.Waxing.REPACK.WebRip.x264-FiHTV.mp4":
        ["Community.S06E04.Queer.Studies.and.Advanced.Waxing.REPACK.WebRip.x264-FiHTV.mp4", ".mp4", "Community.", 6, "06", 4, "04"],
      "Scratch/DVR/Doctor_Who_2005.8x10.In_The_Forest_Of_The_Night.HDTV_x264-FoV.mp4":
        ["Doctor_Who_2005.8x10.In_The_Forest_Of_The_Night.HDTV_x264-FoV.mp4", ".mp4", "Doctor_Who_2005.", 8, "08", 10, "10"],
      "House.of.Cards.2013.S02E01.WEBRip.HDTV.x264-2HD.mp4":
        ["House.of.Cards.2013.S02E01.WEBRip.HDTV.x264-2HD.mp4", ".mp4", "House.of.Cards.2013.", 2, "02", 1, "01"],
      "Once.Upon.a.Time.S04E15.HDTV.x264-LOL.mp4":
        ["Once.Upon.a.Time.S04E15.HDTV.x264-LOL.mp4", ".mp4", "Once.Upon.a.Time.", 4, "04", 15, "15"],
      "The.Flash.2014.S01E23.HDTV.x264-LOL.mp4":
        ["The.Flash.2014.S01E23.HDTV.x264-LOL.mp4", ".mp4", "The.Flash.2014.", 1, "01", 23, "23"],
    }
    for (input_path, output_object_vars) in examples.items():
      test_file = dvrhelper.DVRFile(input_path)

      self.assertEqual(test_file.path["filename"]       , output_object_vars[0])
      self.assertEqual(test_file.path["ext"]            , output_object_vars[1])
      self.assertEqual(test_file.show_name["raw"]       , output_object_vars[2])
      self.assertEqual(test_file.season["num"]["int"]   , output_object_vars[3])
      self.assertEqual(test_file.season["num"]["disp"]  , output_object_vars[4])
      self.assertEqual(test_file.episode["num"]["int"]  , output_object_vars[5])
      self.assertEqual(test_file.episode["num"]["disp"] , output_object_vars[6])

if __name__ == '__main__':
  unittest.main()