from get_id import get_id_g
import pathlib
import requests
from requests import post
import sys
if sys.version_info < (3, 0):  # Pytohn2.x
    from urllib import urlencode
else:  # Python3.x
    from urllib.parse import urlencode
from flask import Flask, render_template, abort, session, request, redirect, jsonify
import google.auth.transport.requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import os
from pip._vendor import cachecontrol
from flask_sqlalchemy import SQLAlchemy
import datetime