from feature_counter import FeatureCounter
from type_hint_visitor import TypeHintVisitor

if __name__ == "__main__":
    repo_url = 'https://github.com/conda/conda.git'
    feature_counter = FeatureCounter(repo_url, [TypeHintVisitor])
    feature_counter.process()
    feature_counter.export_to_csv('conda.csv')