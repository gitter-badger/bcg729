#!/usr/bin/env scons

env = Environment(platform="win32", tools=["mingw"])

CCFLAGS = ["-Iinclude"]

# Static Library
libbcg729_sources = [
    "src/adaptativeCodebookSearch.c",
    "src/codebooks.c",
    "src/computeAdaptativeCodebookGain.c",
    "src/computeLP.c",
    "src/computeWeightedSpeech.c",
    "src/decodeAdaptativeCodeVector.c",
    "src/decodeFixedCodeVector.c",
    "src/decodeGains.c",
    "src/decodeLSP.c",
    "src/decoder.c",
    "src/encoder.c",
    "src/findOpenLoopPitchDelay.c",
    "src/fixedCodebookSearch.c",
    "src/gainQuantization.c",
    "src/interpolateqLSP.c",
    "src/LP2LSPConversion.c",
    "src/LPSynthesisFilter.c",
    "src/LSPQuantization.c",
    "src/postFilter.c",
    "src/postProcessing.c",
    "src/preProcessing.c",
    "src/qLSP2LP.c",
    "src/utils.c"
]
libbcg729 = env.StaticLibrary(source=libbcg729_sources, target="bcg729", CCFLAGS=CCFLAGS)

decoder = env.Program(source=["example/decoder.c"], LIBS=[libbcg729], CCFLAGS=CCFLAGS)
encoder = env.Program(source=["example/encoder.c"], LIBS=[libbcg729], CCFLAGS=CCFLAGS)

examples = [decoder, encoder]

env.Default([libbcg729, examples])
