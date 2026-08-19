#list s3 buckets
from langchain.tools import tool
import sys
import boto3
import json

s3 = boto3.client("s3")

@tool
def list_s3_buckets():
    """lists all the s3 buckets"""
    try:
        response = s3.list_buckets()
        return json.dumps({
            "status": True,
            "message": "S3 buckets listed",
            "buckets": response["Buckets"]
        }, default=str)
    except Exception as e:
        return json.dumps({
            "status": False,
            "message": "error listing s3 buckets",
            "error_type": type(e).__name__,
            "error": str(e)
        }, default=str)

@tool
def create_s3_bucket(bucket_name):
    """creates an s3 bucket by name"""
    try:
        response = s3.create_bucket(
            Bucket=bucket_name,
        )
        return json.dumps({
            "status": True,
            "message": "S3 bucket created",
            "bucket_name": bucket_name,
            "aws_response": response
        }, default=str)
    except Exception as e:
        return json.dumps({
            "status": False,
            "message": "error creating s3 bucket",
            "error_type": type(e).__name__,
            "error": str(e)
        }, default=str)

@tool
def get_bucket_by_name(bucket_name):
    """gets the bucket by name"""
    response = s3.list_buckets()
    for bucket in response["Buckets"]:
        if bucket_name == bucket["Name"]:
            return bucket["Name"], str(bucket["CreationDate"])
    return "bucket not found","not found"

#helper function
def get_bucket_by_name_helper(bucket_name):
    """gets the bucket by name as a helper function for a tool"""
    response = s3.list_buckets()
    for bucket in response["Buckets"]:
        if bucket_name == bucket["Name"]:
            return bucket["Name"]
    return "bucket not found"

@tool
def delete_s3_bucket(bucket_name):
    """deletes an s3 bucket by name"""
    bucket_name = get_bucket_by_name_helper(bucket_name)
    if bucket_name == "bucket not found":
        return "bucket not found"
    else:
        try:
            response = s3.delete_bucket(
                Bucket=bucket_name,
            )
            return json.dumps({
                "status": True,
                "message": "S3 bucket deleted",
                "bucket_name": bucket_name,
                "aws_response": response
            }, default=str)
        except Exception as e:
            return json.dumps({
                "status": False,
                "message": "error deleting s3 bucket",
                "error_type": type(e).__name__,
                "error": str(e)
            }, default=str)