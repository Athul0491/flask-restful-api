from flask import Flask 
from flask_restful import Api, Resource,reqparse, abort

app = Flask(__name__)
api = Api(app)

argument = {}
operation_get_args=reqparse.RequestParser()
operation_get_args.add_argument("num1",type=int,help="Number 1 is required",required=True)
operation_get_args.add_argument("num2",type=int,help="Number 2 is required",required=True)
operation_get_args.add_argument("operation",type=str,help="Operation to be performed is required",required=True)

def abort_if_num2_equals_zero(num2):
    if num2 == 0:
        abort(400,message="Number 2 cannot be Zero for division operator")

class Operation(Resource):
    def get(self):
        args = operation_get_args.parse_args()
        if args.operation == "*":
            return {"answer":args.num1*args.num2}
        elif args.operation == "/":
            if(len(str(args.num1))>=15 or len(str(args.num2))>=15):
                return {"message":'The Numbers must not exceed 15 digits'},413

            abort_if_num2_equals_zero(args.num2)
            quotient = round(args.num1/args.num2, 10)
            ans = str(quotient)
            dec = ans.split('.')
            decimalDigits = 5
            dec[1] = dec[1][0:decimalDigits]
            answer = '.'.join(dec)
            return {"answer":answer}
        else:
            return {"message":'Operation invalid. Please enter a valid operation: / or *'},404


api.add_resource(Operation,"/api")
if __name__ == "__main__":
    app.run(debug=True)