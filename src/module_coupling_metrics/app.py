import argparse
import csv
import matplotlib.pyplot
import pandas
import seaborn
from . import reflection, metrics


def save_as_csv(filename, metrics_results):
    with open('%s.csv' % filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Component', 'Instability', 'Abstractness', 'Distance'])
        for (name, component) in metrics_results.items():
            writer.writerow(
                [name, component.instability, component.abstractness, component.distance_from_main_sequence])


def save_as_png(filename, metrics_results):
    data = pandas.DataFrame.from_records([c.__dict__ for c in metrics_results.values()])
    seaborn.scatterplot(data=data, x="instability", y="abstractness").set_title(filename)
    matplotlib.pyplot.savefig('%s.png' % filename)


def main():
    parser = argparse.ArgumentParser(description='Compute some module coupling metrics.')
    parser.add_argument('top_level_folder', metavar='FOLDER', type=str,
                        help='top level folder of the project to analyze')
    args = parser.parse_args()
    project = reflection.load_project_structure(args.top_level_folder)
    result = metrics.compute(project)
    save_as_csv(project.name, result)
    save_as_png(project.name, result)
