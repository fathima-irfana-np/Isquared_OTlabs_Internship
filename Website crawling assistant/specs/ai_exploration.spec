# AI Generated UI Exploratory Tests

## Explore switching between degree and radian modes during calculation

* Navigate to the Scientific Calculator page
* Ensure calculator is in degree mode
* Enter sin(90)
* Toggle calculator mode to radian without clearing input
* Press '='
* Observe displayed result or error behavior

## Verify interrupting user flow by navigating during input

* Navigate to the Scientific Calculator page
* Enter sin(90)
* Navigate to the BMI Calculator page while input is still present
* Observe displayed result or error behavior

## Explore reusing UI state across actions

* Navigate to the Scientific Calculator page
* Enter sin(90)
* Navigate to the Math Calculators page
* Enter sin(90) again
* Observe displayed result or error behavior

## Test edge-case sequence: switching between degree and radian modes multiple times

* Navigate to the Scientific Calculator page
* Ensure calculator is in degree mode
* Enter sin(90)
* Toggle calculator mode to radian without clearing input
* Press '='
* Toggle calculator mode to degree without clearing input
* Press '='
* Toggle calculator mode to radian without clearing input
* Press '='
* Observe displayed result or error behavior

## Explore interrupting user flow by interacting with dynamic UI elements during input

* Navigate to the Scientific Calculator page
* Enter sin(90)
* Interact with the Search button while input is still present
* Observe displayed result or error behavior

## Verify calculator handles invalid input correctly when switching between degree and radian modes

* Navigate to the Scientific Calculator page
* Ensure calculator is in degree mode
* Enter invalid input (e.g. 'abc')
* Toggle calculator mode to radian without clearing input
* Press '='
* Observe displayed result or error behavior

