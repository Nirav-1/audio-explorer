import numpy as np
import pandas as pd
import yaafelib


class YaafeWrapper(object):

    def __init__(self, fs: int, block_size=512, step_size=None):
        if not step_size:
            step_size = block_size // 2

        features_config = {
            'Chroma2': f'Chroma2 CQTAlign=c  CQTBinsPerOctave=48  CQTMinFreq=27.5  CQTNbOctaves=7  CZBinsPerSemitone=1  CZNbCQTBinsAggregatedToPCPBin=-1  CZTuning=440  stepSize={step_size}',
            'LPC': f'LPC LPCNbCoeffs=2  blockSize={block_size}  stepSize={step_size}',
            'LSF': f'LSF blockSize={block_size}  stepSize={step_size}',
            'MFCC2': f'MFCC CepsIgnoreFirstCoeff=1  CepsNbCoeffs=13  FFTWindow=Hanning  MelMaxFreq=5000.0  MelMinFreq=400.0  MelNbFilters=40  blockSize={block_size}  stepSize={step_size}',
            'OBSI': f'OBSI FFTLength=0  FFTWindow=Hanning  OBSIMinFreq=27.5  blockSize={block_size}  stepSize={step_size}',
            'OBSIR': f'OBSIR DiffNbCoeffs=0  FFTLength=0  FFTWindow=Hanning  OBSIMinFreq=27.5  blockSize={block_size}  stepSize={step_size}',
            'PerceptualSharpness': f'PerceptualSharpness FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'PerceptualSpread': f'PerceptualSpread FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'SpectralCrestFactorPerBand': f'SpectralCrestFactorPerBand FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'SpectralDecrease': f'SpectralDecrease FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'SpectralFlatness': f'SpectralFlatness FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'SpectralFlatnessPerBand': f'SpectralFlatnessPerBand FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'SpectralFlux': f'SpectralFlux FFTLength=0  FFTWindow=Hanning  FluxSupport=All  blockSize={block_size}  stepSize={step_size}',
            'SpectralRolloff': f'SpectralRolloff FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'SpectralShapeStatistics': f'SpectralShapeStatistics FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'SpectralSlope': f'SpectralSlope FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'SpectralVariation': f'SpectralVariation FFTLength=0  FFTWindow=Hanning  blockSize={block_size}  stepSize={step_size}',
            'ZCR': f'ZCR blockSize={block_size}  stepSize={step_size}'
        }

        self.fs = fs
        feature_plan = yaafelib.FeaturePlan(sample_rate=fs, normalize=True)
        for feature_name, setting in features_config.items():
            feature_plan.addFeature(feature_name + ': ' + setting)
        data_flow = feature_plan.getDataFlow()
        self.engine = yaafelib.Engine()
        self.engine.load(data_flow)

    def get_features(self, audio_data: np.ndarray) -> dict:
        features = self.engine.processAudio(audio_data.reshape(1, -1).astype('float64'))
        return features

    def get_mean_features(self, audio_data: np.ndarray) -> dict:
        features = self.engine.processAudio(audio_data.reshape(1, -1).astype('float64'))

        flat_dict = {}
        for name, values in features.items():
            if values.shape[1] == 1:
                flat_dict[name] = values.mean()
            else:
                d = {f'{name}_{idx}': value for idx, value in enumerate(list(values.mean(axis=0)))}
                flat_dict.update(d)
        return flat_dict

    def get_mean_features_as_series(self, audio_data: np.ndarray) -> pd.Series:
        flat_dict = self.get_mean_features(audio_data)
        return pd.Series(flat_dict)



