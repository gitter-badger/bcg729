
env = Environment(platform="win32", tools=["mingw"])

env.Append(CFLAGS="-Iinclude")

# Static Library
libbcg729_sources = ["src/adaptativeCodebookSearch.c", "src/codebooks.c", "src/computeAdaptativeCodebookGain.c", "src/computeLP.c", "src/computeWeightedSpeech.c", "src/decodeAdaptativeCodeVector.c",
                     "src/decodeFixedCodeVector.c", "src/decodeGains.c", "src/decodeLSP.c", "src/decoder.c", "src/encoder.c", "src/findOpenLoopPitchDelay.c", "src/fixedCodebookSearch.c",
                     "src/gainQuantization.c", "src/interpolateqLSP.c", "src/LP2LSPConversion.c", "src/LPSynthesisFilter.c", "src/LSPQuantization.c", "src/postFilter.c", "src/postProcessing.c",
                     "src/preProcessing.c", "src/qLSP2LP.c", "src/utils.c"]
libbcg729 = env.StaticLibrary(source=libbcg729_sources, target="bcg729")

# Tests suite
testUtils = env.Object(source="test/src/testUtils.c")

adaptativeCodebookSearchTest = env.Program(source=["test/src/adaptativeCodebookSearchTest.c",testUtils], LIBS=[libbcg729])
computeAdaptativeCodebookGainTest = env.Program(source=["test/src/computeAdaptativeCodebookGainTest.c",testUtils], LIBS=[libbcg729])
computeLPTest = env.Program(source=["test/src/computeLPTest.c",testUtils], LIBS=[libbcg729])
computeWeightedSpeechTest = env.Program(source=["test/src/computeWeightedSpeechTest.c",testUtils], LIBS=[libbcg729])
decodeAdaptativeCodeVectorTest = env.Program(source=["test/src/decodeAdaptativeCodeVectorTest.c",testUtils], LIBS=[libbcg729])
decodeFixedCodeVectorTest = env.Program(source=["test/src/decodeFixedCodeVectorTest.c",testUtils], LIBS=[libbcg729])
decodeGainsTest = env.Program(source=["test/src/decodeGainsTest.c",testUtils], LIBS=[libbcg729])
decodeLSPTest = env.Program(source=["test/src/decodeLSPTest.c",testUtils], LIBS=[libbcg729])
decoderMultiChannelTest = env.Program(source=["test/src/decoderMultiChannelTest.c",testUtils], LIBS=[libbcg729])
decoderTest = env.Program(source=["test/src/decoderTest.c",testUtils], LIBS=[libbcg729])
encoderMultiChannelTest = env.Program(source=["test/src/encoderMultiChannelTest.c",testUtils], LIBS=[libbcg729])
encoderTest = env.Program(source=["test/src/encoderTest.c",testUtils], LIBS=[libbcg729])
findOpenLoopPitchDelayTest = env.Program(source=["test/src/findOpenLoopPitchDelayTest.c",testUtils], LIBS=[libbcg729])
fixedCodebookSearchTest = env.Program(source=["test/src/fixedCodebookSearchTest.c",testUtils], LIBS=[libbcg729])
g729FixedPointMathTest = env.Program(source=["test/src/g729FixedPointMathTest.c",testUtils], LIBS=[libbcg729])
gainQuantizationTest = env.Program(source=["test/src/gainQuantizationTest.c",testUtils], LIBS=[libbcg729])
interpolateqLSPAndConvert2LPTest = env.Program(source=["test/src/interpolateqLSPAndConvert2LPTest.c",testUtils], LIBS=[libbcg729])
LP2LSPConversionTest = env.Program(source=["test/src/LP2LSPConversionTest.c",testUtils], LIBS=[libbcg729])
LPSynthesisFilterTest = env.Program(source=["test/src/LPSynthesisFilterTest.c",testUtils], LIBS=[libbcg729])
LSPQuantizationTest = env.Program(source=["test/src/LSPQuantizationTest.c",testUtils], LIBS=[libbcg729])
postFilterTest = env.Program(source=["test/src/postFilterTest.c",testUtils], LIBS=[libbcg729])
postProcessingTest = env.Program(source=["test/src/postProcessingTest.c",testUtils], LIBS=[libbcg729])
preProcessingTest = env.Program(source=["test/src/preProcessingTest.c",testUtils], LIBS=[libbcg729])

tests = [adaptativeCodebookSearchTest, computeAdaptativeCodebookGainTest, computeLPTest, computeWeightedSpeechTest, decodeAdaptativeCodeVectorTest, decodeFixedCodeVectorTest, decodeGainsTest,
         decodeLSPTest, decoderMultiChannelTest, decoderTest, encoderMultiChannelTest, encoderTest, findOpenLoopPitchDelayTest, fixedCodebookSearchTest, g729FixedPointMathTest, gainQuantizationTest,
         interpolateqLSPAndConvert2LPTest, LP2LSPConversionTest, LPSynthesisFilterTest, LSPQuantizationTest, postFilterTest, postProcessingTest, preProcessingTest]

decoder = env.Program(source=["example/decoder.c"], LIBS=[libbcg729])
encoder = env.Program(source=["example/encoder.c"], LIBS=[libbcg729])

env.Default([libbcg729, tests, decoder, encoder])
