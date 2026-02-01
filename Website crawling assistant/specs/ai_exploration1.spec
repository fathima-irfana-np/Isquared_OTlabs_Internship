# AI Generated UI Exploratory Tests

## Explore switching between degree and radian modes during calculation

* Navigate to the Scientific Calculator page
* Ensure calculator is in degree mode
* Enter sin(90)
* Toggle calculator mode to radian without clearing input
* Press '='
* Observe displayed result or error behavior

## Verify state preservation when switching between scientific and standard modes

* Navigate to the Scientific Calculator page
* Enter sin(90)
* Toggle calculator mode to standard
* Enter sin(90)
* Observe displayed result or error behavior

## Test interrupting user flow by navigating during input

* Navigate to the Scientific Calculator page
* Enter sin(90)
* Navigate to the BMI Calculator page
* Return to the Scientific Calculator page
* Observe displayed result or error behavior

## Explore reusing UI state across actions

* Navigate to the Scientific Calculator page
* Enter sin(90)
* Clear calculator input
* Enter cos(90)
* Observe displayed result or error behavior

## Verify edge-case sequence: switching between scientific and standard modes multiple times

* Navigate to the Scientific Calculator page
* Toggle calculator mode to standard
* Toggle calculator mode to scientific
* Toggle calculator mode to standard
* Toggle calculator mode to scientific
* Observe displayed result or error behavior

## Test interrupting user flow by pressing multiple buttons during input

* Navigate to the Scientific Calculator page
* Enter sin(90)
* Press '+'
* Press '-'
* Press '='
* Observe displayed result or error behavior

## Explore reusing UI state across actions with multiple inputs

* Navigate to the Scientific Calculator page
* Enter sin(90)
* Clear calculator input
* Enter cos(90)
* Clear calculator input
* Enter tan(90)
* Observe displayed result or error behavior

## Verify edge-case sequence: switching between scientific and standard modes with multiple inputs

* Navigate to the Scientific Calculator page
* Enter sin(90)
* Toggle calculator mode to standard
* Enter cos(90)
* Toggle calculator mode to scientific
* Enter tan(90)
* Observe displayed result or error behavior