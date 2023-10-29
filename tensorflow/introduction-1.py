# TensorFlow 2.0 Introduction - Python (.py) file

# Importing necessary libraries
import tensorflow as tf

# 1. TensorFlow Install and Setup
# TensorFlow is assumed to be installed.
# This can be done using: pip install tensorflow for the CPU version
# or pip install tensorflow-gpu for the GPU version

# Checking TensorFlow version to ensure it is 2.x
print("TensorFlow version:", tf.__version__)
print("Ensure that the TensorFlow version is 2.x")

# 2. Representing Tensors
# Tensors are multi-dimensional arrays with a uniform type

# Creating various tensors
string_tensor = tf.Variable("this is a string", dtype=tf.string)
number_tensor = tf.Variable(324, dtype=tf.int16)
floating_tensor = tf.Variable(3.567, dtype=tf.float64)

# 3. Tensor Shape and Rank
# Rank: Number of tensor dimensions
# Shape: Number of elements in each dimension

# Creating tensors of different ranks
rank1_tensor = tf.Variable(["Test"], dtype=tf.string)
rank2_tensor = tf.Variable([["test", "ok"], ["test", "yes"]], dtype=tf.string)

# Displaying tensor rank
print("Tensor rank:", tf.rank(rank2_tensor).numpy())

# Displaying tensor shape
print("Tensor shape:", rank2_tensor.shape)

# 4. Types of Tensors
# TensorFlow provides several types of tensors, including:
# - Variable: Mutable tensor, can change value during execution
# - Constant, Placeholder, SparseTensor: Immutable tensors

# Creating a variable tensor
variable_tensor = tf.Variable([1, 2, 3])

# Printing the variable tensor
print("Variable tensor:", variable_tensor)

# 5. Slicing Tensors
# Selecting specific elements or sections of a tensor

# Creating a 2D tensor
matrix = [[1, 2, 3, 4, 5],
          [6, 7, 8, 9, 10],
          [11, 12, 13, 14, 15],
          [16, 17, 18, 19, 20]]
tensor = tf.Variable(matrix, dtype=tf.int32)

# Slicing examples
three = tensor[0, 2]  # Selects the 3rd element from the 1st row
row1 = tensor[0]  # Selects the first row
column1 = tensor[:, 0]  # Selects the first column
row_2_and_4 = tensor[1::2]  # Selects second and fourth row

# Displaying slicing results
print("Element [0, 2]:", three.numpy())
print("First row:", row1.numpy())
print("First column:", column1.numpy())
print("Second and fourth row:", row_2_and_4.numpy())
