---
layout: post
title:  'Linear Algebra for Machine Learning'
author: jane
categories: [ Machine Learning ]
image: assets/images/linear-algebra.jpg
tags: [Machine Learning, Linear Algebra]
---

# Linear Algebra for Machine Learning (Part 1): The Building Blocks of Data

Welcome to the first article in our series designed to build your understanding of linear algebra for machine learning. If you've ever felt that the math behind machine learning is an intimidating black box, you're in the right place. The goal of this series is to pry that box open, starting with the most fundamental concepts.

Think of it like learning to read. Before you can understand a novel, you must first learn the alphabet. In the world of machine learning, our "alphabet" consists of the objects we use to represent data. This article introduces you to these foundational building blocks: **scalars, vectors, matrices, and tensors.**

## What We'll Cover
*   **Scalars:** The simplest data form.
*   **Vectors:** How we represent a single data point or feature set.
*   **Matrices:** How we organize entire datasets.
*   **Tensors:** The generalization of these concepts for more complex data.

---

### Scalars: The Simplest Form of Data

A **scalar** is just a single number. It's the simplest type of data we can have.

In machine learning, a scalar can represent:
*   A single feature of a data point, like the **age** of a person (e.g., 25).
*   A label or a target value, like the **price** of a house (e.g., $450,000).
*   A hyperparameter of a model, like the **learning rate** (e.g., 0.01).

You've been working with scalars your whole life, so this one is straightforward!

### Vectors: Organizing Information for a Single Data Point

A **vector** is an ordered list of numbers. You can think of it as a single row or column of data. In linear algebra, we often visualize vectors as arrows pointing from an origin to a specific point in space.

**Definition:** A vector is a 1-dimensional array of numbers.

**In Machine Learning:** Vectors are one of the most common ways to represent data. A single data point is almost always represented as a vector. Each element in the vector corresponds to a specific **feature**.

**Example:** Imagine we have a dataset about houses. We want to describe a single house using its features: `square footage`, `number of bedrooms`, and `age in years`. We can represent a single house as a feature vector **v**:

**v** = `[1500, 3, 20]`

Here, `1500`, `3`, and `20` are the elements of the vector. The position matters: the first element is always square footage, the second is the number of bedrooms, and so on.


*A simple 2D vector **v** = `[3, 4]` can be visualized as an arrow from the origin (0,0) to the point (3,4).*

### Matrices: Representing Entire Datasets

A **matrix** is a 2-dimensional grid of numbers, arranged in rows and columns. If a vector represents a single data point, a matrix is the natural way to represent an **entire dataset** containing multiple data points.

**Definition:** A matrix is a 2-dimensional array of numbers.

**In Machine Learning:** This is the standard way to structure your input data before feeding it into a model.
*   **Rows:** Each row corresponds to a single data point (e.g., a single house, a single user, a single patient).
*   **Columns:** Each column corresponds to a single feature (e.g., square footage, age, blood pressure).

**Example:** Let's expand our housing example to include three houses. We can organize this data in a matrix **X**:

| | Square Footage (Feature 1) | Bedrooms (Feature 2) | Age (Feature 3) |
| :--- | :---: | :---: | :---: |
| **House 1** | 1500 | 3 | 20 |
| **House 2** | 2100 | 4 | 5 |
| **House 3** | 1200 | 2 | 35 |

This table translates directly into the following 3x3 matrix (3 data points, 3 features):

```
     [1500, 3, 20]
X =  [2100, 4,  5]
     [1200, 2, 35]
```

Another key example is a grayscale image, which is simply a matrix where each value represents the intensity of a single pixel.

### Tensors: Data in Higher Dimensions

So what comes after scalars (0D), vectors (1D), and matrices (2D)? **Tensors.**

A **tensor** is a generalization of these objects to any number of dimensions. Tensors are the standard data structure in modern machine learning, especially in deep learning frameworks like TensorFlow and PyTorch.

*   A **scalar** is a 0D tensor.
*   A **vector** is a 1D tensor.
*   A **matrix** is a 2D tensor.

**In Machine Learning:** Tensors are used to represent more complex data.
*   **Color Images:** A color image is a **3D tensor**. It has `height`, `width`, and `color channels` (e.g., Red, Green, Blue). So, a 256x256 pixel color image would be represented as a `(256, 256, 3)` tensor.
*   **Video Data:** A video is a sequence of images. So, it would be a **4D tensor**: `(number of frames, height, width, color channels)`.
*   **Batches of Data:** When training a model, we often feed it a "batch" of data points at once. If our dataset is a matrix `X`, a batch of 32 data points would be a `(32, number_of_features)` tensor.

---

### What's Next?

Congratulations! You now understand the fundamental "nouns" of linear algebra—the objects we use to contain and organize data. You can see how a simple number, a list of features, a whole dataset, and even video data can be represented mathematically.

But knowing the alphabet is just the first step. To form words and sentences, we need verbs—actions and operations.

In **Part 2** of this series, we will explore the essential operations that allow us to manipulate these vectors and matrices. We'll cover the dot product and matrix multiplication, and see how these operations form the computational core of machine learning models like neural networks.
