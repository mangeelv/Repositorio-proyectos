import numpy as np
from sklearn.metrics import accuracy_score

def train_test_split(X, y, test_size=0.2, stratify=None, random_state=None):
    """
    Splits arrays or matrices into random train and test subsets. This function demonstrates how to 
    divide a dataset into training and testing sets, optionally stratifying the samples and ensuring 
    reproducibility with a random state.

    Parameters:
    - X (np.ndarray): Input features matrix, where rows represent samples and columns represent features.
    - y (np.ndarray): Target labels array, aligned with the samples in X.
    - test_size (float or int): Determines the size of the test set. If float, it represents a proportion 
                                of the dataset; if int, it specifies the number of samples.
    - stratify (np.ndarray): If provided, the function will ensure the class proportions in train and test 
                             sets mirror those of the provided array, typically the target labels array.
    - random_state (int): Seed for the random number generator to ensure reproducible splits.

    Returns:
    - X_train, X_test, y_train, y_test: Arrays containing the split of features and labels into training and 
                                        test sets.
    """
    # Set the seed for reproducibility
    if random_state:
        np.random.seed(random_state)
    # Determine the number of samples to allocate to the test set
    n_samples = X.shape[0]
    if isinstance(test_size, float):
        n_test = int(n_samples * test_size)
    else:
        n_test = test_size
    n_train = n_samples - n_test
    # Create an array of indices and shuffle if not stratifying
    indices = np.arange(n_samples)
    if stratify is None:
        np.random.shuffle(indices)
    else:
        # For stratified splitting, determine the distribution of classes
        unique_classes, y_indices = np.unique(stratify, return_inverse=True)
        class_counts = np.bincount(y_indices)
        test_counts = np.round(class_counts * test_size).astype(int)

        # Allocate indices to train and test sets preserving class distribution
        train_indices, test_indices = [], []
        for class_index in range(len(unique_classes)):
            class_indices = indices[y_indices == class_index]
            np.random.shuffle(class_indices)
            boundary = test_counts[class_index]
            test_indices.extend(class_indices[:boundary])
            train_indices.extend(class_indices[boundary:])
        # Concatenate indices to form the final split
        indices = train_indices + test_indices
    # Use the indices to partition the dataset
    X_train = X[indices[:n_train]]
    X_test = X[indices[n_train:]]
    y_train = y[indices[:n_train]]
    y_test = y[indices[n_train:]]
    return X_train, X_test, y_train, y_test

def evaluate_classification_metrics(y_true, y_pred, positive_label):
    """
    Calculate various evaluation metrics for a classification model.

    Args:
        y_true (array-like): True labels of the data.
        positive_label: The label considered as the positive class.
        y_pred (array-like): Predicted labels by the model.

    Returns:
        dict: A dictionary containing various evaluation metrics.

    Metrics Calculated:
        - Confusion Matrix: [TN, FP, FN, TP]
        - Accuracy: (TP + TN) / (TP + TN + FP + FN)
        - Precision: TP / (TP + FP)
        - Recall (Sensitivity): TP / (TP + FN)
        - Specificity: TN / (TN + FP)
        - F1 Score: 2 * (Precision * Recall) / (Precision + Recall)
    """
    if positive_label == 'YES':
        possitive = 1
    else:
        possitive = 0 
    # Map string labels to 0 or 1
    y_true_mapped = np.array([1 if label == positive_label else 0 for label in y_true])
    y_pred_mapped = np.array([1 if label == positive_label else 0 for label in y_pred])
    

    # Confusion Matrix
    tp = 0 
    fp = 0
    tn = 0 
    fn = 0 
    for i in range(len(y_true_mapped)):
        if y_pred_mapped[i] == 1 and y_true_mapped[i] == 1:
            tp += 1
        elif y_pred_mapped[i] == 1 and y_true_mapped[i] == 0:
            fp += 1
        elif y_pred_mapped[i]== 0 and y_true_mapped[i] == 0:
            tn += 1
        elif y_pred_mapped[i] == 0 and y_true_mapped[i] == 1:
            fn += 1 

    # Accuracy
    accuracy = (tp+tn) / (tp+tn+fp+fn)

    # Precision
    precision = (tp) / (tp+fp)

    # Recall (Sensitivity)
    recall = (tp) / (tp+fn)

    # Specificity
    specificity = (tn) / (tn+fp)

    # F1 Score
    f1 = 1 - specificity
   
    return {
        'Confusion Matrix': [tn, fp, fn, tp],
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'Specificity': specificity,
        'F1 Score': f1
    }
  




def cross_validationknn(model, X, y, nFolds):
    """
    Perform cross-validation on a given machine learning model to evaluate its performance.
    
    This function manually implements n-fold cross-validation if a specific number of folds is provided.
    If nFolds is set to -1, Leave One Out (LOO) cross-validation is performed instead, which uses each
    data point as a single test set while the rest of the data serves as the training set.
    
    Parameters:
    - model: scikit-learn-like estimator
        The machine learning model to be evaluated. This model must implement the .fit() and .score() methods
        similar to scikit-learn models.
    - X: array-like of shape (n_samples, n_features)
        The input features to be used for training and testing the model.
    - y: array-like of shape (n_samples,)
        The target values (class labels in classification, real numbers in regression) for the input samples.
    - nFolds: int
        The number of folds to use for cross-validation. If set to -1, LOO cross-validation is performed.
    
    Returns:
    - mean_score: float
        The mean score across all cross-validation folds.
    - std_score: float
        The standard deviation of the scores across all cross-validation folds, indicating the variability
        of the score across folds.
    
    Example:
    --------
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.datasets import make_classification
    
    # Generate a synthetic dataset
    X, y = make_classification(n_samples=100, n_features=20, n_classes=2, random_state=42)
    
    # Initialize a kNN model
    model = KNeighborsClassifier(n_neighbors=5)
    
    # Perform 5-fold cross-validation
    mean_score, std_score = cross_validation(model, X, y, nFolds=5)
    
    print(f'Mean CV Score: {mean_score}, Std Deviation: {std_score}')
    """
    if nFolds == -1:
        # Implement Leave One Out CV
        nFolds = X.shape[0]
        accuracy_scores = np.array([])
        for i in range(nFolds): 
            X_train = np.delete(X, i, axis=0)
            y_train = np.delete(y, i, axis=0)
            model.fit(X_train, y_train)
            score = model.score(X[i].reshape(1, -1),y[i].reshape(1, -1))
            accuracy_scores = np.append(accuracy_scores,score)
    else:
        # TODO: Calculate fold_size based on the number of folds
        fold_size = X.shape[0]//nFolds

        # TODO: Initialize a list to store the accuracy values of the model for each fold
        accuracy_scores = np.array([])
        j = 0 
        for i in range(nFolds):
            # TODO: Generate indices of samples for the validation set for the fold
            valid_indices = list(range(j,j+fold_size))
            # TODO: Generate indices of samples for the training set for the fold
            train_indices = [x for x in range(X.shape[0]) if x < j or x >= j+fold_size]
            j = j+fold_size
        
            # TODO: Split the dataset into training and validation
            X_train, X_valid = X[train_indices], X[valid_indices]
            y_train, y_valid = y[train_indices], y[valid_indices]
            
            # TODO: Train the model with the training set
         
            model.fit(X_train,y_train)
            # TODO: Calculate the accuracy of the model with the validation set and store it in accuracy_scores
            score = model.score(X_valid,y_valid)
            accuracy_scores = np.append(accuracy_scores,score)
        
    
    # TODO: Return the mean and standard deviation of the accuracy_scores 
    return np.mean(accuracy_scores), (1/(len(accuracy_scores)-1))*np.std(accuracy_scores) # No es esto, es la desviación estandar de la media, es la 
    # desviación estándar del estimador media muestral Es cómo de mal estoy estimando la media 
    # Si   no se pone esto, la desviación típica crece con los datos  


def cross_validationlogreg(model, X, y, nFolds):

    if nFolds == -1:
        # Implement Leave One Out CV
        nFolds = X.shape[0]
        accuracy_scores = np.array([])
        for i in range(nFolds): 
            X_train = np.delete(X, i, axis=0)
            y_train = np.delete(y, i, axis=0)
            model.fit(X_train, y_train)
            y_pred = model.predict(X[i].reshape(1, -1))
            score = accuracy_score(y[i].reshape(1, -1), y_pred)
            # score = model.score(X[i].reshape(1, -1),y[i].reshape(1, -1))
            accuracy_scores = np.append(accuracy_scores,score)
    else:
        # TODO: Calculate fold_size based on the number of folds
        fold_size = X.shape[0]//nFolds

        # TODO: Initialize a list to store the accuracy values of the model for each fold
        accuracy_scores = np.array([])
        j = 0 
        for i in range(nFolds):
            # TODO: Generate indices of samples for the validation set for the fold
            valid_indices = list(range(j,j+fold_size))
            # TODO: Generate indices of samples for the training set for the fold
            train_indices = [x for x in range(X.shape[0]) if x < j or x >= j+fold_size]
            j = j+fold_size
        
            # TODO: Split the dataset into training and validation
            X_train, X_valid = X[train_indices], X[valid_indices]
            y_train, y_valid = y[train_indices], y[valid_indices]
            
            # TODO: Train the model with the training set
         
            model.fit(X_train,y_train)
            # TODO: Calculate the accuracy of the model with the validation set and store it in accuracy_scores
            y_pred = model.predict(X[i].reshape(1, -1))
            score = accuracy_score(y[i].reshape(1, -1), y_pred)
            accuracy_scores = np.append(accuracy_scores,score)
        
    
    # TODO: Return the mean and standard deviation of the accuracy_scores 
    return np.mean(accuracy_scores), (1/(len(accuracy_scores)-1))*np.std(accuracy_scores) # No es esto, es la desviación estandar de la media, es la 
    # desviación estándar del estimador media muestral Es cómo de mal estoy estimando la media 
    # Si   no se pone esto, la desviación típica crece con los datos  

