import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import models, layers

# OPGAVE 1a


def plot_image(img, label):
    # Deze methode krijgt een matrix mee (in img) en een label dat correspondeert met het
    # plaatje dat in de matrix is weergegeven. Zorg ervoor dat dit grafisch wordt weergegeven.
    # Maak gebruik van plt.cm.binary voor de cmap-parameter van plt.imgshow.

    # YOUR CODE HERE
    plt.matshow(img, cmap='Greys')
    plt.xlabel(label)
    plt.show()

    # OPGAVE 1b


def scale_data(X):
    # Deze methode krijgt een matrix mee waarin getallen zijn opgeslagen van 0..m, en hij
    # moet dezelfde matrix retourneren met waarden van 0..1. Deze methode moet werken voor
    # alle maximale waarde die in de matrix voorkomt.
    # Deel alle elementen in de matrix 'element wise' door de grootste waarde in deze matrix.

    # YOUR CODE HERE
    return X / np.amax(X)

# OPGAVE 1c


def build_model():
    # Deze methode maakt het keras-model dat we gebruiken voor de classificatie van de mnist
    # dataset. Je hoeft deze niet abstract te maken, dus je kunt er van uitgaan dat de input
    # layer van dit netwerk alleen geschikt is voor de plaatjes in de opgave (wat is de
    # dimensionaliteit hiervan?).
    # Maak een model met een input-laag, een volledig verbonden verborgen laag en een softmax
    # output-laag. Compileer het netwerk vervolgens met de gegevens die in opgave gegeven zijn
    # en retourneer het resultaat.

    # Het staat je natuurlijk vrij om met andere settings en architecturen te experimenteren.

    # YOUR CODE HERE

    model = models.Sequential()

    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )

    return model


# OPGAVE 2a
def conf_matrix(labels, pred):
    # Retourneer de econfusion matrix op basis van de gegeven voorspelling (pred) en de actuele
    # waarden (labels). Check de documentatie van tf.math.confusion_matrix:
    # https://www.tensorflow.org/api_docs/python/tf/math/confusion_matrix

    # YOUR CODE HERE
    return tf.math.confusion_matrix(labels, pred)


# OPGAVE 2b
def conf_els(conf, labels):
    # Deze methode krijgt een confusion matrix mee (conf) en een set van labels. Als het goed is, is
    # de dimensionaliteit van de matrix gelijk aan len(labels) × len(labels) (waarom?). Bereken de
    # waarden van de TP, FP, FN en TN conform de berekening in de opgave. Maak vervolgens gebruik van
    # de methodes zip() en list() om een list van len(labels) te retourneren, waarbij elke tupel
    # als volgt is gedefinieerd:

    #     (categorie:string, tp:int, fp:int, fn:int, tn:int)

    # Check de documentatie van numpy diagonal om de eerste waarde te bepalen.
    # https://numpy.org/doc/stable/reference/generated/numpy.diagonal.html

    n = len(labels)
    results = []

    for i, label in enumerate(labels):
        # True positives.
        TP = conf[i][i]

        # False positives.
        FP = 0 - TP
        for l in range(n):
            FP += conf[i][l]

        # False negatives.
        FN = 0 - TP
        for l in range(n):
            FN += conf[l][i]

        # True negatives.
        TN = np.sum(conf) - TP - FP - FN

        results.append((label, TP, FP, FN, TN))

    return results


def conf_data(metrics):
    # Deze methode krijgt de lijst mee die je in de vorige opgave hebt gemaakt (dus met lengte len(labels))
    # Maak gebruik van een list-comprehension om de totale tp, fp, fn, en tn te berekenen en
    # bepaal vervolgens de metrieken die in de opgave genoemd zijn. Retourneer deze waarden in de
    # vorm van een dictionary (de scaffold hiervan is gegeven).

    # VERVANG ONDERSTAANDE REGELS MET JE EIGEN CODE

    tp = sum([x[1] for x in metrics])
    fp = sum([x[2] for x in metrics])
    fn = sum([x[3] for x in metrics])
    tn = sum([x[4] for x in metrics])

    # BEREKEN HIERONDER DE JUISTE METRIEKEN EN RETOURNEER DIE
    # ALS EEN DICTIONARY

    tpr = tp / (tp + fn)
    ppv = tp / (tp + fp)
    tnr = tn / (tn + fp)
    fpr = fp / (fp + tn)

    rv = {'tpr': tpr, 'ppv': ppv, 'tnr': tnr, 'fpr': fpr}
    return rv
