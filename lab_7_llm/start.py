"""
Starter for demonstration of laboratory work.
"""
# pylint: disable= too-many-locals, undefined-variable, unused-import
import json
from pathlib import Path

from core_utils.llm.time_decorator import report_time
from lab_7_llm.main import (
    LLMPipeline,
    RawDataImporter,
    RawDataPreprocessor,
    TaskDataset,
    TaskEvaluator,
)

from core_utils.llm.metrics import Metrics

@report_time
def main() -> None:
    """
    Run the translation pipeline.
    """
    with open(Path(__file__).parent / "settings.json", encoding="utf-8") as f:
        settings = json.load(f)

    importer = RawDataImporter(settings['parameters']['dataset'])
    importer.obtain()

    preprocessor = RawDataPreprocessor(importer.raw_data)
    dataset_analysis = preprocessor.analyze()
    preprocessor.transform()

    BATCH_SIZE = 1
    MAX_LENGTH = 120
    DEVICE = 'cpu'

    dataset = TaskDataset(preprocessor.data.head(100))
    pipeline = LLMPipeline(settings['parameters']['model'], dataset, MAX_LENGTH, BATCH_SIZE, DEVICE)
    model_analysis = pipeline.analyze_model()
    predictions = pipeline.infer_dataset()

    PREDICTIONS_PATH = Path(__file__).parent / 'dist' / 'predictions.csv'
    PREDICTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(PREDICTIONS_PATH, index=False)

    metrics = [Metrics(metric) for metric in settings['parameters']['metrics']]
    evaluator = TaskEvaluator(PREDICTIONS_PATH, metrics)
    result = evaluator.run()
    assert result is not None, "Demo does not work correctly"


if __name__ == "__main__":
    main()
