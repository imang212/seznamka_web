from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from sqlalchemy import create_engine,Table,MetaData,select,Column,Integer,String
from py2neo import Graph, Node, Relationship
from redis import Redis
from bson import json_util
import os

redis = Redis(host="redis", port=6379)
app = Flask(__name__)
app.secret_key = os.urandom(32)
graph = Graph("neo4j://neo4j:7687", auth=("neo4j", "adminpass"))

@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")

@app.route("/login",methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route("/onas", methods=['GET', 'POST'])
def onas():
    return render_template("onas.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
