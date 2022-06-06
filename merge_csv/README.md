
# Merge

A merge script to merge two csv files with the structure [Title, Content, Date] and keep
one instance of each titles, keeping the most recent ones

There are two csv files, movie1 and movie2 and the resulting merged file merge along with the script

It works by using panda to concatenate the csv files and then delete duplicated of the titles, keeping only the most recent ones (detected after sorting by the date)