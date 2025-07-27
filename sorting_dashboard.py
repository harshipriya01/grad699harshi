import pandas as pd
import streamlit as st
import time
from io import BytesIO

# Function for partitioning (used in QuickSort)
def partition(arr, low, high, col):
    pivot = arr[col].iloc[high]   
    i = low - 1
    for j in range(low, high):
        if arr[col].iloc[j] <= pivot:
            i += 1
            arr.iloc[i], arr.iloc[j] = arr.iloc[j], arr.iloc[i]
    arr.iloc[i + 1], arr.iloc[high] = arr.iloc[high], arr.iloc[i + 1]
    return i + 1

# QuickSort Implementation
def quicksort(arr, low, high, col='price'):
    if low < high:
        pi = partition(arr, low, high, col)
        quicksort(arr, low, pi - 1, col)
        quicksort(arr, pi + 1, high, col)

# MergeSort Implementation
def merge_sort(arr, col='price'):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr.iloc[:mid]
        R = arr.iloc[mid:]
        merge_sort(L, col)
        merge_sort(R, col)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[col].iloc[i] < R[col].iloc[j]:
                arr.iloc[k] = L.iloc[i]
                i += 1
            else:
                arr.iloc[k] = R.iloc[j]
                j += 1
            k += 1
        while i < len(L):
            arr.iloc[k] = L.iloc[i]
            i += 1
            k += 1
        while j < len(R):
            arr.iloc[k] = R.iloc[j]
            j += 1
            k += 1

# Insertion Sort for Hybrid Sort
def insertion_sort(arr, col='price'):
    for i in range(1, len(arr)):
        key = arr[col].iloc[i]
        j = i - 1
        while j >= 0 and key < arr[col].iloc[j]:
            arr.iloc[j + 1] = arr.iloc[j]
            j -= 1
        arr.iloc[j + 1] = key

# Hybrid Sort
def hybrid_sort(arr, low, high, col='price', threshold=10):
    if high - low < threshold:
        insertion_sort(arr.iloc[low:high + 1], col)
    elif low < high:
        pi = partition(arr, low, high, col)
        hybrid_sort(arr, low, pi - 1, col, threshold)
        hybrid_sort(arr, pi + 1, high, col, threshold)

# Helper function to convert DataFrame to CSV for download
def to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    processed_data = output.getvalue()
    return processed_data

# Streamlit UI
st.title("Sorting Algorithm Dashboard")

# Upload the dataset
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load dataset
    data = pd.read_csv(uploaded_file)
    st.write("Dataset preview:")
    st.write(data.head())

    # Select sorting column and algorithm
    sort_column = st.selectbox("Select the column to sort", options=data.columns)
    sort_algo = st.selectbox(
        "Select sorting algorithm", 
        options=["QuickSort", "MergeSort", "Hybrid Sort (QuickSort + Insertion Sort)"]
    )
    
    # Button to trigger sorting
    if st.button("Sort Dataset"):
        # Timing the sorting process
        start_time = time.time()
        
        # Sort the dataset based on the selected algorithm
        if sort_algo == "QuickSort":
            quicksort(data, 0, len(data) - 1, col=sort_column)
        elif sort_algo == "MergeSort":
            merge_sort(data, col=sort_column)
        elif sort_algo == "Hybrid Sort (QuickSort + Insertion Sort)":
            hybrid_sort(data, 0, len(data) - 1, col=sort_column)
        
        # Display sorted dataset and time taken
        st.write(f"Sorted dataset by {sort_column}:")
        st.write(data.head())
        st.write(f"Time taken: {time.time() - start_time:.4f} seconds")
        
        # Download button for the sorted dataset
        csv = to_csv(data)
        st.download_button(
            label="Download Sorted Dataset",
            data=csv,
            file_name='sorted_dataset.csv',
            mime='text/csv'
        )
