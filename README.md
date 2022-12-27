# CNN From Scratch
Convolutional Neural Network written from scratch using numpy with API similar to tensorflow

## Implemented Elements

### Layers
- `InputLayer`
- `DenseLayer`
- `BiasLayer`
- `ActivationLayer (relu, leaky reLu, sigmoid, tanh, sin)`
- `DropoutLayer`
- `FlattenLayer`
- `Conv2DLayer (with bias & stride)`
- `Pool2DLayer (max, min)`
- `Padding2DLayer`
- `Crop2DLayer`
- `SoftmaxLayer`

### Losses
- `MSE`
- `CCE`

### Initializers
- `ConstantInitializer`
- `RandomNormalInitializer`
- `RandomUniformInitializer`
- `GlorotUniformInitialization`

### Metrics
- `CategoricalAccuracy`

### Callbacks
- `ModelCheckpoint`
- `EarlyStopping`

## Usage Example

### Definition
```
layers = [
    nn.layers.InputLayer((28, 28, 1)),
    nn.layers.Conv2DLayer(32, kernel_size=3, stride=1),
    nn.layers.ActivationLayer('relu'),
    nn.layers.FlattenLayer(),
    nn.layers.DenseLayer(128),
    nn.layers.BiasLayer(),
    nn.layers.ActivationLayer('relu'),
    nn.layers.DropoutLayer(0.5),
    nn.layers.DenseLayer(10),
    nn.layers.BiasLayer(),
    nn.layers.SoftmaxLayer(),
]

model = nn.network.Sequential(layers)
```

### Compilation
```
model.compile(
    loss='cce',
    metrics=['categorical_accuracy']
)
```

### Fitting
```
checkpoint_callback = nn.callbacks.ModelCheckpoint('checkpoint.dat')

history = model.fit(
    train_x,
    train_y,
    validation_data=(test_x], test_y),
    learning_rate=0.001,
    epochs=10,
    callbacks=[checkpoint_callback],
)
```

### Predicting
```
predictions = model.predict(test_x)
```
