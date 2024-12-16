
# Neural Network Training Results for Image Classification

## Overview

This document provides a detailed analysis of the experiments conducted to train convolutional neural networks (CNNs) on an image classification dataset. The goal was to assess the impact of different neural network architectures on accuracy and loss during training and validation.

Three model configurations were evaluated, with results presented and discussed below.

---

## Model Architectures

Each of the three neural networks had a distinct layer structure, as detailed below:

### Model 1

**Code:**
```python
model = keras.models.Sequential([
    keras.layers.Conv2D(64, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.Flatten(),
    keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
```

#### Performance
- **Initial Loss**: 47.2438 (epoch 1), reduced to 0.1356 in the final epoch.
- **Initial Accuracy**: 53.11% (epoch 1), reaching 97.44% in the last training epoch.
- **Evaluation**: Final accuracy of 92.02% and a loss of 0.9522 on the validation set.

#### Analysis
The model initially showed high loss and low accuracy, but parameters quickly adjusted, leading to a significant increase in accuracy over subsequent epochs. The final accuracy on the validation set was satisfactory, though the loss remained relatively high compared to other models, indicating some difficulty in generalizing to new data.

---

### Model 2

**Code:**
```python
model = keras.models.Sequential([
    keras.layers.Conv2D(64, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.AveragePooling2D(pool_size=(2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
```

#### Performance
- **Initial Loss**: 19.3289 (epoch 1), reduced to 0.0506 in the final epoch.
- **Initial Accuracy**: 55.20%, reaching 98.73% in the last epoch of training.
- **Evaluation**: Final accuracy of 95.47% and a loss of 0.3911 on the validation set.

#### Analysis
Adding a pooling layer reduced dimensionality and improved the model's generalization. Model 2 achieved higher accuracy on the validation set than Model 1 and had a significantly lower loss, indicating improved overall performance. The pooling layer seems to have contributed to faster convergence and more efficient generalization.

---

### Model 3

**Code:**
```python
model = keras.models.Sequential([
    keras.layers.Conv2D(64, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.AveragePooling2D(pool_size=(2,2)),
    keras.layers.Conv2D(128, (3,3), activation="relu"),
    keras.layers.AveragePooling2D(pool_size=(2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
```

#### Performance
- **Initial Loss**: 3.9173 (epoch 1), reduced to 0.0575 in the final epoch.
- **Initial Accuracy**: 51.35%, reaching 98.69% in the final epoch of training.
- **Evaluation**: Final accuracy of 96.29% and a loss of 0.1890 on the validation set.

#### Analysis
With two convolutional layers and two pooling layers, Model 3 demonstrated the best results among the three configurations. The increased complexity seems to have facilitated the extraction of more robust features, allowing for superior accuracy and generalization. The model achieved the lowest loss on the validation set, indicating the least tendency toward overfitting.

--- 

Each model showed distinct advantages and limitations, highlighting the impact of pooling layers and increased convolutional filters on model performance for image classification tasks.
