from feature_counter import FeatureCounter
from feature_visitor import FeatureVisitor

if __name__ == "__main__":
    repo_url = 'https://github.com/conda/conda.git'
    feature_counter = FeatureCounter(repo_url, FeatureVisitor)
    feature_counter.process()
    feature_counter.export_to_csv('feature_counts.csv')