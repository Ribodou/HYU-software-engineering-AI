# REST API Definition
**Common information**
- AI player color: "black"
- Normal player color: "red"

**Template**

## Title
```
URL:            /
Method:         
URL Params:     
Body:           

Success Response:
    - Code: 200 - ok
      Content:
      {
        
      }

Error Response:
    - Code: 500
      Content:
      {
        
      }   

Sample Call:


Notes:

```

# Definitions

## Start a new Game
```
URL:            /api/game/start
Method:         POST
URL Params:     -
Body:           {
                  "difficulty": ['min-max' | 'alpha-zero']
                }

Success Response:
    - Code: 200 - ok
      Content:
      {
        "id": [inteter]
      }

Error Response:
    - Code: 500
      Content:
      {
        "msg": [error]
      }   

Sample Call:
    this.axios.get('http://localhost:8080/api/game/start')

```

## Load old game
```
URL:            /api/game/:id
Method:         GET
URL Params:     -
Body:           -

Success Response:
    - Code: 200 - ok
      Content:
      {
        "{ROW}{COL}": {
            "row": [integer],
            "col": [integer],
            "color": [red | black]
        },
        "{ROW}{COL}": {
            "row": [integer],
            "col": [integer],
            "color": ['red' | 'black']
        },
        ...
      }

Error Response:
    - Code: 500
      Content:
      {
        "msg": [error]
      }   

Sample Call:
     this.axios.get('http://localhost:8080/api/game/' + this.$route.params.id)

```

## Make a move in a game
```
URL:            /api/game/:id/move
Method:         POST
URL Params:     -
Body:           {
                    "row": [integer],
                    "col": [integer],
                    "color:": [red | black]
                }

Success Response:
    - Code: 200 - ok
      Content:
      {
        "col": [integer],
        "row:" [integer]
      }

Error Response:
    - Code: 406 - Not Acceptable
      Content:
      {
        "msg": [error]
      }   

Sample Call:
    this.axios.post(`http://localhost:8080/api/${this.$route.params.id}/move`, {row, col, color})

Notes:
    The response contains the move of the AI.

```

## Undo move
```
URL:            /api/game/:id/undo-move
Method:         POST
URL Params:     -
Body:           -

Success Response:
    - Code: 200 - ok
      Content:
      {
        "{ROW}{COL}": {
            "row": [integer],
            "col": [integer],
            "color": [red | black]
        },
        "{ROW}{COL}": {
            "row": [integer],
            "col": [integer],
            "color": ['red' | 'black']
        },
        ...
      }

Error Response:
    - Code: 500
      Content:
      {
        "msg": [error]
      }   

Sample Call:
     this.axios.post(`http://localhost:8080/api/game/${this.$route.params.id}/undo-move`)

```