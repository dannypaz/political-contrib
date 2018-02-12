# Danny Paz's Political Contributions Roadmap Program of Doom

# Description

I tried to stay away from using any libraries outside of standard lib, so you will see code
that is not as concise as it would be to use numpy, or scikit.

#### Features

I went with a producer/consumer model (same as you would see in utilities such as Spark). The
process for a 'stream' starts at ingestion, to normalization, and then to representation where
we mutate the data into the format we would like to export.

New lines will be added as data comes in for repeat donors.

#### Error Handling
I have omitted most error handling because of the nature of the project, however if I were
to continue to add to the project I would check for the following:

1. All files exists (before being loaded)
2. All output paths exist

# Before you begin

# Running the program

```run.sh```

# Tests

You may need to add executable permissions to the `run.sh` by running the following: `chmod +x run.sh`.

Run tests with the following command:
