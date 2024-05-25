import numpy as np


# KNN
def minkowski_distance(a, b, p=2):
    """
    Compute the Minkowski distance between two arrays.

    Args:
        a (np.ndarray): First array.
        b (np.ndarray): Second array.
        p (int, optional): The degree of the Minkowski distance. Defaults to 2 (Euclidean distance).

    Returns:
        float: Minkowski distance between arrays a and b.
    """
    distancia = 0
    for i in range(len(a)):
        distancia += abs(a[i] - b[i]) ** p
    distancia = distancia ** (1 / p)
    return distancia


class knn:
    def __init__(self):
        self.k = None  # k es el numero de vecinos
        self.p = None
        self.x_train = None
        self.y_train = None

    def fit(self, X_train: np.ndarray, y_train: np.ndarray, k: int = 5, p: int = 2):
        """
        Fit the model using X as training data and y as target values.

        You should check that all the arguments shall have valid values:
            X and y have the same number of rows.
            k is a positive integer.
            p is a positive integer.

        Args:
            X_train (np.ndarray): Training data.
            y_train (np.ndarray): Target values.
            k (int, optional): Number of neighbors to use. Defaults to 5.
            p (int, optional): The degree of the Minkowski distance. Defaults to 2.
        """
        self.k = k
        self.p = p
        self.x_train = X_train
        self.y_train = y_train

    def compute_distances(self, point: np.ndarray) -> np.ndarray:
        """Compute distance from a point to every point in the training dataset

        Args:
            point (np.ndarray): data sample.

        Returns:
            np.ndarray: distance from point to each point in the training dataset.
        """
        distances = []
        for train_point in self.x_train:
            distance = minkowski_distance(point, train_point)
            distances.append(distance)  # El punto de indice 1 estará e x distancia
        return np.array(distances)

    def get_k_nearest_neighbors(self, distances: np.ndarray) -> np.ndarray:
        """Get the k nearest neighbors indices given the distances matrix from a point.

        Args:
            distances (np.ndarray): distances matrix from a point whose neighbors want to be identified.

        Returns:
            np.ndarray: row indices from the k nearest neighbors.

        Hint:
            You might want to check the np.argsort function.
        """
        return np.argsort(distances)[0 : self.k]

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict the class labels for the provided data.

        Args:
            X (np.ndarray): data samples to predict their labels.

        Returns:
            np.ndarray: Predicted class labels.
        """
        clases = []
        for point in X:
            distances = self.compute_distances(point)
            vecinos_indices = self.get_k_nearest_neighbors(distances)
            yes = 0
            no = 0
            for indice in vecinos_indices:
                clase = self.y_train[indice]
                if clase == 1:
                    yes += 1
                elif clase == 0:
                    no += 1
            if no > yes:
                clases.append(0)
            else:
                clases.append(1)
        return np.array(clases)

    def predict_proba(self, X):
        """
        Predict the class probabilities for the provided data.

        Each class probability is the amount of each label from the k nearest neighbors
        divided by k.

        Args:
            X (np.ndarray): data samples to predict their labels.

        Returns:
            np.ndarray: Predicted class probabilities.
        """
        probabilites = []
        for point in X:
            distances = self.compute_distances(point)
            vecinos_indices = self.get_k_nearest_neighbors(distances)
            yes = 0
            no = 0
            for indice in vecinos_indices:
                clase = self.y_train[indice]
                if clase == 1:
                    yes += 1
                elif clase == 0:
                    no += 1
            probabilites.append([no / (no + yes), yes / (no + yes)])
        return np.array(probabilites)

    def most_common_label(self, knn_labels: np.ndarray) -> int:
        """Obtain the most common label from the labels of the k nearest neighbors

        Args:
            knn_labels (np.ndarray): labels from the k nearest neighbors

        Returns:
            int: most common label
        """
        # Lo hago directamente

    def __str__(self):
        """
        String representation of the kNN model.
        """
        return f"kNN model (k={self.k}, p={self.p})"
    

# Regresión logística 


class LogisticRegressor:
    def __init__(self):
        """
        Initializes the Logistic Regressor model.

        Attributes:
        - weights (np.ndarray): A placeholder for the weights of the model. 
                                These will be initialized in the training phase.
        - bias (float): A placeholder for the bias of the model. 
                        This will also be initialized in the training phase.
        """
        self.coefficients = None
        self.intercept = None
    

    
    def fit(self, X, y, learning_rate = 0.01, num_iterations = 1000, 
            penalty = None, l1_ratio = 0.5, C = 1.0, verbose = False, print_every = 100):
        """
        Fits the logistic regression model to the data using gradient descent. 
        
        This method initializes the model's weights and bias, then iteratively updates these parameters by 
        moving in the direction of the negative gradient of the loss function (computed using the 
        log_likelihood method).

        The regularization terms are added to the gradient of the loss function as follows:

        - No regularization: The standard gradient descent updates are applied without any modification.

        - L1 (Lasso) regularization: Adds a term to the gradient that penalizes the absolute value of 
            the weights, encouraging sparsity. The update rule for weight w_j is adjusted as follows:
            dw_j += (C / m) * sign(w_j) - Make sure you understand this!

        - L2 (Ridge) regularization: Adds a term to the gradient that penalizes the square of the weights, 
            discouraging large weights. The update rule for weight w_j is:
            dw_j += (C / m) * w_j       - Make sure you understand this!
            

        - ElasticNet regularization: Combines L1 and L2 penalties. 
            The update rule incorporates both the sign and the magnitude of the weights:
            dw_j += l1_ratio * gradient_of_lasso + (1 - l1_ratio) * gradient_of_ridge


        Parameters:
        - X (np.ndarray): The input features, with shape (m, n), where m is the number of examples and n is
                            the number of features.
        - y (np.ndarray): The true labels of the data, with shape (m,).
        - learning_rate (float): The step size at each iteration while moving toward a minimum of the 
                            loss function.
        - num_iterations (int): The number of iterations for which the optimization algorithm should run.
        - penalty (str): Type of regularization (None, 'lasso', 'ridge', 'elasticnet'). Default is None.
        - l1_ratio (float): The Elastic Net mixing parameter, with 0 <= l1_ratio <= 1. 
                            l1_ratio=0 corresponds to L2 penalty, 
                            l1_ratio=1 to L1. Only used if penalty='elasticnet'. 
                            Default is 0.5.
        - C (float): Inverse of regularization strength; must be a positive float. 
                            Smaller values specify stronger regularization.
        - verbose (bool): Print loss every print_every iterations.
        - print_every (int): Period of number of iterations to show the loss.



        Updates:
        - self.coefficients: The weights of the model after training.
        - self.intercept: The bias of the model after training.
        """
        # TODO: Obtain m (number of examples) and n (number of features)
        m = X.shape[0]  # m es el numero de filas 
        n = X.shape[1] # n el de columnas
        
        # TODO: Initialize all parameters to 0        
        self.coefficients = np.zeros((n)) # Es n-1 ya que X lo mandamos con el 1 metido, por tanto ese 1 va con el intercept 
        self.intercept = 0

        # TODO: Complete the gradient descent code
        # Tip: You can use the code you had in the previous practice
        # Execute the iterative gradient descent
        for i in range(num_iterations):                              # Fill the None here 
    
            # For these two next lines, you will need to implement the respective functions
            # Logging
            # Forward propagation
            y_hat = self.predict_proba(X) # Esto es un vector, son las probabilidades de pertenecer a las clase 1
                
            if i % print_every == 0 and verbose:
                '''Metemos esto aquí para mayor eficiencia'''
                # Compute loss
                loss = self.log_likelihood(y, y_hat) # Esto es un numero, es la pérdida, es cuánto se parecen las clases predichas a las reales 
                print(f"Iteration {i}: Loss {loss}")

            # TODO: Implement the gradient values 
            # CAREFUL! You need to calculate the gradient of the loss function (*negative log-likelihood*)
            # y[y == 0] = -1
            # '''Codificamos los 0 como -1 para que la función a optimizar sea más sencilla'''
            # w = np.insert(self.coefficients, 0, self.intercept)
            # gradient = np.array([]) # Calculamos el gradiente para cada iteración 
            # for i in range(len(w)): # para cada parámetro  de w calculamos la derivada respecto del parámetro 
            #     # DERIVADA
            #     '''Aplicamos mini batch para mejorar la eficiencia'''
            #     # Definir el tamaño del conjunto de filas que deseas seleccionar (por ejemplo, n=2)
            #     n = 100
            #     # Seleccionar filas aleatorias
            #     indices_aleatorios = np.random.choice(np.arange(0, m ), size=n, replace=False)
                
            #     derivada = 0 
            #     clip = 5000 # Valor en el que se corta para evitar errores de overflow con las exponenciales 
            #     for j in indices_aleatorios: # para cada fila de X 
            #         logit = np.clip(np.dot(X[j],w), -clip, clip) # Hacemos un clip para evitar valores que causen overflow
            #         derivada += (1/(1+np.exp(-y[j]*logit))) * np.exp(-y[j]*logit) *(-y[j]) * X[j][i] # la x de la fila j que va con el parámetro i 
                    
            #     gradient = np.append(gradient,derivada)
        
    
            # # TODO: Write the gradient values and the updates for the paramenters
    
            # dw = gradient[1:]
            # db = gradient[0]
            '''Utilizamos mejor esta versión'''
            dw = (1 / m) * np.dot(X.T, (y_hat - y)) # por qué haces 1/m ?
            db = (1 / m) * np.sum(y_hat - y)

            # Regularization: 
            # Apply regularization if it is selected.
            # We feed the regularization method the needed values, where "dw" is the derivative for the 
            # coefficients, "m" is the number of examples and "C" is the regularization hyperparameter.
            # To do this, you will need to complete each regularization method.
            if penalty == 'lasso':
                dw = self.lasso_regularization(dw, m, C)
            elif penalty == 'ridge':
                dw = self.ridge_regularization(dw, m, C)
            elif penalty == 'elasticnet':
                dw = self.elasticnet_regularization(dw, m, C, l1_ratio)

            # Update parameters

            self.coefficients -= learning_rate * dw
            self.intercept -= learning_rate * db

    def predict_proba(self, X): # Predice la porbabilidad de que sea de la clase 1 
        """
        Predicts probability estimates for all classes for each sample X.

        Parameters:
        - X (np.ndarray): The input features, with shape (m, n), where m is the number of samples and 
            n is the number of features.

        Returns:
        - A numpy array of shape (m, 1) containing the probability of the positive class for each sample.
        """
        
        # TODO: z is the value of the logits. Write it here (use self.coefficients and self.intercept):
    
        z = []
        # w = np.insert(self.coefficients, 0, self.intercept)

        # z = [self.intercept + np.dot(fila, self.coefficients) for fila in X]
        z = self.intercept + np.dot(X, self.coefficients)
    
        # Return the associated probabilities via the sigmoid trasnformation (symmetric choice)
        sigmoids = self.sigmoid(z)
    
        return sigmoids

    def predict(self, X, threshold=0.5): # Esta función da una solución dura
        """
        Predicts class labels for samples in X.

        Parameters:
        - X (np.ndarray): The input features, with shape (m, n), where m is the number of samples and n 
                            is the number of features.
        - threshold (float): Threshold used to convert probabilities into binary class labels. 
                            Defaults to 0.5.

        Returns:
        - A numpy array of shape (m,) containing the class label (0 or 1) for each sample.
        """
        
        # TODO: Predict the class for each input data given the threshold in the argument
        probabilities = self.predict_proba(X) # Esto devuelve las probabilidades de pertenecer a la clase 1
        classification_result =  np.array([1 if prob >= threshold else 0 for prob in probabilities])
        return classification_result
    # Reguralizaciones
    # .....................................................................................................................................................................
    def lasso_regularization(self, dw, m, C):
        """
        Applies L1 regularization (Lasso) to the gradient during the weight update step in gradient descent. 
        L1 regularization encourages sparsity in the model weights, potentially setting some weights to zero, 
        which can serve as a form of feature selection.

        The L1 regularization term is added directly to the gradient of the loss function with respect to 
        the weights. This term is proportional to the sign of each weight, scaled by the regularization 
        strength (C) and inversely proportional to the number of samples (m).

        Parameters:
        - dw (np.ndarray): The gradient of the loss function with respect to the weights, before regularization.
        - m (int): The number of samples in the dataset.
        - C (float): Inverse of regularization strength; must be a positive float. 
                    Smaller values specify stronger regularization.

        Returns:
        - np.ndarray: The adjusted gradient of the loss function with respect to the weights, 
                    after applying L1 regularization.
        """
        
        # TODO: 
        # ADD THE LASSO CONTRIBUTION TO THE DERIVATIVE OF THE OBJECTIVE FUNCTION
        lasso_gradient = (C/m) * np.sign(self.coefficients)
        return dw + lasso_gradient
    
    
    def ridge_regularization(self, dw, m, C):
        """
        Applies L2 regularization (Ridge) to the gradient during the weight update step in gradient descent. 
        L2 regularization penalizes the square of the weights, which discourages large weights and helps to 
        prevent overfitting by promoting smaller and more distributed weight values.

        The L2 regularization term is added to the gradient of the loss function with respect to the weights
        as a term proportional to each weight, scaled by the regularization strength (C) and inversely 
        proportional to the number of samples (m).

        Parameters:
        - dw (np.ndarray): The gradient of the loss function with respect to the weights, before regularization.
        - m (int): The number of samples in the dataset.
        - C (float): Inverse of regularization strength; must be a positive float. 
                    Smaller values specify stronger regularization.

        Returns:
        - np.ndarray: The adjusted gradient of the loss function with respect to the weights, 
                        after applying L2 regularization.
        """
        
        # TODO: 
        # ADD THE RIDGE CONTRIBUTION TO THE DERIVATIVE OF THE OBJECTIVE FUNCTION
        ridge_gradient = (C/m) * self.coefficients 
        return dw + ridge_gradient

    def elasticnet_regularization(self, dw, m, C, l1_ratio):
        """
        Applies Elastic Net regularization to the gradient during the weight update step in gradient descent. 
        Elastic Net combines L1 and L2 regularization, incorporating both the sparsity-inducing properties 
        of L1 and the weight shrinkage effect of L2. This can lead to a model that is robust to various types 
        of data and prevents overfitting.

        The regularization term combines the L1 and L2 terms, scaled by the regularization strength (C) and 
        the mix ratio (l1_ratio) between L1 and L2 regularization. The term is inversely proportional to the 
        number of samples (m).

        Parameters:
        - dw (np.ndarray): The gradient of the loss function with respect to the weights, before regularization.
        - m (int): The number of samples in the dataset.
        - C (float): Inverse of regularization strength; must be a positive float. 
                    Smaller values specify stronger regularization.
        - l1_ratio (float): The Elastic Net mixing parameter, with 0 <= l1_ratio <= 1. l1_ratio=0 corresponds
                            to L2 penalty, l1_ratio=1 to L1. Only used if penalty='elasticnet'. 
                            Default is 0.5.

        Returns:
        - np.ndarray: The adjusted gradient of the loss function with respect to the weights, 
                    after applying Elastic Net regularization.
        """
        # TODO: 
        # ADD THE RIDGE CONTRIBUTION TO THE DERIVATIVE OF THE OBJECTIVE FUNCTION
        # Be careful! You can reuse the previous results and combine them here, but beware how you do this!
        elasticnet_gradient = (C/m)*(((1-l1_ratio)*self.coefficients) + ((l1_ratio)*np.sign(self.coefficients)))
        return dw + elasticnet_gradient

    # .............................................................................................................................................................
    @staticmethod
    def log_likelihood(y, y_hat): # Esto no es la verosimilitud que vamos a maximizar, esto es una medida de cómo de bien se hace la predicción de la clase.
        """
        Computes the Log-Likelihood loss for logistic regression, which is equivalent to
        computing the cross-entropy loss between the true labels and predicted probabilities. 
        This loss function is used to measure how well the model predicts the actual class 
        labels. The formula for the loss is:

        L(y, y_hat) = -(1/m) * sum(y * log(y_hat) + (1 - y) * log(1 - y_hat))

        where:
        - L(y, y_hat) is the loss function,
        - m is the number of observations,
        - y is the actual label of the observation,
        - y_hat is the predicted probability that the observation is of the positive class,
        - log is the natural logarithm.

        Parameters:
        - y (np.ndarray): The true labels of the data. Should be a 1D array of binary values (0 or 1).
        - y_hat (np.ndarray): The predicted probabilities of the data belonging to the positive class (1). 
                            Should be a 1D array with values between 0 and 1.

        Returns:
        - The computed loss value as a scalar.
        """
        # y[y == -1] = 0 (esto es por si lo queremos hacer codificando como -1 y 1)
        '''Este paso es necesario y fundamental, ya que la y_hat lo que tendrá es 'la probabilidad de pertenecer a la clase 1',
        es decir, un numero entre 0 y 1 donde el 0 representa que tiene probabilidad 0 de pertenecer a la clase 1.
        Antes hemos codificado el 0 como -1 para hacer el descenso gradiente, como la y_hat devuelve valores entre 0 y 1 y estamos comparando la y con la y_hat 
        es necesario codificar los -1 de la y como 0. 
        '''
        # TODO: Implement the loss function (log-likelihood)
        m = y.shape[0] # Number of examples
        epsilon = 1e-15 # definimos este epsilon para evitar logaritmos de 0 
        loss = -(1/m) * np.sum(np.dot(y,np.log(y_hat + epsilon)) + np.dot(1-y,np.log(1-y_hat + epsilon)))
        return loss

    @staticmethod
    def sigmoid(z):
        """
        Computes the sigmoid of z, a scalar or numpy array of any size. The sigmoid function is used as the 
        activation function in logistic regression, mapping any real-valued number into the range (0, 1), 
        which can be interpreted as a probability. It is defined as 1 / (1 + exp(-z)), where exp(-z) 
        is the exponential of the negative of z.

        Parameters:
        - z (float or np.ndarray): Input value or array for which to compute the sigmoid function.

        Returns:
        - The sigmoid of z. 
        """
        
        # TODO: Implement the sigmoid function to convert the logits into probabilities
        '''
        sigmoid_values = []
        for value in z:
            value = np.clip(value,-500,500)
            sigmoid_values.append(1/(1+np.exp(-value)))
        '''

        return 1/(1+np.exp(-z))



