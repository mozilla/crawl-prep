ALEXA_LIST_FILE = "lists/ALEXA-cannonical-top1m_24-07-2019.csv"
TRANCO_LIST_FILE = "lists/TRANCO-cannonical-top1m_24-07-2019.csv"
FINAL_LIST_FILE = "final_list.csv"

# Set the desired final list length in terms of ALEXA maximum index.
# The final list contains the union of this many top entries from both lists.
FINAL_IDX = 10000


def read_list_csv(csv_file):
    """Read in a top site list formatted as <n>,<tld> (no headers)."""
    list_entries = []
    with open(csv_file, "rb") as f:
        for line in f:
            tld = str(line, "UTF-8").rstrip().split(",")[1]
            list_entries.append(tld)
    return list_entries


def write_list_file(tld_list, list_file):
    """Write a top site list to file.

    Writes one entry per line with no index.
    """
    with open(list_file, "w") as f:
        for tld in tld_list:
            f.write(tld + "\n")


# Holder for the combined list
final_list = []

# Open and parse the ALEXA TLD list from local csv.
a = read_list_csv(ALEXA_LIST_FILE)
# Truncate ALEXA list to minimum necessary elements to process.
a = a[0:FINAL_IDX]
# Save the ALEXA list into a set type for sanity checking list
# combination operations.
alexa_set = set(a)
alexa_subset_length = len(a)

# Open and parse the TRANCO TLD list from local csv.
t = read_list_csv(TRANCO_LIST_FILE)
# Truncate TRANCO list to minimum necessary elements to process.
t = t[0:FINAL_IDX]
# Save the TRANCO list into a set type for sanity checking list
# combination operations.
tranco_set = set(t)
tranco_subset_length = len(t)

# The combined list is generated by taking the union of top elements from
# both lists. The rank in the final list is the minimum rank at which the
# TLD appeared in either list, with ties broken in favour of Alexa.
for i in range(len(a)):
    # Guarantee that the ALEXA list is completely represented in the final
    # list.
    current_alexa_element = a.pop(0)
    # Guarantees complete coverage of ALEXA list even if this element was
    # added from earlier position in TRANCO list.
    if current_alexa_element not in final_list:
        final_list.append(current_alexa_element)

    # Check if the corresponding index in TRANCO is already in the list.
    current_tranco_element = t.pop(0)
    if current_tranco_element not in final_list:
        # If not, add the tranco list element.
        final_list.append(current_tranco_element)

final_list_set = set(final_list)
print("Length of combined ALEXA/TRANCO list: " + str(len(final_list)))

set_validation = len(final_list) == len(final_list_set)
print(
    "Verifying that the list is composed of only unique elements: "
    + str(set_validation)
)

alexa_in_final = alexa_set.issubset(final_list_set)
print(
    "The ALEXA list, truncated at "
    + str(alexa_subset_length)
    + " elements, is a complete subset of the final list of "
    + str(len(final_list))
    + " elements: "
    + str(alexa_in_final)
)

tranco_in_final = tranco_set.issubset(final_list_set)
print(
    "The TRANCO list, truncated at "
    + str(tranco_subset_length)
    + " elements, is a complete subset of the final list of "
    + str(len(final_list))
    + " elements: "
    + str(tranco_in_final)
)

# print("The Final List:")
# print(final_list)

write_list_file(final_list, FINAL_LIST_FILE)
