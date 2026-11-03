#!/bin/sh

set -eu

mc alias set local "$S3_ENDPOINT_URL" "$S3_ROOT_USER" "$S3_ROOT_PASSWORD"

for bucket in "$S3_BUCKET_ORIGINALS" "$S3_BUCKET_HLS" "$S3_BUCKET_IMAGES"; do
  mc mb --ignore-existing "local/$bucket"
  mc anonymous set none "local/$bucket"
done

mc ls local
echo "buckets ready"