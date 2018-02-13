# Danny Paz's Political Contributions Roadmap Program of Doom

# Description

Hey Insight Data Engineering!

This is my attempt at the [Insight Data Engineering Challenge]()

I have spent roughly 5 hours writing code and tests.

I stayed away from using any libraries outside of standard lib, so you will see code
that is not as concise as it would be to use numpy, or scikit.

I have also omitted databases (in-memory and the like) for a solution that should scale
w/ the amount of memory you have on your single machine.

Please see below for more information.

# Architecture

This project is broken up into 3 main parts:

1. Runners
2. Producer
3. Consumer

The project starts at `donation_analytics` which sets up our runner scripts.

Runners are scripts that were made to mimic the 'streaming' of data. These scripts will
essentially be the baseline for how we will run the program. Runners can be found in either
`donation_stream.py` or `donation_analytics.py`. Runners will injest our input file and call
our api to generate the report that we can expect for the front end.

Our producers take in a `row` from a data stream and process all applicable information
to be used by the rest of our application. For the moment, this is a POC, but in the real
world we would store this information in a DB, or send this record to a message bus to be
ingested by another service.

`contribution_formatter` and `repeat_donors` would be considered out producers

Our consumer is the calling of `repeat_donors#export` which will take all the duplicate donor
roles that have been stored in the `repeat_donors` class and export the information for ingestion
on the front end.

#### Features and Explanations

I went with a producer/consumer model (same as you would see in utilities such as Spark). The
process for a 'stream' starts at ingestion, to normalization, and then to representation where
we mutate the data into the format we would like to export.

New lines will be added as data comes in for repeat donors.

In order to store information and provide duplicate donors: For each row I have created
a UUID and CMTE_UUID. These are used to identify repeat donors AND will help me group records
based on the year.

The following formats are used for both UUID's

- UUID = name + zipcode (removed whitespace)
- CMTE_UUID = cmte_id + zipcode + year (year is generated from transaction datetime)

#### Error Handling

I have omitted most error handling because of the nature of the project, however if I were
to continue to add to the project I would check for the following:

1. All files exists (before being loaded)
2. All output paths exist

#### Limitations

The program loads all duplicate rows into memory via a hash.

For generating a report, the time complexity will be determined by how many unique
recipients are in the file AND how many repeat donors there are.

# Running the program

Make sure that appropriate input files are stored in the `input` directory at the root
of the project. Required files are: `itcont.txt` (for contribution info) and `percentile.txt`
(contains the percentile that we will be using for generated report)

Simply run the following command to use the program:

```
run.sh
```

NOTE: You may need to add executable permissions to the `run.sh` by running the following: `chmod +x run.sh`.

# Tests

Tests can be ran with the following command at the root of the directory:

```
(cd insight_testsuite && ./run_tests.sh)
```
