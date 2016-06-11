import unittest
import main

class Test(unittest.TestCase):
    def setUp(self):
        pass
    def _testGenerateTCSV(self):
        main.lBlinks = [
            {'duration': 266.666667, 'start': 2400.0,  'end': 2666.666667},#l1
            {'duration': 133.333333, 'start': 2733.33, 'end': 2866.666667},#l2
            {'duration': 133.333333, 'start': 3000.0,  'end': 3133.333333},#l3
            {'duration': 133.333333, 'start': 6333.33, 'end': 6466.666667},#l4
            {'duration': 200.0,      'start': 9900.0,  'end': 10100.0}#l5
        ]
        main.rBlinks = [
            {'duration': 300.0,      'start': 2266.67, 'end': 2566.666667}, #r1
            {'duration': 66.666667,  'start': 2633.33, 'end': 2700.0},#r2
            {'duration': 366.666667, 'start': 2766.67, 'end': 3133.333333},#r3
            {'duration': 133.333333, 'start': 6333.33, 'end': 6466.666667},#r4
            {'duration': 66.666667,  'start': 9966.67, 'end': 10033.333333}#r5
        ]

        tsdict, tsl = main.generateTCSV()
        self.assertEquals(17, len(tsl))
        self.assertEquals((2266.67, {'rbs': 1}), tsl[0])#r1
        self.assertEquals((2400.0, {'lbs': 1}), tsl[1])#l1
        self.assertEquals((2566.666667, {'rbe': 1}), tsl[2])#r1e
        self.assertEquals((2633.33, {'rbs': 1}), tsl[3])#r2
        self.assertEquals((2666.666667, {'lbe': 1}), tsl[4])#l1e
        self.assertEquals((2700.0, {'rbe': 1}), tsl[5])#r2e
        self.assertEquals((2733.33, {'lbs': 1}), tsl[6])#l2
        self.assertEquals((2766.67, {'rbs': 1}), tsl[7])#r3
        self.assertEquals((2866.666667, {'lbe': 1}), tsl[8])#l2e
        self.assertEquals((3000.0, {'lbs': 1}), tsl[9])#l3
        self.assertEquals((3133.333333, {'rbe': 1, 'lbe': 1}), tsl[10])#l3e r3e
        self.assertEquals((6333.33, {'rbs': 1, 'lbs' : 1}), tsl[11])#l4 r4
        self.assertEquals((6466.666667, {'rbe': 1, 'lbe': 1}), tsl[12])#l4e r4e
        self.assertEquals((9900.0, {'lbs': 1}), tsl[13])#l5
        self.assertEquals((9966.67, {'rbs': 1}), tsl[14])#r5
        self.assertEquals((10033.333333, {'rbe': 1}), tsl[15])#r5e
        self.assertEquals((10100.0, {'lbe': 1}), tsl[16])#l5e
    def testProcessLogLine(self):
        main.lBlinks = []
        main.rBlinks = []
        main.tCors   = []
        r = main.processLogLine("debug_blinks_d4: adding_lBlinkChunks fs 169 fe 173 start 5666.67 end 5800.000000 duration 133.333333")

    def testParseAnnot1(self):
        tmpContent = ""
        tmpContent += "#eye-blink annotation file version 1.1\n"
        tmpContent += "#author:  fogelton\n"
        tmpContent += "#glasses: NO\n"
        tmpContent += "#challenging: NO\n"
        tmpContent += "#message start\n"
        tmpContent += "\n"
        tmpContent += "\n"
        tmpContent += "#message end\n"
        tmpContent += "#start\n"
        tmpContent += "0:-1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "1:-1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "2:-1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "3:1:X:X:X:X:X:251:221:247:290:297:288:348:282:409:270:459:267\n"
        tmpContent += "4:1:X:C:X:C:X:251:221:247:290:297:288:348:282:409:270:459:267\n"
        tmpContent += "5:1:X:X:X:X:X:251:221:247:290:297:288:348:282:409:270:459:267\n"
        tmpContent += "6:-1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "7:2:X:X:X:X:X:251:221:247:290:297:288:348:282:409:270:459:267\n"
        tmpContent += "8:2:X:C:X:C:X:251:221:247:290:297:288:348:282:409:270:459:267\n"
        tmpContent += "9:2:X:X:X:X:X:251:221:247:290:297:288:348:282:409:270:459:267\n"
        tmpContent += "10:-1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += ""
        tmpContent += "#end"
        file("/tmp/.testParseAnnot", "wb").write(tmpContent)
        f = file("/tmp/.testParseAnnot", "rb")

        fndict = {}
        for i in xrange(100):
            fndict[i] = {}

        main.parseAnnotations(f, fndict)

        self.assertEquals({'anots': 0.999}, fndict[3])
        self.assertEquals({'anote': 0.999}, fndict[5])
        self.assertEquals({'anots': 0.999}, fndict[7])
        self.assertEquals({'anote': 0.999}, fndict[9])

    def testParseAnnot2(self):
        tmpContent = ""
        tmpContent += "#start\n"
        tmpContent += "0:-1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "1:1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "2:-1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "#end"
        file("/tmp/.testParseAnnot", "wb").write(tmpContent)
        f = file("/tmp/.testParseAnnot", "rb")

        fndict = {}
        for i in xrange(100):
            fndict[i] = {}

        main.parseAnnotations(f, fndict)

        self.assertEquals({'anots': 0.999, 'anote': 0.999}, fndict[1])

    def testParseAnnot3(self):
        tmpContent = ""
        tmpContent += "#start\n"
        tmpContent += "0:1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "#end"
        file("/tmp/.testParseAnnot", "wb").write(tmpContent)
        f = file("/tmp/.testParseAnnot", "rb")

        fndict = {}
        for i in xrange(100):
            fndict[i] = {}

        main.parseAnnotations(f, fndict)

        self.assertEquals({'anots': 0.999, 'anote': 0.999}, fndict[0])

    def testParseAnnot4(self):
        tmpContent = ""
        tmpContent += "#start\n"
        tmpContent += "0:1:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "1:2:X:X:X:X:X:260:194:251:290:299:270:351:259:416:246:466:243\n"
        tmpContent += "#end"
        file("/tmp/.testParseAnnot", "wb").write(tmpContent)
        f = file("/tmp/.testParseAnnot", "rb")

        fndict = {}
        for i in xrange(100):
            fndict[i] = {}

        main.parseAnnotations(f, fndict)

        self.assertEquals({'anots': 0.999, 'anote': 0.999}, fndict[0])
        self.assertEquals({'anots': 0.999, 'anote': 0.999}, fndict[1])



if __name__ =="__main__":
    unittest.main()