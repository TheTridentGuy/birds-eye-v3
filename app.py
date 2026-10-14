from flask import Flask, request, Response, render_template, redirect, abort
import dotenv
import tba
import json


app = Flask(__name__)
dotenv.load_dotenv()