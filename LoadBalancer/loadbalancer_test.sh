#!/bin/bash
for i in {1..50}; do
curl -X POST -F 'username=test'$i -F 'password=Test@test'$i -F 'gender=Male' -F "email=test${i}@gmail.com" -F 'confirmpassword=Test@test'$i http://localhost:8000/register
done