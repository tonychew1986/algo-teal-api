from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
  
from Naked.toolshed.shell import execute_js, muterun_js

from pyteal import *
import uuid, base64
from algosdk import algod, transaction, account, mnemonic

import time
import re

import os

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('code')


app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route("/")
# @cross_origin()
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        args = parser.parse_args()
        print (args['code'])
        
        uid = str(uuid.uuid4())
        teal_file = "tempFile-" + uid + ".teal"
        with open(teal_file, "w+") as f:
            f.write(args['code'])
        lsig_fname = "tempFile-" + uid + ".tealc"

        # stdout, stderr = execute(["./goal", "clerk", "compile", "-o", lsig_fname, teal_file])

        stdout, stderr = execute(["./goal", "clerk", "compile", teal_file])

        if stderr != "":
            print(stderr)
            raise
        elif len(stdout) < 59:
            print("error in compile teal")
            raise
            
        if os.path.exists(teal_file):
          os.remove(teal_file)
          os.remove(teal_file + ".tok")
        else:
          print("The file does not exist")

        print("stdout", stdout)
        
        return args['code'], 201
        
        
class Compile(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        args = parser.parse_args()
        print (args['code'])
        
        uid = str(uuid.uuid4())
        teal_file = "tempFile-" + uid + ".teal"
        with open(teal_file, "w+") as f:
            f.write(args['code'])
        lsig_fname = "tempFile-" + uid + ".tealc"

        # stdout, stderr = execute(["./goal", "clerk", "compile", "-o", lsig_fname, teal_file])

        stdout, stderr = execute(["./goal", "clerk", "compile", teal_file])

        if stderr != "":
            print("stderr", stderr)
            
            return {
                "response_status": 400
            }
            raise
        elif len(stdout) < 59:
            print("error in compile teal")
            
            return {
                "response_status": 400
            }
            raise
            
        else:
            print("stdout", stdout)
            print("teal_file", teal_file)
            # print("teal_tok_file", teal_tok_file)
            # 
            # time.sleep(5)
            # 
            teal_tok_file = "tempFile-" + uid + ".teal.tok"
            # teal_tok_file = "tempFile-050d50c0-69fd-452d-ab7c-a83cb7eae2b8.teal.tok"
            print("-----")
            # data = open(teal_tok_file, "r").read()
            
            with open(teal_tok_file, 'rb') as f:
                data = f.read()
                
                
            print("-----")
            print("data", data)
            base64_bytes = base64.b64encode(data)
            print("base64_bytes", base64_bytes)
            base64_string = base64_bytes.decode('utf-8')
            print("base64_string", base64_string)
            
            stdResponse = re.split('[:]', stdout)
            
            if os.path.exists(teal_file):
              os.remove(teal_file)
              os.remove(teal_tok_file)
            else:
              print("The file does not exist")
            
            return {
                "file_name": stdResponse[0].strip(), 
                "address": stdResponse[1].strip(), 
                "contractBase64": base64_string, 
                "response_status": 201
            }
            
            
class ExecuteJs(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        args = parser.parse_args()
        print (args['code'])
        
        uid = str(uuid.uuid4())
        js_file = "tempFile-" + uid + ".js"
        with open(js_file, "w+") as f:
            f.write(args['code'])
            
        response = muterun_js(js_file)
        print("response", response)
        print("response.stdout", response.stdout)
        
        if os.path.exists(js_file):
          os.remove(js_file)
        else:
          print("The file does not exist")
        
        if response.exitcode == 0:
            print(response.stdout)
            
            stdResponse = re.split('\n', (response.stdout).decode("utf-8"))
            print(stdResponse)
            
            return {
                "response": stdResponse, 
                "response_status": 201
            }
        else:
            response.stderr.write(response.stderr)
            
        # response = muterun_js(js_file)
        # result = execute_js(js_file)
        # print("result", result)
        # return {
        #      "response": execute_js(js_file), 
        #      "response_status": 201
        #  }
        # result = response.stdout.decode("utf-8")
        # print("result", result)
        # 
        # if response.exitcode == 0:
        #   print(response.stdout)
        # 
        #   return {
        #       "response": response.stdout, 
        #       "response_status": 201
        #   }
        # else:
        #   sys.stderr.write(response.stderr)
        # 
        #   return {
        #       "response_status": 400
        #   }
    

# if request.method == "OPTIONS": # CORS preflight
#     return _build_cors_prelight_response()
# elif request.method == "POST": # The actual request following the preflight
#     order = OrderModel.create(...) # Whatever.
#     return _corsify_actual_response(jsonify(order.to_dict()))

# def _build_cors_prelight_response():
#     response = make_response()
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add('Access-Control-Allow-Headers', "*")
#     response.headers.add('Access-Control-Allow-Methods', "*")
#     return response
# 
# def _corsify_actual_response(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response            


api.add_resource(HelloWorld, '/')
api.add_resource(Compile, '/compile')
api.add_resource(ExecuteJs, '/execute/js')

if __name__ == '__main__':
    app.run(debug=True)
