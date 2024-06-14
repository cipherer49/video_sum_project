import json

def find_unique_arrays(json_file):

  with open(json_file, 'r') as f:
    data = json.load(f)

  # Use a dictionary to store unique arrays and their counts
  unique_arrays = {}
  total_count = 0
  for item in data:
    # Convert the array to a hashable tuple for efficient storage in the dictionary
    array_as_tuple = tuple(item)
    if array_as_tuple not in unique_arrays:
      unique_arrays[array_as_tuple] = 0
    unique_arrays[array_as_tuple] += 1
    total_count += 1  # Increment total count for each item processed

  if unique_arrays:
    print("Unique arrays and their occurrences:")
    for array, count in unique_arrays.items():
      # Convert the tuple back to a list for user-friendly output
      print(f"Array: {list(array)} - Count: {count}")
    print(f"\nTotal count of unique arrays: {total_count}")
  else:
    print("No unique arrays found in", json_file)

# Example usage
json_file = 'labels/Air-force.json'
find_unique_arrays(json_file)
