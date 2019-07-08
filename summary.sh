#!/bin/sh

SUM_A=$(../sum a)
SUM_B=$(../sum b)

echo 去重前: $SUM_A
cat a

echo
echo 去重后: $SUM_B
cat b
