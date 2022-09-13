#!/bin/sh
num=1
for file in *.jpg; do
       mv "$file" "p$(printf "%u" $num).jpg"
       let num=$num+1
done