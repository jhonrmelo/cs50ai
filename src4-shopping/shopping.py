import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def get_int_from_boolean(boolean):
    if boolean == "FALSE":
        return 0 
    
    return 1

def get_visitor_type(visitor_type):
    if visitor_type == "Returning":
        return 1
    
    return 0

def load_data(filename):
    mon_to_number = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11,  
    }
    
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        evidence, labels = [], []
        for row_from_header in reader:
            row = []
            labels.append(get_int_from_boolean(row_from_header[17]))
            
            row.append(int(row_from_header[0]))
            row.append(float(row_from_header[1]))
            row.append(int(row_from_header[2]))
            row.append(float(row_from_header[3]))
            row.append(int(row_from_header[4]))
            row.append(float(row_from_header[5]))
            row.append(float(row_from_header[6]))
            row.append(float(row_from_header[7]))
            row.append(float(row_from_header[8]))
            row.append(float(row_from_header[9]))
            row.append(int(mon_to_number[row_from_header[10]]))
            row.append(int(row_from_header[11]))
            row.append(int(row_from_header[12]))
            row.append(int(row_from_header[13]))
            row.append(int(row_from_header[14]))
            row.append(get_visitor_type(row_from_header[15]))
            row.append(get_int_from_boolean(row_from_header[16]))

            evidence.append(row)

    return (evidence, labels)

def train_model(evidence, labels):
    
    model = KNeighborsClassifier(n_neighbors=1)
    
    model.fit(evidence, labels)
    
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_negatives = 0
    true_positives = 0
    negatives = 0
    positives = 0
    for i in range(len(labels)):
        if(labels[i] == 1):
            positives +=1
            if(predictions[i]) == 1:
                true_positives += 1
        elif(labels[i] == 0):
            negatives +=1
            if(predictions[i] == 0):
                true_negatives += 1
    
    sensitivity = true_positives / positives
    specificity = true_negatives / negatives
    
    
    return (sensitivity, specificity)
    
            
        
    raise NotImplementedError


if __name__ == "__main__":
    main()
