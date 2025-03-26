# Ultimate Battleships

**Ultimate Battleshis** is a Command Line Interface (CLI) game. The aim of this CLI is to provide users with a way of practicing a game of Battleships, which is a game that requires outwitting your opponent.

## User Stories & Wireframes

### User Stories

The decision to make this website is due to the user stories found [here](userstory.md).

### Wireframes

From the user stories you can see the wireframes that were mocked up below.

![CLI Wireframe](assets/readmeimgs/wireframe.png)

### Logic Flow Chart

From the User Stories and wireframes a logic flow chart was mocked up to help know what the code needs to do, e.g. where error messages need to be, where loops need to be, when to end the program, etc. You can see the flow chart below.

![Logic Flowchart](assets/readmeimgs/ultimate_battleships_logic_flowchart.png)

## Responsive Design

![Responsive Mockup](INSERT)

## Features

Below are the features for the website and at the end is listed any features that weren't able to be implemented but would be with more time.

### Existing Features

#### Username Creation

- When 

### Features Left to Implement

- Create

## Testing

The 

### Fixed Bugs

- aksjhdfga

### Unfixed Bugs

- None

### Links and Actions

| Location | Link / Button | Expected Action | Pass / Fail |
| ----- | ----- | ----- | ----- |
| Username Creation | Username not entered | Tell user to fill in the field | Pass |

### Validator Testing

- PEP8

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.
