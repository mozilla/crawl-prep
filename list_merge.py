import csv

# TLDs in Alexa list
a = []
# TLDs in TRANCO list
t = []
# Holder for the comboned list
final_list = []
# Set the desired final list length in terms of ALEXA minumum index.
FINAL_IDX = 10000

# Open and parse the ALEXA list from local csv.
with open(
    "/Users/mlopatka/Downloads/lists/ALEXA-cannonical-top1m_24-07-2019.csv", "rb"
) as f:
    for line in f:
        a.append(str(line, "UTF-8").rstrip().split(",")[1])

# Truncate ALEXA list to minimum necessary elements to process.
a = a[0 : FINAL_IDX + 1]
# Save the ALEXA list into a set type for sanity checking list combination operations.
alexa_set = set(a)
# This should be euqal to FINAL_IDX.
alexa_length = len(a)

# Open and parse the TRANCO list from local csv.
with open(
    "/Users/mlopatka/Downloads/lists/TRANCO-cannonical-top1m_24-07-2019.csv", "rb"
) as f:
    for line in f:
        t.append(str(line, "UTF-8").rstrip().split(",")[1])

# Truncate TANCO list to minimum necessary elements to process.
t = t[0 : FINAL_IDX + 1]
# Save the TANCO list into a set type for sanity checking list combination operations.
tranco_set = set(t)

for i in range(0, len(alexa_set)):
    # When we have depleted the Alexa list, stop appending TRANCO elements.
    if len(a) == 0:
        print(len(a))
        print(len(t))
        break
    # guarantee that the ALEX list is completely represented in the final list.
    current_alexa_element = a.pop(0)
    # Guarantees complete coverage fo ALEXA list even if this element was
    # added from earlier position in TRANCO list.
    if current_alexa_element not in final_list:
        final_list.append(current_alexa_element)

    # Check if the corresponding index into tranco is already int he list.
    current_tranco_element = t.pop(0)
    if current_tranco_element not in final_list:
        # If not, add the tranco list element.
        final_list.append(current_tranco_element)

final_list_set = set(final_list)
print("length of combined ALEXA/TRANCO list: " + str(len(final_list)))

set_validation = len(final_list) == len(final_list_set)
print(
    "Verifying that the list is composed of only unique elements: "
    + str(set_validation)
)

alexa_in_final = alexa_set.issubset(final_list_set)
print(
    "the ALEXA list, truncated at "
    + str(FINAL_IDX)
    + " elements is a complete subset of the final list of "
    + str(len(final_list))
    + " elements: "
    + str(alexa_in_final)
)

tranco_in_final = tranco_set.issubset(final_list_set)
print(
    "the TRANCO list, truncated at "
    + str(FINAL_IDX)
    + " elements is a complete subset of the final list of "
    + str(len(final_list))
    + " elements: "
    + str(tranco_in_final)
)

print("The Final List:")
print(final_list)

with open("final_list.csv", "wb") as resultFile:
    wr = csv.writer(resultFile, dialect="excel")
    for i in final_list_set:
        wr.writerow(final_list)
