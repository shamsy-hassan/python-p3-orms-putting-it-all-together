#!/usr/bin/env python3

from dog import Dog, CONN, CURSOR

# Ensure a clean table
Dog.drop_table()
Dog.create_table()

# Insert dogs
joey = Dog("joey", "cocker spaniel")
joey.save()

fanny = Dog("fanny", "cockapoo")
fanny.save()

# Inspect with ipdb
import ipdb; ipdb.set_trace()
