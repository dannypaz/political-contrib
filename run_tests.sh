#!/bin/bash

echo ''
echo '##############################################'
echo 'RUNNING INSIGHT DATA ENGINEERING TEST SUITE!~'
echo '##############################################'
echo ''
(cd insight_testsuite && ./run_tests.sh)

echo ''
echo '##############################################'
echo 'RUNNING OUR UNIT TESTS!+'
echo '##############################################'
echo ''
(cd src && python -m unittest -v)
