# This app is a REST api to simulate banking
## We have two versions with same endpoints, one write using Flask and the other using Django Rest Framework

### Here, you can see the documentation for the API

*  Endpoints

obs1: parameters are from request body (json)

obs2: endpoint requires a `/api/v1` prefix, ex: `localhost:5000/api/v1/extract`

obs3: you need to send your auth token in request header `Authorization` to access the API for **ALL** endpoints **EXCEPT /user POST and /login**

**/login**

| Method |     Description             |  Parameters  |
| ------ | --------------------------- | ------------ |
|  POST  |  Give user the auth token to access API   | *email*, *password* |


**/user**

| Method |     Description             |  Parameters  |
| ------ | --------------------------- | ------------ |
| POST   |  Insert an new user to the system  | *email*, *password*, *doc_number*  |
| GET    |  Retrieve your user info  | empty  |
| PATCH  |  Update your user information  |  *email*, *password*, *doc_number*  (all optional)  |
| DELETE |  *Soft* delete your user | empty  |


**/deposit**

| Method |     Description             |  Parameters  |
| ------ | --------------------------- | ------------ |
|  POST  | Deposit some amount to your account   |  *value*   |


**/withdraw**

| Method |     Description             |  Parameters  |
| ------ | --------------------------- | ------------ |
|  POST  | Withdraw some amount from your account   |  *value*   |


**/transfer**

| Method |     Description             |  Parameters  |
| ------ | --------------------------- | ------------ |
|  POST  | Send some amount from your account to another one  |  *destiny_doc_number*, *value*   |


**/statements**

| Method |     Description             |  Parameters  |
| ------ | --------------------------- | ------------ |
|  GET   |  List all your transactions and your account current balance  |  empty   |


